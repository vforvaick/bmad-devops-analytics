#!/usr/bin/env python3
"""Validate BDA production markdown artifacts against canonical schema."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


PLACEHOLDER_RE = re.compile(r"\[[^\]\n]{2,}\](?!\()")
H2_RE = re.compile(r"^## (.+)$", re.MULTILINE)


@dataclass
class ArtifactResult:
    path: Path
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors


def load_spec(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_targets(inputs: list[str], artifact_names: set[str]) -> list[Path]:
    targets: list[Path] = []
    seen: set[Path] = set()

    for raw in inputs:
        path = Path(raw)
        if not path.exists():
            raise FileNotFoundError(f"Target does not exist: {path}")

        candidates: list[Path]
        if path.is_dir():
            candidates = sorted(
                file for file in path.iterdir() if file.is_file() and file.name in artifact_names
            )
        else:
            candidates = [path]

        for candidate in candidates:
            resolved = candidate.resolve()
            if resolved not in seen:
                seen.add(resolved)
                targets.append(candidate)

    return targets


def extract_h2_headings(content: str) -> list[str]:
    return H2_RE.findall(content)


def find_metadata_value(content: str, label: str) -> str | None:
    pattern = re.compile(rf"^\*\*{re.escape(label)}\*\*:\s*(.+?)\s*$", re.MULTILINE)
    match = pattern.search(content)
    return match.group(1).strip() if match else None


def validate_order(actual: list[str], expected: list[str]) -> list[str]:
    errors: list[str] = []
    cursor = 0
    for heading in expected:
        try:
            index = actual.index(heading, cursor)
        except ValueError:
            errors.append(f"Missing required heading: ## {heading}")
            continue
        cursor = index + 1
    return errors


def validate_artifact(path: Path, spec: dict, allow_placeholders: bool) -> ArtifactResult:
    content = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []
    name = path.name

    artifact_spec = spec["artifacts"].get(name)
    if artifact_spec is None:
        return ArtifactResult(path=path, errors=[f"No schema defined for artifact: {name}"], warnings=[])

    stripped = content.lstrip()
    title_prefix = artifact_spec["title_prefix"]
    if not stripped.startswith(title_prefix):
        errors.append(f"Title must start with: {title_prefix}")

    for label in artifact_spec["required_metadata"]:
        value = find_metadata_value(content, label)
        if value is None:
            errors.append(f"Missing required metadata field: **{label}**")
            continue
        if not value:
            errors.append(f"Metadata field is empty: **{label}**")

    actual_headings = extract_h2_headings(content)
    errors.extend(validate_order(actual_headings, artifact_spec["required_headings"]))

    placeholders = sorted(set(PLACEHOLDER_RE.findall(content)))
    if placeholders:
        message = "Unresolved placeholder tokens found: " + ", ".join(placeholders[:10])
        if len(placeholders) > 10:
            message += ", ..."
        if allow_placeholders:
            warnings.append(message)
        else:
            errors.append(message)

    if "TBD" in content:
        message = "Found unresolved token: TBD"
        if allow_placeholders:
            warnings.append(message)
        else:
            errors.append(message)

    return ArtifactResult(path=path, errors=errors, warnings=warnings)


def print_text_report(results: list[ArtifactResult]) -> None:
    for result in results:
        status = "PASS" if result.ok else "FAIL"
        print(f"{status} {result.path}")
        for error in result.errors:
            print(f"  - ERROR: {error}")
        for warning in result.warnings:
            print(f"  - WARN: {warning}")


def build_json_report(results: list[ArtifactResult]) -> dict:
    return {
        "summary": {
            "total": len(results),
            "passed": sum(1 for result in results if result.ok),
            "failed": sum(1 for result in results if not result.ok),
        },
        "results": [
            {
                "path": str(result.path),
                "ok": result.ok,
                "errors": result.errors,
                "warnings": result.warnings,
            }
            for result in results
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate BDA production markdown artifacts against canonical schemas."
    )
    parser.add_argument(
        "targets",
        nargs="+",
        help="One or more artifact files or directories to validate.",
    )
    parser.add_argument(
        "--spec",
        default="schemas/production-artifact-spec.json",
        help="Path to the artifact schema JSON file.",
    )
    parser.add_argument(
        "--allow-placeholders",
        action="store_true",
        help="Allow placeholder tokens such as [value] and report them as warnings. Useful for validating templates.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON output instead of plain text.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    spec_path = Path(args.spec)
    spec = load_spec(spec_path)
    artifact_names = set(spec["artifacts"].keys())

    try:
        targets = collect_targets(args.targets, artifact_names)
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if not targets:
        print("No matching artifact files found for validation.", file=sys.stderr)
        return 2

    results = [validate_artifact(path, spec, args.allow_placeholders) for path in targets]

    if args.json:
        print(json.dumps(build_json_report(results), indent=2))
    else:
        print_text_report(results)

    return 0 if all(result.ok for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
