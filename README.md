# finetune-pipelines

[![GitHub Sponsor](https://srv-cdn.himpfen.io/badges/github/github-flat.svg)](https://github.com/sponsors/brandonhimpfen) &nbsp; 
[![Buy Me a Coffee](https://srv-cdn.himpfen.io/badges/buymeacoffee/buymeacoffee-flat.svg)](https://buymeacoffee.com/brandonhimpfen) &nbsp; 
[![Ko-Fi](https://srv-cdn.himpfen.io/badges/kofi/kofi-flat.svg)](https://ko-fi.com/brandonhimpfen) &nbsp; 
[![PayPal](https://srv-cdn.himpfen.io/badges/paypal/paypal-flat.svg)](https://paypal.me/brandonhimpfen)

Fine-tuning pipelines and recipes for practical LLM training workflows in Python.

`finetune-pipelines` provides a lightweight, extensible structure for building, validating, and running fine-tuning jobs. It is designed as a reusable starting point for teams who want clear configuration, repeatable dataset preparation, and simple recipe-driven execution without locking themselves into a single stack too early.

The project currently focuses on:

- Supervised fine-tuning (SFT) pipeline structure.
- Preference-style dataset validation and DPO-ready formatting.
- Recipe-based runs using YAML configuration.
- Dry-run planning and artifact generation.
- Reproducible output directories with manifests and summaries.

This repo is intentionally conservative. It aims to be understandable, hackable, and easy to adapt.

## Features

- Clean Python package layout under `src/`.
- YAML recipes for SFT and DPO-style workflows.
- Dataset normalization and validation utilities.
- CLI for planning and running jobs.
- Artifact manifests for traceability.
- Small test suite to validate core behavior.
- Example datasets and configs.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Quick start

Plan an SFT run:

```bash
finetune-pipelines plan recipes/sft/tiny-sft.yaml
```

Execute a dry run:

```bash
finetune-pipelines run recipes/sft/tiny-sft.yaml --dry-run
```

Execute a run and write artifacts:

```bash
finetune-pipelines run recipes/sft/tiny-sft.yaml
```

## Project structure

```text
finetune-pipelines/
├── docs/
├── examples/
├── recipes/
│   ├── dpo/
│   └── sft/
├── scripts/
├── src/finetune_pipelines/
└── tests/
```

## Recipes

A recipe defines the dataset, model metadata, trainer settings, output location, and pipeline type.

Supported `pipeline.type` values in this starter repo:

- `sft`
- `dpo`

Example:

```yaml
pipeline:
  type: sft
  name: tiny-sft

model:
  base_model: mistralai/Mistral-7B-v0.1

paths:
  train_file: examples/data/sft_train.jsonl
  output_dir: outputs/tiny-sft
```

## Scope

This starter focuses on workflow structure rather than full GPU trainer integrations. In its current form, it validates inputs, plans jobs, prepares standardized artifacts, and simulates trainer execution. It is meant to be extended with:

- Hugging Face Transformers + TRL.
- Axolotl or Unsloth integration.
- PEFT / LoRA adapters.
- Dataset versioning and storage backends.
- Experiment tracking.

## Development

Run tests:

```bash
pytest
```

Format and lint:

```bash
ruff check .
ruff format .
```

## License

MIT
