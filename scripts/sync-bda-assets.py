#!/usr/bin/env python3
"""Sync BDA workflows and agents into a BMAD project without manual copy steps."""

from __future__ import annotations

import argparse
import csv
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


MANIFEST_FIELDS = [
    "name",
    "displayName",
    "title",
    "icon",
    "capabilities",
    "role",
    "identity",
    "communicationStyle",
    "principles",
    "module",
    "path",
    "canonicalId",
]


@dataclass(frozen=True)
class BdaAgent:
    name: str
    display_name: str
    title: str
    icon: str
    capabilities: str
    role: str
    identity: str
    communication_style: str
    principles: str
    canonical_id: str
    local_agent_path: str
    installed_agent_path: str


BDA_AGENTS = (
    BdaAgent(
        name="devops",
        display_name="DevOps",
        title="DevOps Agent",
        icon="⚙️",
        capabilities="deployment orchestration, infrastructure management, rollback coordination, smoke testing",
        role="Deployment orchestration, infrastructure management, and rollback coordination",
        identity="Operational specialist for production delivery on VPS environments. Focuses on boring, repeatable releases, rollback posture, and documenting exactly what changed.",
        communication_style="Checklist-driven, direct, and operationally calm. Prefers concrete preconditions, commands, and rollback triggers over theory.",
        principles="- Deployments should be boring and repeatable. - Always validate rollback posture before touching production. - Automate repetitive infrastructure work but keep explicit manual override paths. - Monitor first, deploy second. - Document failures as learning opportunities.",
        canonical_id="bmad-devops",
        local_agent_path="agents/devops.md",
        installed_agent_path="_bmad/bda/agents/devops.md",
    ),
    BdaAgent(
        name="sre",
        display_name="SRE",
        title="SRE Agent",
        icon="📡",
        capabilities="observability engineering, monitoring, performance analysis, incident response",
        role="Observability, monitoring, performance analysis, and incident response",
        identity="Reliability engineer who treats evidence as an operational contract. Specializes in turning logs, metrics, traces, and release markers into decisions the team can trust.",
        communication_style="Signals-first and evidence-led. Calm under pressure, skeptical of noisy dashboards, and precise about what must be measurable.",
        principles="- Observe first, optimize second. - Alerts should be actionable, not informational. - Dashboards are for humans, not robots. - Incidents are learning opportunities, not personal failures. - Measure what users care about.",
        canonical_id="bmad-sre",
        local_agent_path="agents/sre.md",
        installed_agent_path="_bmad/bda/agents/sre.md",
    ),
    BdaAgent(
        name="analytics",
        display_name="Analytics",
        title="Analytics Agent",
        icon="📈",
        capabilities="product analytics, feature adoption tracking, funnel analysis, behavior insights",
        role="Product analytics and behavior insights for production learning",
        identity="Analytics specialist who bridges raw product usage evidence to planning decisions. Focuses on adoption, drop-off, cohorts, and separating useful signals from vanity metrics.",
        communication_style="Curious, data-grounded, and pragmatic. Connects numbers back to user journeys and avoids overstating causality.",
        principles="- Users do not always do what they say they will do. - Feature usage does not equal feature value. - Drop-off points are gold mines for insights. - Cohort analysis reveals what averages hide. - Privacy is not negotiable.",
        canonical_id="bmad-analytics",
        local_agent_path="agents/analytics.md",
        installed_agent_path="_bmad/bda/agents/analytics.md",
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        default=".",
        help="BMAD project root that should receive the BDA workflows and agent registrations.",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy workflow directories instead of creating symlinks.",
    )
    return parser.parse_args()


def remove_existing(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def ensure_symlink_or_copy(source: Path, destination: Path, copy_mode: bool) -> None:
    if destination.exists() or destination.is_symlink():
        remove_existing(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if copy_mode:
        shutil.copytree(source, destination)
    else:
        destination.symlink_to(source.resolve(), target_is_directory=True)


def workflow_dirs(asset_root: Path) -> Iterable[Path]:
    return sorted(
        path for path in (asset_root / "workflows").iterdir() if path.is_dir() and (path / "SKILL.md").exists()
    )


def build_agent_skill(agent: BdaAgent, agent_path: str) -> str:
    load_path = f"{{project-root}}/{agent_path}" if agent_path.startswith("_bmad/") else agent_path
    return f"""---
name: {agent.canonical_id}
description: Launch the {agent.title}. Use when you want {agent.role.lower()} help.
---

# {agent.title}

## Overview

Launches the canonical {agent.title} from its maintained agent definition so the user always talks to the current BDA agent, not a stale wrapper copy.

## Identity

Thin launcher skill for the {agent.title}.

## Communication Style

Neutral and minimal until the canonical agent file takes over.

## Principles

- Load the canonical agent definition before producing substantive output.
- Preserve the canonical persona, menu, and activation flow without inventing local variants.
- Keep this wrapper lightweight and defer operational behavior to the maintained agent file.

## On Activation

<agent-activation CRITICAL="TRUE">
1. LOAD the FULL agent file from {load_path}
2. READ its entire contents - this contains the complete agent persona, menu, and instructions
3. FOLLOW every step in the <activation> section precisely
4. DISPLAY the welcome/greeting as instructed
5. PRESENT the numbered menu
6. WAIT for user input before proceeding
</agent-activation>
"""


def build_agent_manifest(agent: BdaAgent) -> str:
    return (
        '{\n'
        f'  "name": "{agent.canonical_id}",\n'
        f'  "displayName": "{agent.display_name}",\n'
        '  "persona": {\n'
        f'    "role": "{agent.role}",\n'
        f'    "identity": "{agent.identity}",\n'
        f'    "communicationStyle": "{agent.communication_style}",\n'
        f'    "principles": "{agent.principles}"\n'
        '  },\n'
        '  "capabilities": []\n'
        '}\n'
    )


def sync_agent_skills(project_root: Path, installed_layout: bool) -> list[str]:
    skills_dir = project_root / ".agents" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    synced = []
    for agent in BDA_AGENTS:
        agent_dir = skills_dir / agent.canonical_id
        agent_dir.mkdir(parents=True, exist_ok=True)
        agent_path = agent.installed_agent_path if installed_layout else agent.local_agent_path
        (agent_dir / "SKILL.md").write_text(build_agent_skill(agent, agent_path), encoding="utf-8")
        (agent_dir / "bmad-manifest.json").write_text(build_agent_manifest(agent), encoding="utf-8")
        synced.append(agent.canonical_id)
    return synced


def sync_workflows(project_root: Path, asset_root: Path, copy_mode: bool) -> list[str]:
    skills_dir = project_root / ".agents" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)
    synced = []
    for workflow_dir in workflow_dirs(asset_root):
        destination = skills_dir / workflow_dir.name
        ensure_symlink_or_copy(workflow_dir, destination, copy_mode)
        synced.append(workflow_dir.name)
    return synced


def load_manifest_rows(manifest_path: Path) -> list[dict[str, str]]:
    with manifest_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_manifest_rows(manifest_path: Path, rows: list[dict[str, str]]) -> None:
    with manifest_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        writer.writerows(rows)


def merge_agent_manifest(project_root: Path, installed_layout: bool) -> None:
    manifest_path = project_root / "_bmad" / "_config" / "agent-manifest.csv"
    rows = load_manifest_rows(manifest_path)
    by_id = {row["canonicalId"]: row for row in rows}
    bda_ids = {agent.canonical_id for agent in BDA_AGENTS}

    for agent in BDA_AGENTS:
        path_value = agent.installed_agent_path if installed_layout else agent.local_agent_path
        by_id[agent.canonical_id] = {
            "name": agent.name,
            "displayName": agent.display_name,
            "title": agent.title,
            "icon": agent.icon,
            "capabilities": agent.capabilities,
            "role": agent.role,
            "identity": agent.identity,
            "communicationStyle": agent.communication_style,
            "principles": agent.principles,
            "module": "bda",
            "path": path_value,
            "canonicalId": agent.canonical_id,
        }

    non_bda = [row for row in rows if row["canonicalId"] not in bda_ids]
    write_manifest_rows(manifest_path, non_bda + [by_id[agent.canonical_id] for agent in BDA_AGENTS])


def resolve_asset_root(project_root: Path, module_root: Path) -> tuple[Path, bool]:
    installed_root = project_root / "_bmad" / "bda"
    if installed_root.exists():
        return installed_root, True
    if project_root.resolve() == module_root.resolve():
        return module_root, False
    raise SystemExit(
        "Could not find installed BDA module under '_bmad/bda'. Run 'npx bmad-method install --action update --yes' first."
    )


def main() -> int:
    args = parse_args()
    module_root = Path(__file__).resolve().parent.parent
    project_root = Path(args.project_root).resolve()

    asset_root, installed_layout = resolve_asset_root(project_root, module_root)

    workflow_names = sync_workflows(project_root, asset_root, copy_mode=args.copy)
    agent_names = sync_agent_skills(project_root, installed_layout=installed_layout)
    merge_agent_manifest(project_root, installed_layout=installed_layout)

    print(f"Synced workflows: {', '.join(workflow_names)}")
    print(f"Synced agent skills: {', '.join(agent_names)}")
    print("Merged BDA agents into _bmad/_config/agent-manifest.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
