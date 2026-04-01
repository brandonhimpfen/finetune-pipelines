#!/usr/bin/env bash
set -euo pipefail

python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
finetune-pipelines plan recipes/sft/tiny-sft.yaml
finetune-pipelines run recipes/sft/tiny-sft.yaml --dry-run
