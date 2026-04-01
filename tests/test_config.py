from finetune_pipelines.config import load_recipe


def test_load_recipe() -> None:
    recipe = load_recipe("recipes/sft/tiny-sft.yaml")
    assert recipe.pipeline.type == "sft"
    assert recipe.pipeline.name == "tiny-sft"
    assert recipe.model.base_model == "mistralai/Mistral-7B-v0.1"
