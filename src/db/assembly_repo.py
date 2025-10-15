from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.core.exceptions import ServerError
from src.db.repo_base import RepositoryBase
from src.db.schema import assemblies, assembly_data_sources
from src.interfaces.assembly_interface import AssemblyRepoInterface
from src.services.models.assembly import AssemblyIdMapping, CulopsMappedAssembly


class AssemblyRepo(RepositoryBase, AssemblyRepoInterface):
    def get_mapped_culops_assembly_ids(self, partner_id: str, assembly_ids: list[UUID]) -> list[AssemblyIdMapping]:
        try:
            with self._connection() as conn:
                mapped_src_stmt = (
                    select(
                        assembly_data_sources.c.assembly_id,
                        assembly_data_sources.c.culops_assembly_id,
                        assemblies.c.deleted_at,
                        assemblies.c.partner_id,
                    )
                    .select_from(assembly_data_sources)
                    .join(assemblies, assembly_data_sources.c.assembly_id == assemblies.c.assembly_id)
                    .where(assemblies.c.partner_id == partner_id, assembly_data_sources.c.assembly_id.in_(assembly_ids))
                )

                mapped_src_result = conn.execute(mapped_src_stmt).mappings().fetchall()

                mapped_sources = {}
                missing_sources = {}

                for src in mapped_src_result:
                    deleted = True
                    if src.get("deleted_at") is None:
                        deleted = False

                    culops_mapped_assembly = CulopsMappedAssembly(
                        deleted=deleted,
                        assembly_id=src.get("culops_assembly_id"),
                    )
                    assembly_id_mapping = AssemblyIdMapping(
                        assembly_id=src.get("assembly_id"),
                        cullops_mapped_assembly=culops_mapped_assembly,
                    )
                    mapped_sources[src.get("assembly_id")] = assembly_id_mapping

                    mapped_src_id_list = list(mapped_sources.keys())

                    not_found_sources = [asbl_id for asbl_id in assembly_ids if asbl_id not in mapped_src_id_list]

                    for assembly_id in not_found_sources:
                        miss_cullops_mapped_assembly = CulopsMappedAssembly(
                            deleted=False,
                            assembly_id=None,
                        )

                        miss_assembly_mapping = AssemblyIdMapping(
                            assembly_id=assembly_id,
                            cullops_mapped_assembly=miss_cullops_mapped_assembly,
                        )
                        missing_sources[assembly_id] = miss_assembly_mapping

                merged_sources = {**mapped_sources, **missing_sources}

                return list(merged_sources.values())

        except SQLAlchemyError as e:
            raise ServerError(f"failed to retrieved mapped culops assembly ids {assembly_ids}") from e

    def add_assembly(
        self,
        partner_id: str,
        assembly_id: UUID,
        assembly_data_source_id: int,
    ) -> None:
        try:
            with self._connection() as conn:
                insert_stmt = assemblies.insert().values(assembly_id=assembly_id, partner_id=partner_id)
                conn.execute(insert_stmt)

                insert_stmt = assembly_data_sources.insert().values(
                    assembly_id=assembly_id, partner_id=partner_id, culops_assembly_id=assembly_data_source_id
                )
                conn.execute(insert_stmt)
                conn.commit()

        except SQLAlchemyError as e:
            raise ServerError(
                f"failed to add assembly_id {assembly_id} forculops_assembly_id {assembly_data_source_id}"
            ) from e

    def delete_assembly(self, partner_id: str, assembly_id: UUID) -> None:
        try:
            with self._connection() as conn:
                delete_stmt = assemblies.delete().where(
                    assemblies.c.assembly_id == assembly_id, assemblies.c.partner_id == partner_id
                )
                conn.execute(delete_stmt)

        except SQLAlchemyError as e:
            raise ServerError(f"failed to delete assembly_id {assembly_id}") from e
