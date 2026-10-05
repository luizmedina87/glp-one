import json

from datetime import date


class DailyLog:
    def __init__(self, entry_date: date, weight_t: float | None, calories_tm1: int | None):
        self.entry_date = entry_date
        self.calories_tm1 = calories_tm1 # input in t. You only know how many calories you consumed the next day.
        self.weight_t = weight_t
        self.weight_smoothed_t = None # calculate in t
        self.tdee_t = None # calculate in t+1
        self.tdee_smoothed_t = None # calculate in t+1

    def __repr__(self) -> str:
        attributes = ",\n ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"DailyLog(\n {attributes}\n)"
    
    def to_dict(self) -> dict:
        return {
            "entry_date": self.entry_date.isoformat(),
            "weight_t": self.weight_t,
            "calories_tm1": self.calories_tm1,
            "weight_smoothed_t": self.weight_smoothed_t,
            "tdee_t": self.tdee_t,
            "tdee_smoothed_t": self.tdee_smoothed_t,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class User:
    def __init__(self, user_name: str):
        self.user_name: str = user_name
        self.user_log: UserLog = UserLog()


class UserLog:
    def __init__(self):
        self.logs: list[UserLog] = []

    def __repr__(self) -> str:
        return f"LogTracker({self.logs})"

    def log_entry(self, daily_log: DailyLog) -> None:
        self.logs.append(daily_log)
        self.sort()

    def sort(self) -> None:
        self.logs.sort(key=lambda entry: entry.entry_date)

    def to_dict(self) -> dict:
        return {"logs": [log.to_dict() for log in self.logs]}
