from collections.abc import Mapping
from copy import deepcopy
from typing import Generic, TypeVar
from urllib.parse import urlencode

from pydantic import BaseModel, ConfigDict

from src.api.routes.v1.models import Links, Meta, Pagination

T = TypeVar("T", bound=BaseModel)


class PaginatedResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    data: T
    meta: Meta | None
    links: Links


def set_nested_list(obj: T, path: str, new_list: list[T]) -> T:
    """
    Returns a copy of the object with the list at the given dot-separated path set to new_list.
    """
    obj_copy = deepcopy(obj)
    parts = path.split(".")
    current = obj_copy
    for part in parts[:-1]:
        current = getattr(current, part)
    setattr(current, parts[-1], new_list)
    return obj_copy


def paginate_response(
    *,
    items: list[T],
    item_count: int | None = None,
    page: int | None = None,
    page_size: int | None = None,
    base_url: str,
    url_params: Mapping[str, str] | None = None,
    data_model: BaseModel | None = None,
    list_attr_path: str | None = None,
) -> PaginatedResponse:
    paginated_items = items
    query_string = urlencode(url_params or [])

    if page and page_size:
        total_count = item_count or len(items)
        total_pages = ((total_count + page_size - 1) // page_size) or 1
        start = (page - 1) * page_size
        end = page * page_size

        paginated_items = items if item_count else items[start:end]

        meta = Meta(
            pagination=Pagination(
                total=total_count,
                per_page=page_size,
                current_page=page,
                total_pages=total_pages,
            )
        )

        has_prev = page > 1
        has_next = page < total_pages

        links = Links(
            self=f"{base_url}?{query_string}&page={page}",
            first=f"{base_url}?{query_string}&page=1",
            last=f"{base_url}?{query_string}&page={total_pages}",
            prev=f"{base_url}?{query_string}&page={page - 1}" if has_prev else None,
            next=f"{base_url}?{query_string}&page={page + 1}" if has_next else None,
        )
    else:
        links = Links(self=f"{base_url}{'?' if query_string else ''}{query_string}")
        meta = None

    if data_model and list_attr_path:
        model_copy = deepcopy(data_model)
        data = set_nested_list(model_copy, list_attr_path, paginated_items)
    else:
        data = paginated_items[0]

    return PaginatedResponse(data=data, meta=meta, links=links)
