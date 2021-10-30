from datetime import datetime, timedelta


def get_current_timestamp():
    return str(datetime.utcnow().timestamp())


def get_hours_before_timestamp(timestamp: str, hours: int) -> str:
    return str((datetime.fromtimestamp(float(timestamp)) - timedelta(hours=hours)).timestamp())


def get_hours_after_timestamp(timestamp: str, hours: int) -> str:
    return str((datetime.fromtimestamp(float(timestamp)) + timedelta(hours=hours)).timestamp())
