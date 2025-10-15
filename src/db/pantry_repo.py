from datetime import datetime
from uuid import UUID

from dateutil import parser
from sqlalchemy import and_, func, select
from sqlalchemy.exc import SQLAlchemyError

from src.core.exceptions import ServerError
from src.db.models import PantryState
from src.db.repo_base import RepositoryBase
from src.db.schema import (
    cost_markups,
    pantry_item_availabilities,
    pantry_item_costs,
    pantry_item_custom_fields,
    pantry_item_data_sources,
    pantry_items,
    pantry_states,
)
from src.interfaces.pantry_db_interface import PantryDBInterface
from src.services.models.pantry import (
    Pantry,
    PantryItem,
    PantryItemAvailability,
    PantryItemCost,
    PantryItemCulinaryIngredientSpecification,
    PantryItemCustomField,
    PartnerCostMarkup,
)
from src.services.models.recipe import RecipePantryItemData


class PantryRepo(RepositoryBase, PantryDBInterface):
    def get_partner_pantry_by_id(
        self,
        pantry_state_id: str,
        partner_id: str,
        page_size: int,
        page: int = 1,
    ) -> tuple[Pantry | None, int]:
        try:
            pantry_state_id_uuid = UUID(pantry_state_id)
            offset = (page - 1) * page_size

            with self._connection() as conn:
                find_pantry_stmt = select(pantry_states).where(
                    pantry_states.c.pantry_state_id == pantry_state_id_uuid,
                    pantry_states.c.partner_id == partner_id,
                )
                pantry_data = conn.execute(find_pantry_stmt).mappings().fetchone()
                if not pantry_data:
                    return None, 0

                # Handle datetime values from database (already datetime objects)
                def _parse_datetime(value):
                    if value is None or value == "":
                        return None
                    # If already a datetime, return as-is
                    from datetime import datetime
                    if isinstance(value, datetime):
                        return value
                    # Otherwise parse the string
                    return parser.parse(value)

                pantry_state = PantryState(
                    partner_id=partner_id,
                    pantry_state_id=pantry_state_id_uuid,
                    pantry_state_timestamp=pantry_data["pantry_state_timestamp"],
                    items_available_from=_parse_datetime(pantry_data.get("items_available_from")),
                    items_available_until=_parse_datetime(pantry_data.get("items_available_until")),
                )

                total_count_stmt = (
                    select(func.count())
                    .select_from(pantry_items)
                    .where(pantry_items.c.pantry_state_id == pantry_state_id_uuid)
                )
                total_count = conn.execute(total_count_stmt).scalar() or 0

                get_pantry_items_stmt = (
                    select(pantry_items)
                    .where(pantry_items.c.pantry_state_id == pantry_state_id_uuid)
                    .order_by(pantry_items.c.pantry_item_id)
                    .limit(page_size)
                    .offset(offset)
                )
                pantry_items_result = conn.execute(get_pantry_items_stmt).mappings().fetchall()
                pantry_items_lookup: dict[UUID, PantryItem] = {}
                for row in pantry_items_result:
                    pantry_item = PantryItem(
                        id=str(row["pantry_item_id"]),
                        description=row["description"],
                        amount=row["amount"],
                        units=row["units"],
                        is_prepped_and_ready=row["is_prepped_and_ready"],
                        cost=[],
                        availability=[],
                        custom_fields=[],
                        brand_name=row.get("brand_name"),
                    )
                    pantry_items_lookup[row["pantry_item_id"]] = pantry_item

                if not pantry_items_lookup:
                    return Pantry(
                        pantry_state_id=pantry_state_id,
                        partner_id=partner_id,
                        pantry_state_timestamp=pantry_state.pantry_state_timestamp,
                        pantry_items=[],
                        partner_cost_markup=[],
                        ingredients_available_from=pantry_state.items_available_from,
                        ingredients_available_until=pantry_state.items_available_until,
                    ), total_count

                pantry_items_ids = list(pantry_items_lookup.keys())
                # Costs
                pantry_item_costs_stmt = select(pantry_item_costs).where(
                    pantry_item_costs.c.pantry_item_id.in_(pantry_items_ids)
                )
                for row in conn.execute(pantry_item_costs_stmt).mappings():
                    pantry_item = pantry_items_lookup[row["pantry_item_id"]]
                    start_date = parser.parse(row["applied_from"]).date() if row["applied_from"] else None
                    end_date = parser.parse(row["applied_until"]).date() if row["applied_until"] else None
                    pantry_item.add_cost(
                        PantryItemCost(
                            production_cost_us_dollars=row["production_cost_us_dollars"],
                            start_date=start_date,
                            end_date=end_date,
                        )
                    )

                # Availabilities
                pantry_item_avail_stmt = select(pantry_item_availabilities).where(
                    pantry_item_availabilities.c.pantry_item_id.in_(pantry_items_ids)
                )
                for row in conn.execute(pantry_item_avail_stmt).mappings():
                    pantry_item = pantry_items_lookup[row["pantry_item_id"]]
                    available_from = parser.parse(row["applied_from"]).date() if row.get("applied_from") else None
                    available_until = parser.parse(row["applied_until"]).date() if row.get("applied_until") else None
                    pantry_item.add_availability(
                        PantryItemAvailability(available_from=available_from, available_until=available_until)
                    )

                # Custom fields
                pantry_item_cf_stmt = select(pantry_item_custom_fields).where(
                    pantry_item_custom_fields.c.pantry_item_id.in_(pantry_items_ids)
                )
                for row in conn.execute(pantry_item_cf_stmt).mappings():
                    pantry_item = pantry_items_lookup[row["pantry_item_id"]]
                    pantry_item.add_custom_field(
                        PantryItemCustomField(
                            key=row["key"],
                            value=row["value"],
                        )
                    )

                # Partner markups
                partner_cost_markups = []
                partner_cost_markups_stmt = select(cost_markups).where(cost_markups.c.partner_id == partner_id)
                for row in conn.execute(partner_cost_markups_stmt).mappings():
                    partner_cost_markups.append(
                        PartnerCostMarkup(
                            applied_from=parser.parse(row["applied_from"]) if row.get("applied_from") else None,
                            applied_until=parser.parse(row["applied_until"]) if row.get("applied_until") else None,
                            markup_percent=row["markup_percent"],
                        )
                    )

        except SQLAlchemyError as e:
            raise ServerError(f"failed to get partner {partner_id} pantry {pantry_state_id}") from e

        pantry = Pantry(
            pantry_state_id=pantry_state_id,
            partner_id=partner_id,
            pantry_state_timestamp=pantry_state.pantry_state_timestamp,
            pantry_items=list(pantry_items_lookup.values()),
            partner_cost_markup=partner_cost_markups,
            ingredients_available_from=pantry_state.items_available_from,
            ingredients_available_until=pantry_state.items_available_until,
        )

        return pantry, total_count

    def save_pantry_state(
        self,
        pantry_state_id: UUID,
        partner_id: str,
        pantry_state_timestamp: datetime,
        items_available_from: datetime | None,
        items_available_until: datetime | None,
    ) -> None:
        try:
            with self._connection() as conn:
                pantry_state_stmt = pantry_states.insert().values(
                    pantry_state_id=pantry_state_id,
                    partner_id=partner_id,
                    pantry_state_timestamp=pantry_state_timestamp,
                    items_available_from=items_available_from,
                    items_available_until=items_available_until,
                )
                conn.execute(pantry_state_stmt)
                conn.commit()
        except SQLAlchemyError as e:
            raise ServerError(f"failed to save pantry state {pantry_state_id}") from e

    def save_pantry_items(self, pantry_state_id: UUID, items: list[PantryItem]) -> None:
        """Save pantry items using bulk inserts for better performance."""
        try:
            with self._connection() as conn:
                # Prepare bulk insert data
                items_data: list[dict] = []
                data_sources_data: list[dict] = []
                costs_data: list[dict] = []
                availabilities_data: list[dict] = []
                custom_fields_data: list[dict] = []

                for item in items:
                    if not item.pantry_item_data_source:
                        raise ValueError("Pantry item data source is required")

                    item_id_uuid = UUID(item.id)

                    # Collect pantry items data
                    items_data.append({
                        "pantry_item_id": item_id_uuid,
                        "pantry_state_id": pantry_state_id,
                        "description": item.description,
                        "amount": item.amount,
                        "units": item.units,
                        "is_prepped_and_ready": item.is_prepped_and_ready,
                        "brand_name": item.brand_name if item.brand_name else None,
                    })

                    # Collect data sources
                    data_sources_data.append({
                        "pantry_item_id": item_id_uuid,
                        "culops_culinary_ingredient_id": item.pantry_item_data_source.culops_culinary_ingredient_id,
                        "culops_culinary_ingredient_specification_id": item.pantry_item_data_source.culops_culinary_ingredient_specification_id,
                    })

                    # Collect costs
                    for cost in item.cost:
                        costs_data.append({
                            "pantry_item_id": item_id_uuid,
                            "applied_from": cost.start_date.isoformat().replace("+00:00", "Z") if cost.start_date else None,
                            "applied_until": cost.end_date.isoformat().replace("+00:00", "Z") if cost.end_date else None,
                            "production_cost_us_dollars": cost.production_cost_us_dollars,
                        })

                    # Collect availabilities
                    for availability in item.availability:
                        availabilities_data.append({
                            "pantry_item_id": item_id_uuid,
                            "applied_from": availability.available_from.isoformat().replace("+00:00", "Z") if availability.available_from else "",
                            "applied_until": availability.available_until.isoformat().replace("+00:00", "Z") if availability.available_until else "",
                        })

                    # Collect custom fields
                    if item.custom_fields:
                        for custom_field in item.custom_fields:
                            custom_fields_data.append({
                                "pantry_item_id": item_id_uuid,
                                "key": custom_field.key,
                                "value": custom_field.value,
                            })

                # Execute bulk inserts
                if items_data:
                    conn.execute(pantry_items.insert(), items_data)
                if data_sources_data:
                    conn.execute(pantry_item_data_sources.insert(), data_sources_data)
                if costs_data:
                    conn.execute(pantry_item_costs.insert(), costs_data)
                if availabilities_data:
                    conn.execute(pantry_item_availabilities.insert(), availabilities_data)
                if custom_fields_data:
                    conn.execute(pantry_item_custom_fields.insert(), custom_fields_data)

                conn.commit()
        except SQLAlchemyError as e:
            raise ServerError("failed to save pantry items") from e

    def delete_pantry(self, pantry_state_id: UUID) -> None:
        try:
            with self._connection() as conn:
                delete_costs_stmt = pantry_item_costs.delete().where(
                    pantry_item_costs.c.pantry_item_id.in_(
                        select(pantry_items.c.pantry_item_id).where(pantry_items.c.pantry_state_id == pantry_state_id)
                    )
                )
                conn.execute(delete_costs_stmt)

                delete_avails_stmt = pantry_item_availabilities.delete().where(
                    pantry_item_availabilities.c.pantry_item_id.in_(
                        select(pantry_items.c.pantry_item_id).where(pantry_items.c.pantry_state_id == pantry_state_id)
                    )
                )
                conn.execute(delete_avails_stmt)

                delete_cfs_stmt = pantry_item_custom_fields.delete().where(
                    pantry_item_custom_fields.c.pantry_item_id.in_(
                        select(pantry_items.c.pantry_item_id).where(pantry_items.c.pantry_state_id == pantry_state_id)
                    )
                )
                conn.execute(delete_cfs_stmt)

                delete_sources_stmt = pantry_item_data_sources.delete().where(
                    pantry_item_data_sources.c.pantry_item_id.in_(
                        select(pantry_items.c.pantry_item_id).where(pantry_items.c.pantry_state_id == pantry_state_id)
                    )
                )
                conn.execute(delete_sources_stmt)

                delete_items_stmt = pantry_items.delete().where(pantry_items.c.pantry_state_id == pantry_state_id)
                conn.execute(delete_items_stmt)

                delete_state_stmt = pantry_states.delete().where(pantry_states.c.pantry_state_id == pantry_state_id)
                conn.execute(delete_state_stmt)

                conn.commit()
        except SQLAlchemyError as e:
            raise ServerError(f"failed to delete pantry {pantry_state_id}") from e

    def get_pantry_item_data_sources(
        self, pantry_item_ids: list[str]
    ) -> dict[UUID, PantryItemCulinaryIngredientSpecification]:
        # Validate all IDs are valid UUIDs before querying
        for item_id in pantry_item_ids:
            try:
                UUID(item_id)
            except (ValueError, AttributeError) as e:
                raise ValueError(f"Invalid UUID format for pantry_item_id: {item_id}") from e

        with self._connection() as conn:
            try:
                stmt = select(pantry_item_data_sources).where(
                    pantry_item_data_sources.c.pantry_item_id.in_(pantry_item_ids)
                )

                rows = conn.execute(stmt).mappings().fetchall()

                culops_culinary_ingredient_ids = {}
                for row in rows:
                    culops_culinary_ingredient_ids[row["pantry_item_id"]] = PantryItemCulinaryIngredientSpecification(
                        pantry_item_id=row["pantry_item_id"],
                        culops_culinary_ingredient_specification_id=row["culops_culinary_ingredient_specification_id"],
                        culops_culinary_ingredient_id=row["culops_culinary_ingredient_id"],
                    )

                return culops_culinary_ingredient_ids
            except SQLAlchemyError as e:
                raise ServerError("Failed to get pantry item data sources") from e

    def get_pantry_item_data_by_culops_culinary_ingredient_and_specification_id(
        self, culinary_ingredient_specification_id: int, culinary_ingredient_id: int
    ) -> RecipePantryItemData | None:
        try:
            with self._connection() as conn:
                stmt = (
                    select(pantry_items)
                    .join(
                        pantry_item_data_sources,
                        pantry_items.c.pantry_item_id == pantry_item_data_sources.c.pantry_item_id,
                    )
                    .where(
                        and_(
                            pantry_item_data_sources.c.culops_culinary_ingredient_specification_id
                            == culinary_ingredient_specification_id,
                            pantry_item_data_sources.c.culops_culinary_ingredient_id == culinary_ingredient_id,
                        )
                    )
                )
                result = conn.execute(stmt).mappings().first()

                if result:
                    return RecipePantryItemData(
                        pantry_item_id=str(result["pantry_item_id"]),
                        is_prepped_and_ready=result["is_prepped_and_ready"],
                    )
                return None
        except SQLAlchemyError as e:
            raise ServerError(
                f"failed to get pantry item by culinary ingredient id {culinary_ingredient_id} "
                f"and specification id {culinary_ingredient_specification_id}"
            ) from e
