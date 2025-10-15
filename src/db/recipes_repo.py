from collections.abc import Callable
from datetime import datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError

from src.core.constants import RecipeStatus
from src.core.exceptions import ServerError
from src.db.repo_base import RepositoryBase
from src.db.schema import (
    recipe_data_sources,
    recipes,
)
from src.interfaces.recipes_repo_interface import RecipesRepoInterface
from src.services.models.recipe import CulopsRecipeRef, RecipeRef


class RecipesRepo(RepositoryBase, RecipesRepoInterface):
    def store_recipe_source(
        self,
        partner_id: str,
        recipe_id: UUID,
        culops_recipe_id: int,
        culops_product_sku: str,
        is_external: bool = False,
    ) -> None:
        try:
            with self._connection() as conn:
                recipe_stmt = recipes.insert().values(
                    recipe_id=recipe_id, partner_id=partner_id, externally_created=is_external
                )

                conn.execute(recipe_stmt)

                sources_stmt = recipe_data_sources.insert().values(
                    recipe_id=recipe_id, culops_recipe_id=culops_recipe_id, culops_product_sku=culops_product_sku
                )

                conn.execute(sources_stmt)

                conn.commit()
            return None

        except SQLAlchemyError as e:
            raise ServerError(
                f"failed to create recipe data source for recipe_id {recipe_id} "
                f"with culops_recipe_id {culops_recipe_id}"
            ) from e

    def get_culops_recipe_ref_by_id(self, partner_id: str, recipe_id: UUID) -> CulopsRecipeRef | None:
        try:
            with self._connection() as conn:
                stmt = (
                    select(
                        recipe_data_sources.c.culops_recipe_id,
                        recipes.c.deleted_at,
                    )
                    .select_from(
                        recipes.join(recipe_data_sources, recipes.c.recipe_id == recipe_data_sources.c.recipe_id)
                    )
                    .where(recipes.c.recipe_id == recipe_id, recipes.c.partner_id == partner_id)
                )

                result = conn.execute(stmt).mappings().fetchone()

                if result:
                    return CulopsRecipeRef(
                        culops_recipe_id=result["culops_recipe_id"],
                        recipe_id=recipe_id,
                        deleted=result["deleted_at"] is not None,
                    )

                return None
        except SQLAlchemyError as e:
            raise ServerError(f"failed to get recipe by id {recipe_id}") from e

    def get_recipe_sku_by_id(self, partner_id: str, recipe_id: UUID) -> tuple[str, RecipeStatus] | None:
        try:
            with self._connection() as conn:
                stmt = (
                    select(recipe_data_sources.c.culops_product_sku, recipes.c.deleted_at)
                    .select_from(
                        recipes.join(recipe_data_sources, recipes.c.recipe_id == recipe_data_sources.c.recipe_id)
                    )
                    .where(recipes.c.recipe_id == recipe_id, recipes.c.partner_id == partner_id)
                )
                result = conn.execute(stmt).mappings().fetchone()
                if result:
                    return result["culops_product_sku"], RecipeStatus(result["deleted_at"] is None)
                return None

        except SQLAlchemyError as e:
            raise ServerError(f"failed to get recipe by id {recipe_id}") from e

    def mark_recipe_as_deleted(
        self, partner_id: str, recipe_id: UUID, pre_delete_hook: Callable[[], None] | None = None
    ) -> None:
        try:
            with self._connection() as conn:
                if pre_delete_hook:
                    pre_delete_hook()

                stmt = (
                    update(recipes)
                    .where(recipes.c.recipe_id == recipe_id, recipes.c.partner_id == partner_id)
                    .values(deleted_at=datetime.now())
                )
                conn.execute(stmt)
                conn.commit()
        except SQLAlchemyError as e:
            raise ServerError(f"failed to mark recipe as deleted {recipe_id}") from e

    def get_recipe_id_by_culops_recipe_id(
        self,
        culops_recipe_id: int,
    ) -> UUID | None:
        try:
            with self._connection() as conn:
                stmt = select(recipe_data_sources.c.recipe_id).where(
                    recipe_data_sources.c.culops_recipe_id == culops_recipe_id
                )

                recipe_id: UUID | None = conn.execute(stmt).scalar_one_or_none()
                return recipe_id

        except SQLAlchemyError as e:
            raise ServerError(f"failed to look up recipe_id for culops_recipe_id {culops_recipe_id}") from e

    def get_culops_recipe_ref_by_sku(self, partner_id: str, sku: str) -> RecipeRef | None:
        try:
            with self._connection() as conn:
                stmt = (
                    select(
                        recipes.c.recipe_id,
                        recipe_data_sources.c.culops_recipe_id,
                    )
                    .select_from(
                        recipes.join(recipe_data_sources, recipes.c.recipe_id == recipe_data_sources.c.recipe_id)
                    )
                    .where(recipe_data_sources.c.culops_product_sku == sku, recipes.c.partner_id == partner_id)
                )

                result = conn.execute(stmt).mappings().fetchone()

                if result:
                    return RecipeRef(
                        culops_recipe_id=result["culops_recipe_id"],
                        recipe_id=result["recipe_id"],
                        culops_product_sku=sku,
                    )

                return None
        except SQLAlchemyError as e:
            raise ServerError(f"failed to get recipe by sku {sku}") from e

    def get_culops_recipe_refs_by_skus(self, partner_id: str, skus: list[str]) -> list[RecipeRef]:
        try:
            with self._connection() as conn:
                stmt = (
                    select(
                        recipes.c.recipe_id,
                        recipe_data_sources.c.culops_recipe_id,
                        recipe_data_sources.c.culops_product_sku,
                    )
                    .select_from(
                        recipes.join(recipe_data_sources, recipes.c.recipe_id == recipe_data_sources.c.recipe_id)
                    )
                    .where(recipe_data_sources.c.culops_product_sku.in_(skus), recipes.c.partner_id == partner_id)
                )

                results = conn.execute(stmt).mappings().fetchall()

                return [
                    RecipeRef(
                        culops_recipe_id=result["culops_recipe_id"],
                        recipe_id=result["recipe_id"],
                        culops_product_sku=result["culops_product_sku"],
                    )
                    for result in results
                ]
        except SQLAlchemyError as e:
            raise ServerError(f"failed to get recipes by skus {skus}") from e

    def get_all_recipe_refs_by_partner(self, partner_id: str) -> list[CulopsRecipeRef]:
        try:
            with self._connection() as conn:
                stmt = (
                    select(
                        recipes.c.recipe_id,
                        recipe_data_sources.c.culops_recipe_id,
                        recipes.c.deleted_at,
                    )
                    .select_from(
                        recipes.join(recipe_data_sources, recipes.c.recipe_id == recipe_data_sources.c.recipe_id)
                    )
                    .where(recipes.c.partner_id == partner_id)
                )

                results = conn.execute(stmt).mappings().fetchall()

                return [
                    CulopsRecipeRef(
                        recipe_id=row["recipe_id"],
                        culops_recipe_id=row["culops_recipe_id"],
                        deleted=row["deleted_at"] is not None,
                    )
                    for row in results
                ]

        except SQLAlchemyError as e:
            raise ServerError(f"failed to get all recipes for partner {partner_id}") from e
