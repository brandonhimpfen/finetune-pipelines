from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from .config import load_recipe
from .pipeline import build_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="finetune-pipelines")
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan", help="Plan a fine-tuning pipeline run")
    plan_parser.add_argument("recipe", help="Path to YAML recipe")

    run_parser = subparsers.add_parser("run", help="Run a fine-tuning pipeline")
    run_parser.add_argument("recipe", help="Path to YAML recipe")
    run_parser.add_argument("--dry-run", action="store_true", help="Plan only, do not execute trainer")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    recipe = load_recipe(args.recipe)
    pipeline = build_pipeline(recipe)

    if args.command == "plan":
        plan = pipeline.plan()
        print(json.dumps(asdict(plan), indent=2))
        return

    if args.command == "run":
        result = pipeline.run(dry_run=args.dry_run)
        print(json.dumps(result, indent=2))
        return

    parser.error("Unknown command")
