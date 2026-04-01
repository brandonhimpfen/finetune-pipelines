from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ValidationReport:
    valid: bool
    pipeline_type: str
    record_count: int
    issues: list[str]


SFT_REQUIRED_KEYS = {"prompt", "completion"}
DPO_REQUIRED_KEYS = {"prompt", "chosen", "rejected"}


def validate_records(records: list[dict[str, object]], pipeline_type: str) -> ValidationReport:
    issues: list[str] = []

    if pipeline_type == "sft":
        required = SFT_REQUIRED_KEYS
    elif pipeline_type == "dpo":
        required = DPO_REQUIRED_KEYS
    else:
        return ValidationReport(
            valid=False,
            pipeline_type=pipeline_type,
            record_count=len(records),
            issues=[f"Unsupported pipeline type: {pipeline_type}"],
        )

    for idx, record in enumerate(records):
        missing = required - set(record.keys())
        if missing:
            issues.append(f"record[{idx}] missing keys: {sorted(missing)}")
            continue
        for key in required:
            value = record.get(key)
            if not isinstance(value, str) or not value.strip():
                issues.append(f"record[{idx}] field '{key}' must be a non-empty string")

    return ValidationReport(
        valid=not issues,
        pipeline_type=pipeline_type,
        record_count=len(records),
        issues=issues,
    )
