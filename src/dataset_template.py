"""Helpers for loading dataset templates from disk."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from src.system_model import SystemModelParams


def dataset_templates_root(project_root: Path) -> Path:
    """Returns the dataset template root folder."""
    return project_root / "data" / "dataset_templates"


def load_dataset_template(project_root: Path, template_name: str) -> Dict[str, Any]:
    """Loads a dataset template by name from data/dataset_templates/<name>/template.json."""
    template_path = (
        dataset_templates_root(project_root) / template_name / "template.json"
    )
    if not template_path.exists():
        raise FileNotFoundError(
            f"Dataset template '{template_name}' not found at {template_path}"
        )
    with template_path.open("r", encoding="utf-8") as handle:
        template = json.load(handle)
    template["template_name"] = template_name
    template["template_path"] = str(template_path)
    return template


def build_system_model_params_from_template(template: Dict[str, Any]) -> SystemModelParams:
    """Builds SystemModelParams from a loaded dataset template."""
    params = SystemModelParams()
    system_model_config = template.get("system_model", {})
    for name, value in system_model_config.items():
        params.set_parameter(name, value)
    params.set_parameter("template_name", template.get("template_name"))
    return params
