from .models import CV
import yaml
import os


def load_cv_data(config_path: str = "cv_data.yaml") -> CV:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return CV(**data)
