from datetime import datetime

import requests
from pydantic import ValidationError
from requests import HTTPError, RequestException

from src.clients.cabinet.models import CabinetCycleResponse, CabinetResponse
from src.core.config import settings
from src.core.exceptions import ServerError
from src.interfaces.cabinet_client_interface import CabinetClientInterface
from src.services.models.recipe import RecipeSlotCode


class CabinetService(CabinetClientInterface):
    def __init__(self) -> None:
        self.host = settings.CABINET_API_HOST
        self.session = requests.Session()

    def get_recipe_slots(
        self,
        filter_date: datetime | None = None,
    ) -> list[RecipeSlotCode]:
        try:
            res_json = self.session.get(
                url=f"https://{self.host}/recipe-slots",
                params={"filter[date]": filter_date.strftime("%Y-%m-%d") if filter_date else None},
            ).json()
        except Exception as e:
            raise RuntimeError(f"Failed to fetch data: {e}") from e

        if not res_json:
            raise RuntimeError(f"No data found with date: {filter_date}")
        try:
            parsed_response = CabinetResponse(**res_json)
            data_items = parsed_response.data
            results = [
                RecipeSlotCode(
                    plan_id=item.attributes.plan_id,
                    plan_description=item.attributes.plan_description,
                    slot_code=item.attributes.short_code,
                )
                for item in data_items
            ]
        except Exception as e:
            raise ServerError(f"failed to parse recipe slots response data: {e}") from e

        return results

    def find_cycle(self, cycle_date: datetime) -> bool:
        try:
            res = self.session.get(
                url=f"https://{self.host}/cycles",
                params={"filter[start_date]": cycle_date.strftime("%Y-%m-%d")},
            )
            res.raise_for_status()

            parsed_response = CabinetCycleResponse.model_validate(res.json())
            cycles = parsed_response.data
            if not cycles:
                return False
            for cycle in cycles:
                if cycle.attributes.date == cycle_date.strftime("%Y-%m-%d"):
                    return True
            return False
        except (HTTPError, RequestException, ValidationError) as e:
            raise ServerError(f"Failed to retrieve cycle for date: {cycle_date}") from e
