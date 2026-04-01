from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .artifacts import write_run_artifacts
from .config import RecipeConfig
from .io import read_jsonl
from .validators import ValidationReport, validate_records


@dataclass(slots=True)
class PipelinePlan:
    pipeline_name: str
    pipeline_type: str
    train_file: str
    output_dir: str
    record_count: int
    valid: bool
    issues: list[str]
    planned_steps: list[str]


class BasePipeline:
    def __init__(self, recipe: RecipeConfig) -> None:
        self.recipe = recipe

    def load_records(self) -> list[dict[str, object]]:
        train_path = Path(self.recipe.paths.train_file)
        return read_jsonl(train_path)

    def validate(self, records: list[dict[str, object]]) -> ValidationReport:
        return validate_records(records, self.recipe.pipeline.type)

    def planned_steps(self) -> list[str]:
        return [
            "load recipe",
            "read dataset",
            "validate records",
            "prepare trainer config",
            "write manifest",
            "simulate trainer execution",
        ]

    def plan(self) -> PipelinePlan:
        records = self.load_records()
        report = self.validate(records)
        return PipelinePlan(
            pipeline_name=self.recipe.pipeline.name,
            pipeline_type=self.recipe.pipeline.type,
            train_file=self.recipe.paths.train_file,
            output_dir=self.recipe.paths.output_dir,
            record_count=report.record_count,
            valid=report.valid,
            issues=report.issues,
            planned_steps=self.planned_steps(),
        )

    def run(self, dry_run: bool = False) -> dict[str, object]:
        records = self.load_records()
        report = self.validate(records)

        if not report.valid:
            execution = {
                "dry_run": dry_run,
                "planned_steps": self.planned_steps(),
                "status": "failed_validation",
            }
            write_run_artifacts(self.recipe.output_dir, self.recipe, report, execution)
            return execution

        execution = {
            "dry_run": dry_run,
            "planned_steps": self.planned_steps(),
            "status": "planned_only" if dry_run else "completed_stub_run",
        }
        write_run_artifacts(self.recipe.output_dir, self.recipe, report, execution)
        return execution


class SFTPipeline(BasePipeline):
    pass


class DPOPipeline(BasePipeline):
    def planned_steps(self) -> list[str]:
        return [
            "load recipe",
            "read preference dataset",
            "validate prompt/chosen/rejected records",
            "prepare preference trainer config",
            "write manifest",
            "simulate trainer execution",
        ]


def build_pipeline(recipe: RecipeConfig) -> BasePipeline:
    if recipe.pipeline.type == "sft":
        return SFTPipeline(recipe)
    if recipe.pipeline.type == "dpo":
        return DPOPipeline(recipe)
    raise ValueError(f"Unsupported pipeline type: {recipe.pipeline.type}")
