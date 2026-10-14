import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from glp_one.config import APP_NAME
from glp_one.main import app


@pytest.fixture
def cli_runner(tmp_path, monkeypatch):
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    return CliRunner()


def test_help_lists_user_and_log_commands(cli_runner):
    result = cli_runner.invoke(app, ["--help"])

    assert result.exit_code == 0
    assert "user" in result.output
    assert "log" in result.output


def test_user_profile_lifecycle(cli_runner, tmp_path):
    user_file = tmp_path / f".{APP_NAME}" / "Ada.json"

    result = cli_runner.invoke(app, ["user", "add", "Ada"])
    assert result.exit_code == 0
    assert "Ada saved" in result.output
    assert user_file.exists()

    result = cli_runner.invoke(app, ["user", "add", "Ada"])
    assert result.exit_code == 0
    assert "Ada already exists" in result.output

    result = cli_runner.invoke(app, ["user", "rename", "Ada", "Grace"])
    assert result.exit_code == 0
    assert "Ada was renamed to Grace" in result.output
    assert not user_file.exists()
    assert (user_file.parent / "Grace.json").exists()

    result = cli_runner.invoke(app, ["user", "list"])
    assert result.exit_code == 0
    assert "Grace" in result.output
    assert "Ada" not in result.output

    result = cli_runner.invoke(app, ["user", "delete", "Grace"])
    assert result.exit_code == 0
    assert "Grace deleted" in result.output
    assert not (user_file.parent / "Grace.json").exists()


def test_log_upsert_get_and_delete(cli_runner, tmp_path):
    user_file = tmp_path / f".{APP_NAME}" / "Ada.json"

    assert cli_runner.invoke(app, ["user", "add", "Ada"]).exit_code == 0

    result = cli_runner.invoke(
        app,
        [
            "log",
            "upsert",
            "Ada",
            "--date",
            "2026-10-13",
            "--weight",
            "75.2",
            "--calories",
            "1900",
        ],
    )
    assert result.exit_code == 0
    assert "Upserted entry for Ada" in result.output
    saved_logs = json.loads(user_file.read_text(encoding="utf-8"))["logs"]
    assert saved_logs[0]["entry_date"] == "2026-10-13"
    assert saved_logs[0]["weight_t"] == 75.2
    assert saved_logs[0]["calories_tm1"] == 1900

    result = cli_runner.invoke(app, ["user", "get", "Ada"])
    assert result.exit_code == 0
    assert "2026-10-13" in result.output
    assert "75.2" in result.output

    result = cli_runner.invoke(
        app, ["log", "delete", "Ada", "--date", "2026-10-13"]
    )
    assert result.exit_code == 0
    assert "Deleted entry for Ada" in result.output
    assert json.loads(user_file.read_text(encoding="utf-8"))["logs"] == []


def test_compute_and_diet_use_requested_profile(cli_runner, tmp_path):
    user_file = tmp_path / f".{APP_NAME}" / "Ada.json"
    assert cli_runner.invoke(app, ["user", "add", "Ada"]).exit_code == 0

    for entry_date, weight, calories in (
        ("2026-10-13", "75.2", "1900"),
        ("2026-10-14", "75.0", "2000"),
    ):
        result = cli_runner.invoke(
            app,
            [
                "log",
                "upsert",
                "Ada",
                "--date",
                entry_date,
                "--weight",
                weight,
                "--calories",
                calories,
            ],
        )
        assert result.exit_code == 0

    result = cli_runner.invoke(app, ["user", "compute", "Ada"])
    assert result.exit_code == 0
    assert "Recalculated Ada" in result.output

    logs = json.loads(user_file.read_text(encoding="utf-8"))["logs"]
    assert logs[-1]["weight_smoothed_t"] is not None
    assert logs[-1]["tdee_smoothed_t"] is not None

    result = cli_runner.invoke(app, ["user", "diet", "Ada"])
    assert result.exit_code == 0
    assert "Cut:" in result.output
    assert "Maintain:" in result.output
    assert "Bulk:" in result.output


def test_log_upsert_reports_missing_profile(cli_runner):
    result = cli_runner.invoke(
        app,
        [
            "log",
            "upsert",
            "Missing",
            "--date",
            "2026-10-14",
            "--weight",
            "75.2",
            "--calories",
            "1900",
        ],
    )

    assert result.exit_code == 0
    assert "Missing doesn't exist. Upsert canceled." in result.output


def test_diet_requires_at_least_two_entries(cli_runner):
    assert cli_runner.invoke(app, ["user", "add", "Ada"]).exit_code == 0

    result = cli_runner.invoke(app, ["user", "diet", "Ada"])

    assert result.exit_code == 0
    assert "Not enough data." in result.output
