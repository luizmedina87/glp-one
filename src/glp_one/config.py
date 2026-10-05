from pathlib import Path


# Application Metadata
APP_NAME = "glp_one"

# Paths
def get_data_dir() -> Path:
    """Returns the data directory, creating it if non-existent."""
    data_dir = Path.home() / f".{APP_NAME}"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir