import csv
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class LocalBdaMetadataTests(unittest.TestCase):
    def test_agent_manifest_contains_bda_agents(self) -> None:
        manifest_path = ROOT / "_bmad" / "_config" / "agent-manifest.csv"
        with manifest_path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))

        rows_by_id = {row["canonicalId"]: row for row in rows}
        for canonical_id, expected_path in (
            ("bmad-devops", "agents/devops.md"),
            ("bmad-sre", "agents/sre.md"),
            ("bmad-analytics", "agents/analytics.md"),
        ):
            self.assertIn(canonical_id, rows_by_id)
            self.assertEqual(rows_by_id[canonical_id]["module"], "bda")
            self.assertEqual(rows_by_id[canonical_id]["path"], expected_path)

    def test_versions_are_aligned(self) -> None:
        module_text = (ROOT / "module.yaml").read_text(encoding="utf-8")
        module_version = re.search(r"^version:\s*(.+)$", module_text, re.MULTILINE)
        self.assertIsNotNone(module_version)
        expected = module_version.group(1)

        workflow_versions = []
        for manifest_path in sorted(ROOT.glob("workflows/*/bmad-skill-manifest.yaml")):
            text = manifest_path.read_text(encoding="utf-8")
            match = re.search(r"^version:\s*(.+)$", text, re.MULTILINE)
            self.assertIsNotNone(match, manifest_path.as_posix())
            workflow_versions.append((manifest_path, match.group(1)))

        agent_versions = []
        for agent_path in sorted(ROOT.glob("agents/*.yaml")):
            text = agent_path.read_text(encoding="utf-8")
            match = re.search(r"^version:\s*(.+)$", text, re.MULTILINE)
            self.assertIsNotNone(match, agent_path.as_posix())
            agent_versions.append((agent_path, match.group(1)))

        for path, version in workflow_versions + agent_versions:
            self.assertEqual(version, expected, path.as_posix())

    def test_phase_five_workflow_order_matches_runtime_loop(self) -> None:
        module_help_path = ROOT / "module-help.csv"
        with module_help_path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))

        phase_five_names = [row["name"] for row in rows if row["module"] == "bda" and row["phase"] == "5"]
        self.assertEqual(
            phase_five_names,
            [
                "Observability Setup",
                "Release Readiness",
                "Deploy",
                "Deployment Verification",
                "Post-Launch Review",
                "Spec Refinement",
            ],
        )


if __name__ == "__main__":
    unittest.main()
