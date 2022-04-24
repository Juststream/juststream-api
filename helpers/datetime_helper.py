from datetime import datetime, timedelta


def get_time_after(days, hours, minutes):
    return datetime.utcnow() + timedelta(days=days, hours=hours, minutes=minutes)


def get_current_timestamp():
    return str(datetime.utcnow().timestamp())


def get_hours_before_timestamp(timestamp: str, hours: int) -> str:
    return str((datetime.fromtimestamp(float(timestamp)) - timedelta(hours=hours)).timestamp())


def get_hours_after_timestamp(timestamp: str, hours: int) -> str:
    return str((datetime.fromtimestamp(float(timestamp)) + timedelta(hours=hours)).timestamp())
