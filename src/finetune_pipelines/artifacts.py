from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .config import RecipeConfig
from .io import write_json, write_text
from .validators import ValidationReport


def write_run_artifacts(
    output_dir: str | Path,
    recipe: RecipeConfig,
    report: ValidationReport,
    execution: dict[str, Any],
) -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    manifest = {
        "generated_at": datetime.now(UTC).isoformat(),
        "recipe": {
            "pipeline": asdict(recipe.pipeline),
            "model": asdict(recipe.model),
            "paths": asdict(recipe.paths),
            "trainer": asdict(recipe.trainer),
            "metadata": recipe.metadata,
        },
        "validation": asdict(report),
        "execution": execution,
    }

    write_json(output_path / "manifest.json", manifest)

    summary = _build_summary(recipe, report, execution)
    write_text(output_path / "SUMMARY.md", summary)


def _build_summary(recipe: RecipeConfig, report: ValidationReport, execution: dict[str, Any]) -> str:
    return f"""# Run Summary

## Pipeline

- Name: {recipe.pipeline.name}
- Type: {recipe.pipeline.type}
- Base model: {recipe.model.base_model}
- Output dir: {recipe.paths.output_dir}

## Dataset

- Train file: {recipe.paths.train_file}
- Eval file: {recipe.paths.eval_file or 'None'}
- Record count: {report.record_count}
- Validation: {'passed' if report.valid else 'failed'}

## Execution

- Dry run: {execution.get('dry_run')}
- Planned steps: {execution.get('planned_steps')}
- Status: {execution.get('status')}

## Notes

This starter repo writes planning and run artifacts, but does not yet launch a full trainer backend.
"""
