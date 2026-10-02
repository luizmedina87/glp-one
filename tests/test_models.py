import json

from src.models import DailyLog, LogTracker
from datetime import date


def test_log():
    test_date = date(2026, 10, 1)
    log = DailyLog(test_date, 72.5, 1900)
    assert log.weight == 72.5
    assert log.entry_date == test_date
    assert log.calories == 1900

def test_log_to_dict():
    test_date = date(2026, 10, 1)
    log = DailyLog(test_date, 72.5, 1900)
    assert log.to_dict() == {
        "entry_date": "2026-10-01",
        "weight": 72.5,
        "calories": 1900,
    }

def test_log_to_json():
    test_date = date(2026, 10, 1)
    log = DailyLog(test_date, 72.5, 1900)
    assert json.loads(log.to_json()) == {
        "entry_date": "2026-10-01",
        "weight": 72.5,
        "calories": 1900,
    }

