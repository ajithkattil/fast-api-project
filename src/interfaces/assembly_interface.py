from typing import Protocol
from uuid import UUID

from src.services.models.assembly import AssemblyIdMapping


class AssemblyRepoInterface(Protocol):
    def get_mapped_culops_assembly_ids(self, partner_id: str, assembly_ids: list[UUID]) -> list[AssemblyIdMapping]: ...

    def add_assembly(
        self,
        partner_id: str,
        assembly_id: UUID,
        assembly_data_source_id: int,
    ) -> None: ...

    def delete_assembly(self, partner_id: str, assembly_id: UUID) -> None: ...
