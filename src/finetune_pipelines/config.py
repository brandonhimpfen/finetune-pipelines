from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(slots=True)
class PipelineSection:
    type: str
    name: str
    description: str = ""


@dataclass(slots=True)
class ModelSection:
    base_model: str
    tokenizer: str | None = None
    revision: str | None = None
    trust_remote_code: bool = False


@dataclass(slots=True)
class PathsSection:
    train_file: str
    eval_file: str | None = None
    output_dir: str = "outputs/default"


@dataclass(slots=True)
class TrainerSection:
    epochs: int = 1
    batch_size: int = 1
    learning_rate: float = 2e-5
    gradient_accumulation_steps: int = 1
    max_seq_length: int = 2048
    warmup_ratio: float = 0.03
    log_every: int = 10
    save_every: int = 100
    seed: int = 42
    extras: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RecipeConfig:
    pipeline: PipelineSection
    model: ModelSection
    paths: PathsSection
    trainer: TrainerSection
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def output_dir(self) -> Path:
        return Path(self.paths.output_dir)


class RecipeError(ValueError):
    """Raised when a recipe is invalid."""


REQUIRED_TOP_LEVEL_KEYS = {"pipeline", "model", "paths"}
SUPPORTED_PIPELINES = {"sft", "dpo"}


def _validate_top_level(data: dict[str, Any]) -> None:
    missing = REQUIRED_TOP_LEVEL_KEYS - set(data.keys())
    if missing:
        raise RecipeError(f"Recipe missing required sections: {sorted(missing)}")

    pipeline_type = data["pipeline"].get("type")
    if pipeline_type not in SUPPORTED_PIPELINES:
        raise RecipeError(
            f"Unsupported pipeline.type '{pipeline_type}'. Supported: {sorted(SUPPORTED_PIPELINES)}"
        )


def load_recipe(recipe_path: str | Path) -> RecipeConfig:
    path = Path(recipe_path)
    if not path.exists():
        raise FileNotFoundError(f"Recipe not found: {path}")

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    if not isinstance(data, dict):
        raise RecipeError("Recipe must parse to a mapping/object.")

    _validate_top_level(data)

    trainer_data = data.get("trainer", {}) or {}
    known_trainer_keys = {
        "epochs",
        "batch_size",
        "learning_rate",
        "gradient_accumulation_steps",
        "max_seq_length",
        "warmup_ratio",
        "log_every",
        "save_every",
        "seed",
    }
    extras = {k: v for k, v in trainer_data.items() if k not in known_trainer_keys}

    return RecipeConfig(
        pipeline=PipelineSection(**data["pipeline"]),
        model=ModelSection(**data["model"]),
        paths=PathsSection(**data["paths"]),
        trainer=TrainerSection(
            epochs=trainer_data.get("epochs", 1),
            batch_size=trainer_data.get("batch_size", 1),
            learning_rate=trainer_data.get("learning_rate", 2e-5),
            gradient_accumulation_steps=trainer_data.get("gradient_accumulation_steps", 1),
            max_seq_length=trainer_data.get("max_seq_length", 2048),
            warmup_ratio=trainer_data.get("warmup_ratio", 0.03),
            log_every=trainer_data.get("log_every", 10),
            save_every=trainer_data.get("save_every", 100),
            seed=trainer_data.get("seed", 42),
            extras=extras,
        ),
        metadata=data.get("metadata", {}) or {},
    )
