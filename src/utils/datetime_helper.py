from datetime import UTC, datetime

UTC_MIN = datetime.min.replace(tzinfo=UTC)

UTC_MAX = datetime.max.replace(tzinfo=UTC)


def parse_to_datetime(date: str) -> datetime:
    return datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=UTC)


def parse_from_datetime(date: datetime) -> str:
    return date.astimezone(UTC).strftime("%Y-%m-%d")
