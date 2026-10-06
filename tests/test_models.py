import json

from datetime import date
from pathlib import Path
from src.models import DailyLog, UserLog, User
from src.glp_one.config import APP_NAME


def test_daily_log_initialization():
    test_date = date(2026, 10, 1)
    log = DailyLog(entry_date=test_date, weight_t=72.5, calories_tm1=1900)

    assert log.entry_date == test_date
    assert log.weight_t == 72.5
    assert log.calories_tm1 == 1900
    assert log.weight_smoothed_t is None


def test_daily_log_to_dict():
    test_date = date(2026, 10, 1)
    log = DailyLog(entry_date=test_date, weight_t=72.5, calories_tm1=1900)

    expected = {
        "entry_date": "2026-10-01",
        "calories_tm1": 1900,
        "weight_t": 72.5,
        "weight_smoothed_t": None,
        "tdee_t": None,
        "tdee_smoothed_t": None,
    }
    assert log.to_dict() == expected


def test_daily_log_to_json():
    test_date = date(2026, 10, 1)
    log = DailyLog(entry_date=test_date, weight_t=72.5, calories_tm1=1900)

    data = json.loads(log.to_json())
    assert data["entry_date"] == "2026-10-01"
    assert data["weight_t"] == 72.5
    assert data["calories_tm1"] == 1900
    assert data["weight_smoothed_t"] == None
    assert data["tdee_t"] == None
    assert data["tdee_smoothed_t"] == None


def test_sample_tracker_length(sample_tracker):
    # sample_tracker from conftest.py
    assert isinstance(sample_tracker, UserLog)
    assert len(sample_tracker.logs) == 36


def test_sample_tracker_chronological_order(sample_tracker):
    # Verifies sorting logic puts earliest date first
    assert sample_tracker.logs[0].entry_date == date(2026, 7, 3)
    assert sample_tracker.logs[-1].entry_date == date(2026, 8, 7)


def test_sample_tracker_missing_calories(sample_tracker):
    # Verifies July 27 entry handled None for calories correctly
    july_27_log = next(
        log for log in sample_tracker.logs if log.entry_date == date(2026, 7, 27)
    )
    assert july_27_log.entry_date == date(2026, 7, 27)
    assert july_27_log.weight_t == 70.2
    assert july_27_log.calories_tm1 == None
    assert july_27_log.weight_smoothed_t is None
    assert july_27_log.tdee_t == None
    assert july_27_log.tdee_smoothed_t == None


def test_user_log_to_dict(sample_tracker):
    dict_data = sample_tracker.to_dict()

    assert "logs" in dict_data
    assert len(dict_data["logs"]) == 36
    assert dict_data["logs"][0]["entry_date"] == "2026-07-03"


def test_user_log_to_json(sample_tracker):
    dict_data = json.loads(sample_tracker.to_json())

    assert "logs" in dict_data
    assert len(dict_data["logs"]) == 36
    assert dict_data["logs"][0]["entry_date"] == "2026-07-03"


def test_user_save(tmp_path, monkeypatch, sample_tracker):
    # Redirect Path.home() to pytest's temporary directory
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    user = User(user_name="test_user")
    user.user_log = sample_tracker
    user.save()

    expected_file = tmp_path / f".{APP_NAME}" / "test_user.json"
    assert expected_file.exists()

    file_content = json.loads(expected_file.read_text(encoding="utf-8"))
    assert "logs" in file_content
    assert len(file_content["logs"]) == 36
    assert file_content["logs"][0]["entry_date"] == "2026-07-03"


def test_daily_log_from_dict():
    data = {
        "entry_date": "2026-10-01",
        "weight_t": 72.5,
        "calories_tm1": 1900,
        "weight_smoothed_t": 72.3,
        "tdee_t": 2400.0,
        "tdee_smoothed_t": 2380.0,
    }
    log = DailyLog.from_dict(data)

    assert log.entry_date == date(2026, 10, 1)
    assert log.weight_t == 72.5
    assert log.calories_tm1 == 1900
    assert log.weight_smoothed_t == 72.3
    assert log.tdee_t == 2400.0
    assert log.tdee_smoothed_t == 2380.0


def test_daily_log_from_json():
    json_str = json.dumps({
        "entry_date": "2026-10-01",
        "weight_t": 72.5,
        "calories_tm1": 1900,
    })
    log = DailyLog.from_json(json_str)

    assert log.entry_date == date(2026, 10, 1)
    assert log.weight_t == 72.5
    assert log.calories_tm1 == 1900
    assert log.weight_smoothed_t is None


def test_user_log_from_dict():
    data = {
        "logs": [
            {"entry_date": "2026-10-02", "weight_t": 72.0, "calories_tm1": 1850},
            {"entry_date": "2026-10-01", "weight_t": 72.5, "calories_tm1": 1900},
        ]
    }
    user_log = UserLog.from_dict(data)

    assert len(user_log.logs) == 2
    assert isinstance(user_log.logs[0], DailyLog)
    assert user_log.logs[0].entry_date == date(2026, 10, 2)


