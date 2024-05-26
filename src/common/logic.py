from fastapi import HTTPException


def clear_none(data: dict) -> dict:
    after = {}

    for k, v in data.items():
        if v:
            after.update({k: v})

    if not after:
        raise HTTPException(400, "No data to update")

    return after
