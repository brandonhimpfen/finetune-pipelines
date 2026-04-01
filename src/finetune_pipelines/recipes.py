from __future__ import annotations

from pathlib import Path

import yaml


def save_recipe(path: str | Path, recipe: dict[str, object]) -> None:
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(recipe, handle, sort_keys=False)
