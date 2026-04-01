from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable


JsonDict = dict[str, object]


def read_jsonl(path: str | Path) -> list[JsonDict]:
    path = Path(path)
    records: list[JsonDict] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                obj = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Invalid JSON on line {line_number} in {path}") from exc
            if not isinstance(obj, dict):
                raise ValueError(f"Expected object on line {line_number} in {path}")
            records.append(obj)
    return records


def write_json(path: str | Path, data: object) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")


def write_text(path: str | Path, text: str) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def count_records(records: Iterable[JsonDict]) -> int:
    return sum(1 for _ in records)
