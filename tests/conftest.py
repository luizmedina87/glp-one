# tests/conftest.py
import pytest
from datetime import date
from src.models import DailyLog, UserLog

HISTORICAL_LOG_DATA = [
    (date(2026, 7, 3), 72.5, 1900),
    (date(2026, 7, 4), 72.5, 1900),
    (date(2026, 7, 5), 72.2, 1900),
    (date(2026, 7, 6), 72.0, 1900),
    (date(2026, 7, 7), 71.7, 1900),
    (date(2026, 7, 8), 71.6, 1900),
    (date(2026, 7, 9), 71.7, 1900),
    (date(2026, 7, 10), 71.6, 1900),
    (date(2026, 7, 11), 71.5, 1900),
    (date(2026, 7, 12), 71.9, 1900),
    (date(2026, 7, 13), 72.3, 1900),
    (date(2026, 7, 14), 71.8, 1900),
    (date(2026, 7, 15), 71.5, 1900),
    (date(2026, 7, 16), 71.1, 1900),
    (date(2026, 7, 17), 70.9, 1900),
    (date(2026, 7, 18), 70.8, 1900),
    (date(2026, 7, 19), 70.6, 1900),
    (date(2026, 7, 20), 70.7, 1900),
    (date(2026, 7, 21), 70.9, 1900),
    (date(2026, 7, 22), 70.9, 1900),
    (date(2026, 7, 23), 70.6, 1900),
    (date(2026, 7, 24), 70.6, 1900),
    (date(2026, 7, 25), 70.7, 1900),
    (date(2026, 7, 26), 70.5, 1900),
    (date(2026, 7, 27), 70.2, None),
    (date(2026, 7, 28), 71.0, 1900),
    (date(2026, 7, 29), 70.2, 1900),
    (date(2026, 7, 30), 70.1, 1900),
    (date(2026, 7, 31), 70.3, 1900),
    (date(2026, 8, 1), 70.3, 1900),
    (date(2026, 8, 2), 70.5, 1900),
    (date(2026, 8, 3), 70.5, 1900),
    (date(2026, 8, 4), 71.2, 1900),
    (date(2026, 8, 5), 70.7, 1900),
    (date(2026, 8, 6), 70.3, 1900),
    (date(2026, 8, 7), 70.8, 1900),
]


@pytest.fixture
def sample_tracker():
    """Provides a fully populated UserLog pre-loaded with historical data."""
    tracker = UserLog()
    for entry_date, weight, calories in HISTORICAL_LOG_DATA:
        tracker.log_entry(DailyLog(entry_date, weight, calories))
    return tracker