def test_user_log_from_json():
    json_str = json.dumps({
        "logs": [
            {"entry_date": "2026-10-01", "weight_t": 72.5, "calories_tm1": 1900}
        ]
    })
    user_log = UserLog.from_json(json_str)

    assert len(user_log.logs) == 1
    assert user_log.logs[0].entry_date == date(2026, 10, 1)


def test_user_load_existing_file(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    user_dir = tmp_path / f".{APP_NAME}"
    user_dir.mkdir(parents=True, exist_ok=True)
    user_file = user_dir / "existing_user.json"

    user_file.write_text(
        json.dumps({
            "logs": [
                {"entry_date": "2026-10-01", "weight_t": 72.5, "calories_tm1": 1900}
            ]
        }),
        encoding="utf-8",
    )

    user = User(user_name="existing_user")
    user.load()

    assert len(user.user_log.logs) == 1
    assert user.user_log.logs[0].entry_date == date(2026, 10, 1)


def test_user_load_or_create_existing(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    user_dir = tmp_path / f".{APP_NAME}"
    user_dir.mkdir(parents=True, exist_ok=True)
    (user_dir / "test_user.json").write_text(
        json.dumps({"logs": [{"entry_date": "2026-10-01", "weight_t": 75.0, "calories_tm1": 2000}]}),
        encoding="utf-8",
    )

    user = User.load_or_create("test_user")

    assert user.user_name == "test_user"
    assert len(user.user_log.logs) == 1
    assert user.user_log.logs[0].weight_t == 75.0


def test_user_load_or_create_new(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    user = User.load_or_create("new_user")

    assert user.user_name == "new_user"
    assert len(user.user_log.logs) == 0


def test_user_log_find_log():
    log1 = DailyLog(entry_date=date(2026, 10, 1), weight_t=70.0, calories_tm1=2000)
    log2 = DailyLog(entry_date=date(2026, 10, 5), weight_t=70.5, calories_tm1=2100)
    user_log = UserLog(logs=[log1, log2])

    assert user_log.find_log(date(2026, 10, 1)) == 0
    assert user_log.find_log(date(2026, 10, 5)) == 1
    assert user_log.find_log(date(2026, 10, 10)) == -1


def test_user_log_get_entry():
    target_date = date(2026, 10, 1)
    log = DailyLog(entry_date=target_date, weight_t=70.0, calories_tm1=2000)
    user_log = UserLog(logs=[log])

    retrieved = user_log.get_entry(target_date)
    assert retrieved is not None
    assert retrieved.entry_date == target_date
    assert retrieved.weight_t == 70.0

    assert user_log.get_entry(date(2026, 10, 9)) is None


def test_user_log_upsert_entry_insert():
    user_log = UserLog(
        logs=[
            DailyLog(entry_date=date(2026, 10, 1), weight_t=70.0, calories_tm1=2000),
            DailyLog(entry_date=date(2026, 10, 3), weight_t=71.0, calories_tm1=2000),
        ]
    )

    # Insert a log out-of-order
    new_log = DailyLog(
        entry_date=date(2026, 10, 2), weight_t=70.5, calories_tm1=1950
    )
    user_log.upsert_entry(new_log)

    assert len(user_log.logs) == 3
    # Ensures sorting was triggered automatically
    assert user_log.logs[1].entry_date == date(2026, 10, 2)
    assert user_log.logs[1].weight_t == 70.5


def test_user_log_upsert_entry_update():
    target_date = date(2026, 10, 1)
    user_log = UserLog(
        logs=[
            DailyLog(entry_date=target_date, weight_t=70.0, calories_tm1=2000)
        ]
    )

    # Overwrite the entry for the same date
    updated_log = DailyLog(
        entry_date=target_date, weight_t=72.5, calories_tm1=2200
    )
    user_log.upsert_entry(updated_log)

    assert len(user_log.logs) == 1  # No duplicate created
    entry = user_log.get_entry(target_date)
    assert entry is not None
    assert entry.weight_t == 72.5
    assert entry.calories_tm1 == 2200


def test_user_log_delete_entry():
    target_date = date(2026, 10, 1)
    user_log = UserLog(
        logs=[
            DailyLog(entry_date=target_date, weight_t=70.0, calories_tm1=2000)
        ]
    )

    # Delete non-existent entry
    assert user_log.delete_entry(date(2026, 10, 9)) is False
    assert len(user_log.logs) == 1

    # Delete existing entry
    assert user_log.delete_entry(target_date) is True
    assert len(user_log.logs) == 0
    assert user_log.get_entry(target_date) is None


def test_user_get_data_path(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    path = User.get_data_path("test_user")
    assert path == tmp_path / f".{APP_NAME}" / "test_user.json"

    user = User("test_user")
    assert user.data_path == path


def test_user_rename(tmp_path, monkeypatch, sample_tracker):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    # Save initial user
    user = User(user_name="old_name", user_log=sample_tracker)
    user.save()

    old_file = User.get_data_path("old_name")
    new_file = User.get_data_path("new_name")

    assert old_file.exists()
    assert not new_file.exists()

    # Rename
    user.rename("new_name")

    assert user.user_name == "new_name"
    assert not old_file.exists()
    assert new_file.exists()

    # Verify content was preserved
    loaded_content = json.loads(new_file.read_text(encoding="utf-8"))
    assert len(loaded_content["logs"]) == len(sample_tracker.logs)