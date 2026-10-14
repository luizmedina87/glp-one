from __future__ import annotations

import json

from datetime import date, timedelta
from pathlib import Path
from glp_one.config import (
    get_data_dir, 
    WEIGHT_MULTIPLIER, 
    CALORIES_PER_KILOGRAM,
    DEFAULT_MAX_DEFICIT,
    DEFAULT_MAX_SURPLUS,
    WEIGHT_DECAY,
    TDEE_DECAY,
    WEEKLY_BULK_SPEED,
    WEEKLY_CUT_SPEED
    )


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

    def next_day(self) -> timedelta:
        return self.entry_date + timedelta(days=1)

    def prev_day(self) -> timedelta:
        return self.entry_date - timedelta(days=1)



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
        self.fill_gap(daily_log)

    def fill_gap(
            self, 
            daily_log: DailyLog, 
            weight_mult: int = WEIGHT_MULTIPLIER,
            cal_per_kg: int = CALORIES_PER_KILOGRAM,
            def_max_def: int = DEFAULT_MAX_DEFICIT,
            def_max_surp: int = DEFAULT_MAX_SURPLUS
            ) -> None:
        idx = self.find_log(daily_log.entry_date)

        if idx != 0:
            prev_log = self.logs[idx - 1]
            delta = daily_log.entry_date - prev_log.entry_date

            for i in range(1, delta.days):
                new_date = prev_log.entry_date + timedelta(days=i)

                if daily_log.weight_t:
                    weight_diff = (daily_log.weight_t - prev_log.weight_t) / delta.days
                    new_weight = round(prev_log.weight_t + weight_diff * i, 1)
                    kcal_diff = weight_diff * cal_per_kg
                    capped_kcal_diff = max(def_max_def, min(def_max_surp, kcal_diff))
                    new_kcal = int(new_weight * weight_mult + capped_kcal_diff)
                else:
                    new_weight = None
                    new_kcal = None

                new_log = DailyLog(
                    entry_date = new_date, 
                    weight_t = new_weight,
                    calories_tm1 = new_kcal
                    )
                self.log_entry(new_log)
                
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

    def compute(self) -> str:
        if len(self.logs) < 2:
            return # You need at least two days of logs to compute TDEE and EWMA
        initial_log = self.logs[0]
        initial_log.weight_smoothed_t = initial_log.weight_t
        initial_log.tdee_smoothed_t = initial_log.weight_t * WEIGHT_MULTIPLIER
        for i, log in enumerate(self.logs[1:], start=1):
            prev_log = self.logs[i - 1]
            log.weight_smoothed_t = round(log.weight_t * WEIGHT_DECAY + prev_log.weight_smoothed_t * (1 - WEIGHT_DECAY), 1)
            delta_weight = log.weight_smoothed_t - prev_log.weight_smoothed_t
            log.tdee_t = int(log.calories_tm1 - delta_weight * CALORIES_PER_KILOGRAM)
            log.tdee_smoothed_t = int(log.tdee_t * TDEE_DECAY + prev_log.tdee_smoothed_t * (1 - TDEE_DECAY))

    
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
        if self.user_log:
            self.user_log.compute()
            self.save()

    def calculate_goal(self) -> int:
        last_entry: DailyLog = self.user_log.logs[-1]
        last_tdee: int = last_entry.tdee_smoothed_t
        daily_cut_speed = WEEKLY_CUT_SPEED / 7
        daily_bulk_speed = WEEKLY_BULK_SPEED / 7
        bodly_kcal = last_entry.weight_smoothed_t * CALORIES_PER_KILOGRAM
        cut = last_tdee - bodly_kcal * daily_cut_speed
        maintain = last_tdee
        bulk = last_tdee + bodly_kcal * daily_bulk_speed
        return cut, maintain, bulk