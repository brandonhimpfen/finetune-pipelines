from finetune_pipelines.recipes import save_recipe

recipe = {
    "pipeline": {
        "type": "sft",
        "name": "custom-sft",
        "description": "Custom starter recipe",
    },
    "model": {
        "base_model": "mistralai/Mistral-7B-v0.1",
        "tokenizer": "mistralai/Mistral-7B-v0.1",
        "trust_remote_code": False,
    },
    "paths": {
        "train_file": "examples/data/sft_train.jsonl",
        "output_dir": "outputs/custom-sft",
    },
    "trainer": {
        "epochs": 1,
        "batch_size": 2,
        "learning_rate": 2e-5,
    },
}

save_recipe("recipes/sft/custom-sft.yaml", recipe)
print("Saved recipes/sft/custom-sft.yaml")
