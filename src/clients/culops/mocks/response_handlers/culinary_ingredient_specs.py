import json
from collections.abc import Iterable
from typing import Any, cast
from urllib.parse import urlencode

from requests import Response

from src.clients.culops.mocks.response_data.culinary_ingredient_specs import culinary_ingredient_specifications


def get_culinary_ingredient_specifications_response_handler(headers: dict, params: dict) -> Response:
    page = int(params.get("page[number]", 1))
    available_from = params.get("available_from", None)
    available_until = params.get("available_until", None)
    filter_ids = params.get("filter[id]", [])
    brand_name = params.get("brand_name", None)

    data = _get_culinary_ingredient_specifications_data(
        available_from=available_from,
        available_until=available_until,
        filter_ids=filter_ids.split(",") if filter_ids else [],
        brand_name=brand_name,
    )

    paginated_data = _get_paginated_data(data, page, 2)
    response = Response()
    if not paginated_data:
        response.status_code = 404
        response._content = b'{"error": "No data found for the given parameters."}'
        return response

    content = json.dumps(paginated_data, ensure_ascii=False).encode("utf-8")
    response.status_code = 200
    response._content = content
    response.raise_for_status()
    return response


def _get_culinary_ingredient_specifications_data(
    available_from: str | None,
    available_until: str | None,
    filter_ids: list[str] | None = None,
    brand_name: str | None = None,
) -> list[dict[str, Any]]:
    filtered_data = []
    for culops_data in culinary_ingredient_specifications:
        included_items = cast(list[dict[str, Any]], culops_data["included"])
        brand_matched = True

        if isinstance(included_items, Iterable):
            availabilities: list[bool] = []
            found_availability = False

            for item in included_items:
                if item["type"] == "culinary-ingredient-brands":
                    if not brand_name or brand_name != item["attributes"].get("name"):
                        brand_matched = False

                if item["type"] == "culinary-ingredient-specification-availabilities":
                    found_availability = True
                    available = _is_available_within(
                        cast(list[dict[str, Any]], [item["attributes"]]),
                        available_from,
                        available_until,
                    )
                    availabilities.append(available)

            id_in_filter = True
            if filter_ids:
                id_in_filter = str(culops_data.get("data", {}).get("id", "")) in filter_ids
        if (any(availabilities) or not found_availability) and id_in_filter and brand_matched:
            filtered_data.append({"data": culops_data["data"], "included": included_items})

    return filtered_data


def _get_paginated_data(data: list[dict[str, Any]], page: int, items_per_page: int = 2) -> dict[str, Any]:
    total_items = len(data)
    total_pages = (total_items + items_per_page - 1) // items_per_page

    if page < 1 or page > total_pages:
        return {}

    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    page_data = data[start_index:end_index]

    res_data: dict[str, list] = {
        "data": [],
        "included": [],
    }

    for item in page_data:
        res_data["data"].append(item["data"])
        res_data["included"].extend(item["included"])

    encoded_query_params = urlencode({"page[number]": page + 1})
    page_number_link = f"https://culops.freshrealm.com/api/culinary_ingredient_specifications?{encoded_query_params}"

    next_link = page_number_link if page < total_pages else None

    prev_link = (
        f"https://culops.freshrealm.com/api/culinary_ingredient_specifications?page={page - 1!s}" if page > 1 else None
    )

    item_data: dict[str, Any] = {
        **res_data,
        "meta": {
            "current_page": page,
            "total_pages": total_pages,
            "total_items": total_items,
            "items_per_page": items_per_page,
        },
        "links": {
            "self": f"https://culops.freshrealm.com/api/culinary_ingredient_specifications?page={page!s}",
        },
    }

    if next_link:
        item_data["links"]["next"] = next_link
    if prev_link:
        item_data["links"]["prev"] = prev_link

    return item_data


def _is_available_within(availability: list[dict], available_from: str | None, available_until: str | None) -> bool:
    for period in availability:
        start = period.get("start")
        end = period.get("end")

        start_ok = not available_from or not start or start <= available_from
        end_ok = not available_until or not end or end <= available_until

        if start_ok and end_ok:
            return True

    return False
