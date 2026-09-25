#!/usr/bin/env python3
"""Offline paired-result checker. It does not call providers or send data."""
import json
import sys
from pathlib import Path


def answer(value):
    return value.replace("\r\n", "\n").strip()


def nonnegative_int(value, label):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return value


def measure(data):
    for section in ("baseline", "jev"):
        if not isinstance(data.get(section), dict):
            raise ValueError(f"missing object: {section}")
    if not isinstance(data.get("expected"), str):
        raise ValueError("expected must be a string")
    baseline, jev = data["baseline"], data["jev"]
    for section, obj in (("baseline", baseline), ("jev", jev)):
        for key in ("output",):
            if not isinstance(obj.get(key), str):
                raise ValueError(f"{section}.{key} must be a string")
    counts = {}
    for key in ("chatgpt_input_tokens", "chatgpt_output_tokens", "local_input_tokens", "local_output_tokens"):
        counts[key] = nonnegative_int(jev.get(key), f"jev.{key}")
    baseline_total = sum(nonnegative_int(baseline.get(k), f"baseline.{k}") for k in ("input_tokens", "output_tokens"))
    jev_chatgpt_total = counts["chatgpt_input_tokens"] + counts["chatgpt_output_tokens"]
    local_total = counts["local_input_tokens"] + counts["local_output_tokens"]
    baseline_pass = answer(baseline["output"]) == answer(data["expected"])
    jev_pass = answer(jev["output"]) == answer(data["expected"])
    credited = max(0, baseline_total - jev_chatgpt_total) if baseline_pass and jev_pass else 0
    return {
        "task": str(data.get("task", "unnamed task")),
        "baseline_exact_match": baseline_pass,
        "jev_exact_match": jev_pass,
        "quality_equivalent": baseline_pass and jev_pass,
        "baseline_chatgpt_tokens": baseline_total,
        "jev_chatgpt_tokens": jev_chatgpt_total,
        "jev_local_tokens": local_total,
        "chatgpt_tokens_avoided_credited": credited,
        "credit_rule": "both outputs must exactly match expected; only observed ChatGPT tokens are counted",
    }


def self_test():
    passing = {
        "expected": "A\nB", "baseline": {"output": "A\nB", "input_tokens": 100, "output_tokens": 20},
        "jev": {"output": " A\r\nB ", "chatgpt_input_tokens": 0, "chatgpt_output_tokens": 0, "local_input_tokens": 30, "local_output_tokens": 8},
    }
    assert measure(passing)["chatgpt_tokens_avoided_credited"] == 120
    passing["jev"]["output"] = "A\nC"
    assert measure(passing)["chatgpt_tokens_avoided_credited"] == 0
    passing["jev"]["output"] = "A\nB"
    passing["jev"]["chatgpt_input_tokens"] = 4
    assert measure(passing)["chatgpt_tokens_avoided_credited"] == 116
    print("self-test: 3 checks passed")


def main():
    if sys.argv[1:] in (["-h"], ["--help"]):
        print(f"usage: {Path(sys.argv[0]).name} <pair.json> | --self-test")
        print("Compare baseline and Jev outputs against an expected answer.")
        return 0
    if sys.argv[1:] == ["--self-test"]:
        self_test()
        return 0
    if len(sys.argv) != 2:
        print(f"usage: {Path(sys.argv[0]).name} <pair.json> | --self-test", file=sys.stderr)
        return 2
    try:
        report = measure(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
