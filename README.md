# GLP-One

GLP-One is a personal command-line app for tracking my daily weight and calorie
intake and estimating calorie targets as my weight changes. It is built for my
own diet management, not as a public health or nutrition service.

The app records daily entries, smooths weight and estimated total daily energy
expenditure (TDEE), and estimates calorie targets for cutting, maintaining, or
bulking. These are estimates for personal tracking, not medical advice.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/)

## Setup

From the project directory, install the project and its dependencies:

```bash
uv sync
```

Run the CLI with `uv run`:

```bash
uv run glp-one --help
```

## Daily use

Create a profile (the examples use `John`):

```bash
uv run glp-one user add John
```

Add or update a daily entry. Weight is the measurement for that date; calories
are the intake from the previous day:

```bash
uv run glp-one log upsert John --date 2026-10-14 --weight 75.2 --calories 1900
```

Recalculate the smoothed weight and TDEE, then view estimated calorie targets:

```bash
uv run glp-one user compute John
uv run glp-one user diet John
```

At least two daily log entries are needed for TDEE calculations and diet
estimates. View the profile's log entries and calculations with:

```bash
uv run glp-one user get John
```

## Commands

```text
glp-one user add <username>       Create a profile
glp-one user list                 List profiles
glp-one user get <username>      Display a profile's daily logs and calculations
glp-one user compute <username>  Recalculate smoothed weight and TDEE
glp-one user diet <username>     Show cut, maintain, and bulk calorie estimates
glp-one user rename <old> <new>  Rename a profile
glp-one user delete <username>   Delete a profile and its data
glp-one log upsert <username>    Add or update a daily log entry
glp-one log delete <username>    Delete a daily log entry by date
```

Use `--help` on the CLI or any command to see its arguments and options. For
example:

```bash
uv run glp-one log upsert --help
```

## Data and privacy

Profiles are stored as JSON files in `~/.glp_one/` on the local machine. Back up
that directory if you want to preserve or move your tracking history. The app
does not require an online account or remote service.
