import statistics as stats
from typing import Any, Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class UserData(BaseModel):
    """
    Pydantic model for client payloads
    """
    vals: list[dict[str, Any]] | list[int | float]
    payload_type: Literal['dict', 'list']
    key: str | None = None


def validate_numeric(flat_list: list) -> None:
    """Raises HTTPException if any value in the list is not int or float."""
    for val in flat_list:
        if not isinstance(val, (int, float)):
            raise HTTPException(
                status_code=400,
                detail="Values for calculation must be int or float"
            )


def normalize_list(userdata: UserData) -> list:
    """Extracts values from a list-type payload."""
    return userdata.vals


def normalize_dict(userdata: UserData) -> list:
    """Extracts numerical values from a dict-type payload using the provided key."""
    if not userdata.key:
        raise HTTPException(status_code=400, detail="Key not provided for dict")

    dict_keys = list(userdata.key in d.keys() for d in userdata.vals)
    if not all(dict_keys):
        raise HTTPException(
            status_code=400,
            detail="Key must be present in all list[dict] entries"
        )

    return [item[userdata.key] for item in userdata.vals]


def normalize_data(userdata: UserData) -> list:
    """
    Normalizes input data into a list of numerical values for stat calculations.
    :param userdata: UserData object
    :return: list of numerical values
    """
    if userdata.payload_type == 'list':
        flat_list = normalize_list(userdata)
    else:
        flat_list = normalize_dict(userdata)

    validate_numeric(flat_list)
    return flat_list


@app.post('/avg')
def avg(data: UserData) -> dict[str, float]:
    """ Calculates average value of input data """
    flat_data = normalize_data(data)
    return {'avg': stats.mean(flat_data)}


@app.post('/sum')
def total(data: UserData) -> dict[str, float]:
    """ Calculates sum total of input data """
    flat_data = normalize_data(data)
    return {'total': sum(flat_data)}


@app.post('/minmax')
def minmax(data: UserData) -> dict[str, Any]:
    """ Calculates min and max value of input data """
    flat_data = normalize_data(data)
    min_val = min(flat_data)
    max_val = max(flat_data)
    user_key = data.key

    # Handling for lists
    if not user_key:
        min_entries = min(flat_data)
        max_entries = max(flat_data)
    # Handling for dicts with provided key
    else:
        min_entries = [entry for entry in data.vals if entry[user_key] == min_val]
        max_entries = [entry for entry in data.vals if entry[user_key] == max_val]

    return {
        'key': data.key,
        'min': min_entries,
        'max': max_entries
    }


if __name__ == '__main__':
    test_data = UserData(vals=[{'name': 'rufus', 'age': 5}, {'name': 'todd', 'age': 6}, {'name': 'marx', 'age': 7}], payload_type='dict', key='age')
    print(normalize_data(test_data))
    print(avg(data=test_data))
    print(total(data=test_data))
    print(minmax(data=test_data))

    test_data = UserData(vals=[5, 6, 7], payload_type='list')
    print(normalize_data(test_data))
    print(avg(data=test_data))
    print(total(data=test_data))
    print(minmax(data=test_data))

    bad_data = UserData(vals=[{'name': 'rufus', 'age': 'uhoh'}, {'name': 'todd', 'age': 6}, {'name': 'marx', 'age': 7}], payload_type='dict', key='age')
