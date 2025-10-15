from datetime import datetime


class CostMarkup:
    def __init__(self, applied_from: datetime | None, applied_until: datetime | None, markup_percent: float):
        self._applied_from: datetime | None = applied_from
        self._applied_until: datetime | None = applied_until
        self._markup_percent: float = markup_percent

    @property
    def markup_percent(self) -> float:
        return self._markup_percent


class Partner:
    def __init__(
        self,
        name: str,
        recipe_create_cutoff_days: int,
        recipe_update_cutoff_days: int | None = None,
        recipe_delete_cutoff_days: int | None = None,
        max_assemblies_per_recipe: int | None = None,
    ):
        self._name: str = name
        self._recipe_create_cutoff_days: int = recipe_create_cutoff_days
        self._recipe_update_cutoff_days: int | None = recipe_update_cutoff_days
        self._recipe_delete_cutoff_days: int | None = recipe_delete_cutoff_days
        self._max_assemblies_per_recipe: int | None = max_assemblies_per_recipe
        self._cost_markups: list[CostMarkup] = []
        self._packaging_options: list[str] = []

    @property
    def recipe_update_cutoff_days(self) -> int | None:
        return self._recipe_update_cutoff_days

    def add_cost_markup(self, cost_markup: CostMarkup) -> None:
        self._cost_markups.append(cost_markup)

    def add_packaging_option(self, packaging_option: str) -> None:
        if packaging_option not in self._packaging_options:
            self._packaging_options.append(packaging_option)


class PartnerRecipePlanMap:
    def __init__(self, plan_name: str, cabinet_plan_id: int) -> None:
        self._plan_name: str = plan_name
        self._cabinet_plan_id: int = cabinet_plan_id

    @property
    def plan_name(self) -> str:
        return self._plan_name

    @property
    def cabinet_plan_id(self) -> int:
        return self._cabinet_plan_id


class Brand:
    def __init__(self, name: str, partner_id: str, fes_name: str) -> None:
        self._name: str = name
        self._partner_id: str = partner_id
        self._fes_name: str = fes_name

    @property
    def name(self) -> str:
        return self._name


class SalesChannel:
    def __init__(self, name: str, partner_id: str, fes_name: str) -> None:
        self._name: str = name
        self._partner_id: str = partner_id
        self._fes_name: str = fes_name

    @property
    def name(self) -> str:
        return self._name

    @property
    def fes_name(self) -> str:
        return self._fes_name
