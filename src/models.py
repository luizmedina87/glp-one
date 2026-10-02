import json

from datetime import date, timedelta


class DailyLog:
    def __init__(self, entry_date: date, calories_tm1: int | None, weight_t: float | None):
        self.entry_date = entry_date
        self.calories_tm1 = calories_tm1 # input in t. You only know how many calories you consumed the next day.
        self.weight_t = weight_t
        self.weight_smoothed_t = None # calculate in t
        self.tdee_t = None # calculate in t+1
        self.tdee_smoothed_t = None # calculate in t+1

    def __repr__(self) -> str:
        return f"DailyLog(entry_date={self.entry_date}, weight_t={self.weight_t}, weight_smoothed_t={self.weight_smoothed_t}, calories_tm1={self.calories_tm1}, tdee_t={self.tdee_t}, tdee_smoothed_t={self.tdee_smoothed_t})"

    def to_dict(self) -> dict:
        return {
            "entry_date": self.entry_date.isoformat(),
            "weight": self.weight,
            "calories": self.calories,
        }

    def to_json(self) -> json:
        return json.dumps(self.to_dict(), indent=2)


class LogTracker:
    def __init__(self):
        self.logs = []

    def __repr__(self) -> str:
        return f"LogTracker({self.logs})"

    def log_entry(self, daily_log: DailyLog) -> None:
        self.logs.append(daily_log)
        self.sort()

    def sort(self):
        self.logs.sort(key=lambda entry: entry.entry_date)


# Tests
# date
test_date = date.today()
print(test_date)
test_dailylog = DailyLog(test_date, 73.0, 1900)
test_dailylog2 = DailyLog(test_date + timedelta(days=1), 73.0, 1900)
print(test_dailylog)
print(test_dailylog.to_dict())
print(test_dailylog.to_json())
# tracker
track = LogTracker()
test_date = date.today()
print(test_date)
test_dailylog = DailyLog(test_date, 73.0, 1900)
print(test_dailylog)
print(test_dailylog.to_dict())
print(test_dailylog.to_json())
track.log_entry(test_dailylog)
track.log_entry(test_dailylog2)
print(track)

# from datetime import date
# from models import DailyLog

# # Sample year set to 2026
# raw_logs = [
#     (date(2026, 7, 3), 72.5, 1900),
#     (date(2026, 7, 4), 72.5, 1900),
#     (date(2026, 7, 5), 72.2, 1900),
#     (date(2026, 7, 6), 72.0, 1900),
#     (date(2026, 7, 7), 71.7, 1900),
#     (date(2026, 7, 8), 71.6, 1900),
#     (date(2026, 7, 9), 71.7, 1900),
#     (date(2026, 7, 10), 71.6, 1900),
#     (date(2026, 7, 11), 71.5, 1900),
#     (date(2026, 7, 12), 71.9, 1900),
#     (date(2026, 7, 13), 72.3, 1900),
#     (date(2026, 7, 14), 71.8, 1900),
#     (date(2026, 7, 15), 71.5, 1900),
#     (date(2026, 7, 16), 71.1, 1900),
#     (date(2026, 7, 17), 70.9, 1900),
#     (date(2026, 7, 18), 70.8, 1900),
#     (date(2026, 7, 19), 70.6, 1900),
#     (date(2026, 7, 20), 70.7, 1900),
#     (date(2026, 7, 21), 70.9, 1900),
#     (date(2026, 7, 22), 70.9, 1900),
#     (date(2026, 7, 23), 70.6, 1900),
#     (date(2026, 7, 24), 70.6, 1900),
#     (date(2026, 7, 25), 70.7, 1900),
#     (date(2026, 7, 26), 70.5, 1900),
#     (date(2026, 7, 27), 70.2, 1900),  # Calorie entry missing in raw string
#     (date(2026, 7, 28), 71.0, 1900),
#     (date(2026, 7, 29), 70.2, 1900),
#     (date(2026, 7, 30), 70.1, 1900),
#     (date(2026, 7, 31), 70.3, 1900),
#     (date(2026, 8, 1), 70.3, 1900),
#     (date(2026, 8, 2), 70.5, 1900),
#     (date(2026, 8, 3), 70.5, 1900),
#     (date(2026, 8, 4), 71.2, 1900),
#     (date(2026, 8, 5), 70.7, 1900),
#     (date(2026, 8, 6), 70.3, 1900),
#     (date(2026, 8, 7), 70.8, 1900),
# ]

# # Instantiate tracker and populate
# track = LogTracker()

# for entry_date, weight, calories in raw_logs:
#     track.log_entry(DailyLog(entry_date, weight, calories))

# print(f"Logged {len(track.logs)} entries successfully.")
