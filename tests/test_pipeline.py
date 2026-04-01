from finetune_pipelines.config import load_recipe
from finetune_pipelines.pipeline import build_pipeline


def test_plan_pipeline() -> None:
    recipe = load_recipe("recipes/sft/tiny-sft.yaml")
    pipeline = build_pipeline(recipe)
    plan = pipeline.plan()
    assert plan.pipeline_type == "sft"
    assert plan.record_count == 2
    assert plan.valid is True
