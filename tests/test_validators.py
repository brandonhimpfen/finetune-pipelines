from finetune_pipelines.validators import validate_records


def test_validate_sft_records() -> None:
    report = validate_records(
        [
            {"prompt": "Hello", "completion": "Hi"},
            {"prompt": "A", "completion": "B"},
        ],
        "sft",
    )
    assert report.valid is True
    assert report.record_count == 2


def test_validate_dpo_records() -> None:
    report = validate_records(
        [
            {"prompt": "Hello", "chosen": "Hi", "rejected": "No"},
        ],
        "dpo",
    )
    assert report.valid is True
