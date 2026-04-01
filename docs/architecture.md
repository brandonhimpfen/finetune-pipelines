# Architecture

`finetune-pipelines` separates the workflow into five concerns.

## 1. Recipes

Recipes describe the run in YAML. They are portable, reviewable, and easy to version control.

## 2. Config loading

The config layer parses YAML and validates the required sections.

## 3. Dataset validation

The validation layer checks record structure based on pipeline type.

## 4. Pipeline planning and execution

The pipeline layer turns a recipe into an executable plan. In this starter repo, execution is stubbed so teams can wire in their preferred trainer later.

## 5. Artifacts

Each run writes a manifest and summary to support reproducibility and debugging.
