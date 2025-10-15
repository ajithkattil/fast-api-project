import uuid
from datetime import datetime


def is_valid_uuid(val: str) -> bool:
    try:
        uuid_obj = uuid.UUID(val)
        return str(uuid_obj) == val.lower()
    except ValueError:
        return False


def validate_cycle_date(cycle_date: str) -> str:
    try:
        parsed_date = datetime.strptime(cycle_date, "%Y-%m-%d")

        if parsed_date.weekday() != 0:
            raise ValueError(f"Cycle date {cycle_date} must be a Monday")

        return cycle_date
    except ValueError as e:
        if "must be a Monday" in str(e):
            raise ValueError(str(e)) from None
        else:
            raise ValueError(f"Invalid cycle date format: {cycle_date}. Expected format: YYYY-MM-DD") from None


def validate_cycle_datetime(cycle_datetime: datetime) -> bool:
    return cycle_datetime.weekday() == 0
