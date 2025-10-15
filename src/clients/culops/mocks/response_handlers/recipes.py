import copy
import json
import random

from requests import Response

from src.clients.culops.mocks.response_data.recipes import recipe_patch_response


def patch_recipe_update_response_handler(headers: dict, json_data: dict) -> Response:
    recipe_id = json_data.get("id")
    new_attributes = json_data.get("attributes", {})

    if not recipe_id:
        response = Response()
        response.status_code = 400
        response._content = b'{"error": "Missing recipe ID."}'
        return response

    updated_data = copy.deepcopy(recipe_patch_response)

    if updated_data["data"]["id"] != str(recipe_id):
        response = Response()
        response.status_code = 404
        response._content = b'{"error": "Recipe not found."}'
        return response

    updated_data["data"]["attributes"].update(new_attributes)

    response = Response()
    response.status_code = 200
    response._content = json.dumps(updated_data, ensure_ascii=False).encode("utf-8")

    return response


def add_ingredients_response_handler(headers: dict, json_data: dict) -> Response:
    recipe_id = json_data.get("id")
    relationships = json_data.get("data", {}).get("relationships", {})

    if not recipe_id or not relationships:
        response = Response()
        response.status_code = 400
        response._content = b'{"error": "Missing recipe ID or relationships data."}'
        return response

    new_ingredient_id = str(random.randint(100000, 999999))

    response_body = {
        "data": {
            "type": "recipe_ingredient_relationships",
            "id": new_ingredient_id,
            "attributes": {
                "recipe_id": recipe_id,
                "culinary_ingredient_id": relationships.get("culinary_ingredients", {}).get("data", {}).get("id"),
                "culinary_ingredient_specification_id": relationships.get("culinary_ingredient_specification", {})
                .get("data", {})
                .get("id"),
            },
        }
    }

    response = Response()
    response.status_code = 200
    response._content = json.dumps(response_body, ensure_ascii=False).encode("utf-8")

    return response
