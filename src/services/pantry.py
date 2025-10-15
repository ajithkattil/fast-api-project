import logging
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from uuid import UUID, uuid4

from src.api.routes.v1.models import (
    Pantry as ResponsePantry,
    PantryItem as ResponsePantryItem,
    PantryItemAvailability,
    PantryItemCost as ResponsePantryItemCost,
    PantryItemCustomField,
)

log = logging.getLogger(__name__)
from src.core.config import get_settings
from src.core.exceptions import NotFoundException, ServerError
from src.interfaces.culops_client_interface import CulopsClientInterface
from src.interfaces.pantry_db_interface import PantryDBInterface
from src.services.models.pantry import (
    DateRange,
    Pantry,
    PantryItem,
    PantryItemCost,
    PartnerCostMarkup,
)
from src.services.partner import PartnerService
from src.utils.datetime_helper import UTC_MAX, UTC_MIN, parse_from_datetime

settings = get_settings()


class PantryService:
    def __init__(
        self,
        pantry_db: PantryDBInterface,
        culops_service: CulopsClientInterface,
        partner_service: PartnerService,
    ) -> None:
        self.pantry_db = pantry_db
        self.culops_service = culops_service
        self.partner_service = partner_service
        self._executor = ThreadPoolExecutor(max_workers=1)

    def get_pantry(
        self,
        partner_id: str,
        available_from: datetime | None = None,
        available_until: datetime | None = None,
        cost_start_date: datetime | None = None,
        cost_end_date: datetime | None = None,
        pantry_state_id: str | None = None,
        brand_name: str = "",
        page_size: int = settings.DEFAULT_PAGE_SIZE,
        page: int = 1,
    ) -> tuple[ResponsePantry, int]:
        if not partner_id:
            raise ValueError("Missing partner id")

        try:
            # If pantry_state_id is provided, retrieve cached pantry from database
            if pantry_state_id:
                log.info(f"Retrieving cached pantry for partner {partner_id} with state ID {pantry_state_id}")
                pantry, total_count = self.pantry_db.get_partner_pantry_by_id(
                    pantry_state_id=pantry_state_id,
                    partner_id=partner_id,
                    page_size=page_size,
                    page=page,
                )

                if pantry is None:
                    raise NotFoundException(f"Pantry state {pantry_state_id} not found for partner {partner_id}")

                return self._build_pantry_response(pantry, cost_start_date, cost_end_date), total_count

            # Otherwise, fetch fresh data from CulOps
            def _to_utc(dt: datetime | None) -> datetime | None:
                if dt is None:
                    return None
                return dt if dt.tzinfo else dt.replace(tzinfo=UTC)

            items_available_from = _to_utc(available_from)
            items_available_until = _to_utc(available_until)

            partner_cost_markups = self.partner_service.get_partner_cost_markups()
            markups = [
                PartnerCostMarkup(
                    markup_percent=cm.markup_percent,
                    applied_from=cm._applied_from,
                    applied_until=cm._applied_until,
                )
                for cm in partner_cost_markups
            ]

            # Fetch first page immediately for fast response
            log.info(f"Fetching first page of pantry items for partner {partner_id}")
            generator = self.culops_service.get_partner_culops_pantry_data(
                available_from=items_available_from,
                available_until=items_available_until,
                partner_id=partner_id,
                brand_name=brand_name,
                page=page,
                page_size=page_size,
            )

            # Get the first page to return immediately
            first_page_items, has_next_page = next(generator)
            for pantry_item in first_page_items:
                pantry_item.cost = self.get_partner_cost(pantry_item, markups)

            # Build response with new pantry_state_id for stateful pagination
            pantry_state_id_uuid = uuid4()
            pantry_state_timestamp = datetime.now(UTC)

            pantry = Pantry(
                pantry_state_id=str(pantry_state_id_uuid),
                partner_id=partner_id,
                pantry_items=first_page_items,
                ingredients_available_from=items_available_from,
                ingredients_available_until=items_available_until,
                pantry_state_timestamp=pantry_state_timestamp,
                partner_cost_markup=markups,
            )

            # Fetch and cache ALL remaining pages in background (fire and forget)
            # This enables true stateful pagination through the entire dataset
            log.info(f"Starting background fetch of all pantry items for partner {partner_id}")
            self._executor.submit(
                self._fetch_and_cache_all_items,
                pantry_state_id_uuid,
                partner_id,
                pantry_state_timestamp,
                items_available_from,
                items_available_until,
                first_page_items,
                markups,
                brand_name,
            )

            # Return estimated total count (will be updated once background fetch completes)
            # Use first page count as a lower bound estimate
            total_count = len(first_page_items) if not has_next_page else len(first_page_items) * 20
            return self._build_pantry_response(pantry, cost_start_date, cost_end_date), total_count

        except NotFoundException:
            raise
        except Exception as e:
            if isinstance(e, ValueError):
                raise
            raise ServerError(f"Failed to get pantry for partner {partner_id}") from e

    @staticmethod
    def _build_pantry_response(
        pantry: Pantry,
        cost_start_date: datetime | None = None,
        cost_end_date: datetime | None = None,
    ) -> ResponsePantry:
        pantry_items = []

        for item in pantry.pantry_items:
            availability = [
                PantryItemAvailability(
                    startDate=parse_from_datetime(a.available_from) if a.available_from else None,
                    endDate=parse_from_datetime(a.available_until) if a.available_until else None,
                )
                for a in item.availability
            ]

            # Filter costs by date range if provided
            filtered_costs = item.cost
            if cost_start_date or cost_end_date:
                filtered_costs = [
                    c for c in item.cost
                    if PantryService._cost_in_date_range(c, cost_start_date, cost_end_date)
                ]

            cost = [
                ResponsePantryItemCost(
                    startDate=parse_from_datetime(c.start_date) if c.start_date else "",
                    endDate=parse_from_datetime(c.end_date) if c.end_date else "",
                    usDollars=c.production_cost_us_dollars,
                )
                for c in filtered_costs
            ]

            custom_fields = [
                PantryItemCustomField(
                    key=cf.key,
                    value=cf.value,
                )
                for cf in item.custom_fields
            ]

            pantry_items.append(
                ResponsePantryItem(
                    id=item.id,
                    description=item.description,
                    amount=str(item.amount),
                    units=item.units,
                    availability=availability,
                    cost=cost,
                    isPreppedAndReady=item.is_prepped_and_ready,
                    customFields=custom_fields,
                    brand=item.brand_name,
                )
            )

        return ResponsePantry(
            pantryItems=pantry_items,
            pantryStateId=pantry.pantry_state_id,
            partner_id=pantry.partner_id,
            ingredientsAvailableFrom=pantry.ingredients_available_from.strftime("%Y-%m-%d")
            if pantry.ingredients_available_from
            else "",
            ingredientsAvailableUntil=pantry.ingredients_available_until.strftime("%Y-%m-%d")
            if pantry.ingredients_available_until
            else "",
            pantryStateTimestamp=pantry.pantry_state_timestamp,
        )

    @staticmethod
    def _cost_in_date_range(
        cost: PantryItemCost,
        start_filter: datetime | None,
        end_filter: datetime | None,
    ) -> bool:
        """Check if a cost overlaps with the given date range filter."""
        # If no filters provided, include all costs
        if not start_filter and not end_filter:
            return True

        # Convert cost dates to datetime for comparison
        cost_start = cost.start_date if cost.start_date else datetime.min.replace(tzinfo=UTC)
        cost_end = cost.end_date if cost.end_date else datetime.max.replace(tzinfo=UTC)

        # Ensure filter dates have timezone
        filter_start = start_filter.replace(tzinfo=UTC) if start_filter and not start_filter.tzinfo else start_filter
        filter_end = end_filter.replace(tzinfo=UTC) if end_filter and not end_filter.tzinfo else end_filter

        # Check if cost range overlaps with filter range
        # Cost overlaps if: cost_start < filter_end AND cost_end > filter_start
        if filter_start and filter_end:
            return cost_start < filter_end and cost_end > filter_start
        elif filter_start:
            return cost_end > filter_start
        elif filter_end:
            return cost_start < filter_end

        return True

    @staticmethod
    def _split_ranges(ranges: list[DateRange]) -> list[DateRange]:
        """Split date ranges into non-overlapping, consecutive segments."""
        points = {r.start or UTC_MIN for r in ranges} | {r.end or UTC_MAX for r in ranges}
        sorted_points = sorted(points)

        return [DateRange(start=sorted_points[i], end=sorted_points[i + 1]) for i in range(len(sorted_points) - 1)]

    def _overlaps(self, range1: DateRange, range2: DateRange) -> bool:
        """Check if two date ranges overlap."""
        start1, end1 = range1.start or UTC_MIN, range1.end or UTC_MAX
        start2, end2 = range2.start or UTC_MIN, range2.end or UTC_MAX

        return start1 < end2 and end1 > start2

    def get_partner_cost(self, item: PantryItem, partner_markups: list[PartnerCostMarkup]) -> list[PantryItemCost]:
        result: list[PantryItemCost] = []

        availabilities = item.availability
        costs = item.cost
        all_ranges = [x.get_date_range() for x in (availabilities + costs + partner_markups)]
        flat_ranges = self._split_ranges(all_ranges)

        for date_slice in flat_ranges:
            matching_costs = [c for c in costs if self._overlaps(date_slice, c.get_date_range())]
            matching_avails = [a for a in availabilities if self._overlaps(date_slice, a.get_date_range())]
            if not matching_costs or (availabilities and not matching_avails):
                continue

            for cost in matching_costs:
                for markup in partner_markups:
                    if self._overlaps(date_slice, markup.get_date_range()):
                        applied_cost = round(cost.production_cost_us_dollars * (1 + markup.markup_percent / 100), 2)
                        pantry_item_cost = PantryItemCost(
                            start_date=None
                            if not date_slice.start or date_slice.start == UTC_MIN
                            else date_slice.start,
                            end_date=None if not date_slice.end or date_slice.end == UTC_MAX else date_slice.end,
                            production_cost_us_dollars=applied_cost,
                        )

                        result.append(pantry_item_cost)
                        break

        return result

    def _fetch_and_cache_all_items(
        self,
        pantry_state_id_uuid: UUID,
        partner_id: str,
        pantry_state_timestamp: datetime,
        items_available_from: datetime | None,
        items_available_until: datetime | None,
        first_page_items: list[PantryItem],
        markups: list[PartnerCostMarkup],
        brand_name: str,
    ) -> None:
        """Fetch all pantry items and cache in background using streaming batches."""
        try:
            log.info(f"Background fetch started for partner {partner_id}, state {pantry_state_id_uuid}")

            # Save pantry state first
            self.pantry_db.save_pantry_state(
                pantry_state_id=pantry_state_id_uuid,
                partner_id=partner_id,
                pantry_state_timestamp=pantry_state_timestamp,
                items_available_from=items_available_from,
                items_available_until=items_available_until,
            )
            log.info(f"Saved pantry state {pantry_state_id_uuid}")

            # Process and save first page items
            for pantry_item in first_page_items:
                pantry_item.cost = self.get_partner_cost(pantry_item, markups)

            self.pantry_db.save_pantry_items(
                pantry_state_id=pantry_state_id_uuid,
                items=first_page_items,
            )
            total_saved = len(first_page_items)
            log.info(f"Saved first page: {total_saved} items")

            # Fetch and save remaining pages in batches
            generator = self.culops_service.get_partner_culops_pantry_data(
                available_from=items_available_from,
                available_until=items_available_until,
                partner_id=partner_id,
                brand_name=brand_name,
                page=None,  # Get all pages
                page_size=None,
            )

            # Process each page as it arrives, then immediately save to DB
            for page_items, has_next in generator:
                for pantry_item in page_items:
                    pantry_item.cost = self.get_partner_cost(pantry_item, markups)

                self.pantry_db.save_pantry_items(
                    pantry_state_id=pantry_state_id_uuid,
                    items=page_items,
                )
                total_saved += len(page_items)
                log.info(f"Saved batch: {len(page_items)} items, total: {total_saved}")

                if not has_next:
                    break

            log.info(
                f"Background fetch completed successfully: {total_saved} total items for partner {partner_id}, state {pantry_state_id_uuid}",
                extra={
                    "pantry_state_id": str(pantry_state_id_uuid),
                    "partner_id": partner_id,
                    "item_count": total_saved,
                }
            )

        except Exception as e:
            log.error(
                f"Failed to fetch and cache all items for state {pantry_state_id_uuid}",
                extra={
                    "pantry_state_id": str(pantry_state_id_uuid),
                    "partner_id": partner_id,
                    "error": str(e),
                }
            )
