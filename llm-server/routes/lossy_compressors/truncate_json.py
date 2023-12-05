from typing import Any, Union, Dict, List


def truncate_json(
    json_obj: Union[Dict[str, Any], List[Any]], max_elements: int = 5
) -> Union[Dict[str, Any], List[Any]]:
    """
    Truncate a JSON object to contain a maximum of `max_elements` elements for each list within the JSON.

    Args:
        json_obj (Union[Dict[str, Any], List[Any]]): The JSON object to truncate.
        max_elements (int, optional): The maximum number of elements to keep in each list. Defaults to 5.

    Returns:
        Union[Dict[str, Any], List[Any]]: The truncated JSON object.
    """
    if isinstance(json_obj, list):
        # Truncate the list to contain only max_elements
        return json_obj[:max_elements]
    elif isinstance(json_obj, dict):
        return {
            key: truncate_json(value, max_elements)
            for key, value in json_obj.items()
        }
    else:
        # If it's neither a list nor a dictionary, return as is
        return json_obj
