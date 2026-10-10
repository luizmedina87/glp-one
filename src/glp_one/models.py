from __future__ import annotations

import json

from datetime import date
from pathlib import Path
from glp_one.config import get_data_dir


class DailyLog:
    def __init__(
            self, 
            entry_date: date, 
            weight_t: float | None, 
            calories_tm1: int | None,
            weight_smoothed_t: float | None = None,
            tdee_t: float | None = None,
            tdee_smoothed_t: float | None = None
        ):
        if isinstance(entry_date, str):
            self.entry_date: date = date.fromisoformat(entry_date)
        else:
            self.entry_date: date = entry_date
        self.weight_t: float | None = weight_t
        self.calories_tm1: int | None = calories_tm1 # input in t. You only know how many calories you consumed the next day.
        self.weight_smoothed_t: float | None = weight_smoothed_t # calculate in t
        self.tdee_t: float | None = tdee_t # calculate in t+1
        self.tdee_smoothed_t: float | None = tdee_smoothed_t # calculate in t+1

    def __repr__(self) -> str:
        attributes = ",\n ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"DailyLog(\n {attributes}\n)"
    
    @classmethod
    def from_dict(cls, data: dict) -> DailyLog:
        return cls(
            entry_date=data["entry_date"],
            weight_t=data.get("weight_t"),
            calories_tm1=data.get("calories_tm1"),
            weight_smoothed_t=data.get("weight_smoothed_t"),
            tdee_t=data.get("tdee_t"),
            tdee_smoothed_t=data.get("tdee_smoothed_t")
        )

    @classmethod
    def from_json(cls, json_str: str) -> DailyLog:
        data_dict = json.loads(json_str)
        return cls.from_dict(data_dict)
    
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



class UserLog:
    def __init__(self, logs: list[DailyLog] | None = None):
        self.logs: list[DailyLog] = logs if logs is not None else []

    def __repr__(self) -> str:
        return f"LogTracker({self.logs})"

    @classmethod
    def from_dict(cls, data: dict) -> UserLog:
        log_entries = [DailyLog.from_dict(item) for item in data.get("logs", [])]
        return cls(logs=log_entries)

    @classmethod
    def from_json(cls, json_str: str) -> UserLog:
        data_dict = json.loads(json_str)
        return cls.from_dict(data_dict)
    
    def log_entry(self, daily_log: DailyLog) -> None:
        self.logs.append(daily_log)
        self.sort()

    def sort(self) -> None:
        self.logs.sort(key=lambda entry: entry.entry_date)

    def find_log(self, entry_date: date) -> int:
        for idx, log in enumerate(self.logs):
            if log.entry_date == entry_date:
                return idx
        return -1

    def get_entry(self, entry_date: date) -> DailyLog | None:
        idx = self.find_log(entry_date)
        return None if idx == -1 else self.logs[idx]

    def upsert_entry(self, new_log: DailyLog) -> None:
        idx = self.find_log(new_log.entry_date)
        if idx != -1:
            self.logs[idx] = new_log
        else:
            self.log_entry(new_log)

    def delete_entry(self, entry_date: date) -> bool:
        if isinstance(entry_date, str):
                entry_date = date.fromisoformat(entry_date)
        idx = self.find_log(entry_date)
        if idx != -1:
            del self.logs[idx]
            return True
        return False

    def to_dict(self) -> dict:
        return {"logs": [log.to_dict() for log in self.logs]}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


class User:
    def __init__(self, user_name: str, user_log: UserLog | None = None):
        self.user_name: str = user_name
        self.user_log: UserLog = UserLog() if user_log is None else user_log

    @property
    def data_path(self) -> Path:
        return User.get_data_path(self.user_name)
    
    @classmethod
    def get_data_path(cls, user_name: str) -> Path:
        return get_data_dir() / f"{user_name}.json"
        
    @classmethod
    def load_or_create(cls, user_name: str) -> User:
        user = cls(user_name=user_name)
        user.load()
        return user

    def exists(self) -> bool:
        return self.data_path.exists()
    
    def save(self) -> None:
        self.data_path.write_text(self.user_log.to_json(), encoding="utf-8")

    def load(self) -> None:
        if self.exists():
            json_str = self.data_path.read_text(encoding="utf-8")
            self.user_log = UserLog.from_json(json_str)

    def rename(self, new_name: str) -> None:
        old_path = self.data_path
        self.user_name = new_name
        if old_path.exists():
            self.save()
            old_path.unlink()

    def delete(self) -> None:
        if self.exists():
            self.data_path.unlink()

    def update(self) -> None:
        ...