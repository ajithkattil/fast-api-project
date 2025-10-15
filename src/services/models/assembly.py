from uuid import UUID


class CulopsMappedAssembly:
    def __init__(
        self,
        deleted: bool,
        assembly_id: int | None = None,
    ):
        self._deleted: bool = deleted
        self._missing: bool = True if assembly_id is None else False
        self._assembly_id: int | None = assembly_id


class AssemblyIdMapping:
    def __init__(
        self,
        assembly_id: UUID,
        cullops_mapped_assembly: CulopsMappedAssembly,
    ):
        self._assembly_id: UUID = assembly_id
        self._cullops_mapped_assembly: CulopsMappedAssembly = cullops_mapped_assembly

    @property
    def assembly_id(self) -> UUID:
        return self._assembly_id

    @property
    def cullops_mapped_assembly(self) -> CulopsMappedAssembly:
        return self._cullops_mapped_assembly
