import json

from datetime import date


class DailyLog:
    def __init__(self, entry_date: date, weight: float, calories: int):
        self.entry_date = entry_date
        self.weight = weight
        self.calories = calories

    def __repr__(self) -> str:
        return f"DailyLog(entry_date={self.entry_date}, weight={self.weight}, calories={self.calories})"

    def to_dict(self) -> dict:
        return {
            "entry_date": self.entry_date.isoformat(),
            "weight": self.weight,
            "calories": self.calories,
        }

    def to_json(self) -> json:
        return json.dumps(self.to_dict(), indent=2)




# Tests
test_date = date.today()
print(test_date)
test_dailylog = DailyLog(test_date, 73.0, 1900)
print(test_dailylog)
print(test_dailylog.to_dict())
print(test_dailylog.to_json())

