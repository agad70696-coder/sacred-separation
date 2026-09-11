#!/usr/bin/env python3

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []

    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()

            if not line:
                continue

            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSONL at {path}:{line_no}: {exc}"
                ) from exc

            if not isinstance(obj, dict):
                raise ValueError(
                    f"{path}:{line_no} must contain a JSON object"
                )

            rows.append(obj)

    return rows


def require_file(path: Path, label: str) -> None:
    if not path.exists():
        raise RuntimeError(
            f"BLOCKED: missing {label}: {path}"
        )


def validate_required_fields(record: dict[str, Any], label: str) -> None:
    required = {
        "construction_id",
        "ayah",
        "parent_id",
        "family",
        "domain",
        "entry",
        "slot",
        "span",
    }

    missing = sorted(required - set(record.keys()))

    if missing:
        raise RuntimeError(
            f"BLOCKED: {label} {record.get('construction_id')} "
            f"missing fields: {missing}"
        )


def entropy_bits(n: int) -> float:
    if n <= 1:
        return 0.0
    return math.log2(n)


def model_cost(
    model: dict[str, Any],
    codebook: dict[str, Any]
) -> float:
    costs = codebook["costs"]
    transform = model["transform"]

    # Deterministic representation cost.
    # Each active top-level capability is paid once.
    total = 0.0

    total += costs["domain_symbol"]
    total += costs["family_symbol"]
    total += costs["entry_symbol"]
    total += costs["slot_symbol"]
    total += costs["span_symbol"]
    total += costs["transition_symbol"]

    active_transforms = sum(
        1 for value in transform.values() if value is True
    )

    # Explicit complexity cost for additional transformations.
    total += active_transforms * 1.0

    return total


def normalized_record(
    record: dict[str, Any],
    model: dict[str, Any]
) -> dict[str, Any]:
    out = dict(record)
    t = model["transform"]

    if t["speech_to_entry"] and out.get("family") == "Speech":
        out["family"] = "CLAUSAL"
        out["domain"] = "CLAUSAL"
        out["entry"] = "Speech"

    if t["address_to_entry"] and out.get("family") == "Address":
        out["family"] = "CLAUSAL"
        out["domain"] = "CLAUSAL"
        out["entry"] = "Address"

    if t["predicate_to_entry"] and out.get("family") == "Predicate":
        out["family"] = "CLAUSAL"
        out["domain"] = "CLAUSAL"
        out["entry"] = "Predicate"

    if t["assertion_to_entry"] and out.get("family") == "Assertion":
        out["family"] = "CLAUSAL"
        out["domain"] = "CLAUSAL"
        out["entry"] = "Assertion"

    if t["constraint_grouping"]:
        constraint_families = {
            "Negation",
            "Restriction",
            "Exception",
            "Boundary"
        }

        if out.get("family") in constraint_families:
            original = out["family"]
            out["family"] = "CONSTRAINT"
            out["domain"] = "CONSTRAINT"
            out["entry"] = original

    return out


def compare_field(
    gold: dict[str, Any],
    pred: dict[str, Any],
    field: str
) -> bool:
    return gold.get(field) == pred.get(field)


def record_residual_cost(
    gold: dict[str, Any],
    pred: dict[str, Any],
    codebook: dict[str, Any]
) -> tuple[float, list[str]]:
    c = codebook["costs"]
    total = 0.0
    residuals: list[str] = []

    checks = [
        ("family", "residual_family"),
        ("domain", "residual_domain"),
        ("entry", "residual_entry"),
        ("slot", "residual_slot"),
        ("span", "residual_span"),
        ("parent_id", "residual_parent")
    ]

    for field, cost_key in checks:
        if not compare_field(gold, pred, field):
            total += c[cost_key]
            residuals.append(field)

    if residuals:
        total += c["exception"]

    return total, residuals


def evaluate_model(
    gold: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    model: dict[str, Any],
    codebook: dict[str, Any]
) -> dict[str, Any]:

    candidate_map = {
        row["construction_id"]: row
        for row in candidates
    }

    total_data_cost = 0.0
    exception_cost = 0.0
    exact = 0
    evaluated = 0
    missing_predictions = 0

    residual_counts: dict[str, int] = {}

    for g in gold:
        cid = g["construction_id"]

        if cid not in candidate_map:
            missing_predictions += 1
            c = codebook["costs"]["exception"]
            total_data_cost += c
            exception_cost += c
            residual_counts["missing_prediction"] = (
                residual_counts.get("missing_prediction", 0) + 1
            )
            continue

        p = normalized_record(candidate_map[cid], model)
        cost, residuals = record_residual_cost(
            g,
            p,
            codebook
        )

        total_data_cost += cost
        evaluated += 1

        if not residuals:
            exact += 1

        for field in residuals:
            residual_counts[field] = (
                residual_counts.get(field, 0) + 1
            )

        if residuals:
            exception_cost += codebook["costs"]["exception"]

    mcost = model_cost(model, codebook)
    total = mcost + total_data_cost

    exact_rate = (
        exact / len(gold)
        if gold
        else 0.0
    )

    return {
        "model_id": model["model_id"],
        "gold_records": len(gold),
        "evaluated_predictions": evaluated,
        "missing_predictions": missing_predictions,
        "exact_records": exact,
        "exact_rate": exact_rate,
        "model_cost_bits": mcost,
        "data_cost_bits": total_data_cost,
        "exception_cost_bits": exception_cost,
        "total_description_length_bits": total,
        "residual_counts": residual_counts
    }


def main() -> int:
    gold_path = ROOT / "gold" / "gold_01_85.jsonl"
    codebook_path = ROOT / "codebooks" / "mdl_v1.json"

    require_file(gold_path, "Gold 1-85")
    require_file(codebook_path, "MDL codebook")

    gold = load_jsonl(gold_path)

    if not gold:
        raise RuntimeError(
            "BLOCKED: Gold 1-85 is empty"
        )

    for row in gold:
        validate_required_fields(row, "Gold record")

    codebook = load_json(codebook_path)

    results = []

    for model_id in ["M9", "M8", "M7", "M6"]:
        model_path = ROOT / "models" / f"{model_id}.json"
        candidate_path = (
            ROOT / "evaluations" / f"{model_id}_candidate.jsonl"
        )

        require_file(model_path, f"{model_id} specification")
        require_file(candidate_path, f"{model_id} candidate dataset")

        model = load_json(model_path)
        candidates = load_jsonl(candidate_path)

        for row in candidates:
            validate_required_fields(row, f"{model_id} candidate")

        result = evaluate_model(
            gold,
            candidates,
            model,
            codebook
        )

        results.append(result)

    results.sort(
        key=lambda x: (
            x["total_description_length_bits"],
            x["data_cost_bits"],
            x["exception_cost_bits"],
            x["model_cost_bits"],
            x["model_id"]
        )
    )

    output = {
        "status": "PASS",
        "protocol": {
            "gold": "gold_01_85.jsonl",
            "models": ["M9", "M8", "M7", "M6"],
            "codebook": "mdl_v1",
            "selection": "minimum total description length"
        },
        "winner": results[0]["model_id"],
        "results": results
    }

    out_path = ROOT / "reports" / "mdl_gold_01_85.json"

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(
            output,
            f,
            ensure_ascii=False,
            indent=2
        )

    print(json.dumps(output, ensure_ascii=False, indent=2))
    print(f"\nWROTE: {out_path}")

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)
