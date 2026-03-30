import csv
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "sync-bda-assets.py"


class SyncBdaAssetsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.tempdir.name)
        (self.project_root / ".agents" / "skills").mkdir(parents=True)
        (self.project_root / "_bmad" / "_config").mkdir(parents=True)
        (self.project_root / "_bmad" / "bda").parent.mkdir(parents=True, exist_ok=True)
        os.symlink(ROOT, self.project_root / "_bmad" / "bda", target_is_directory=True)

        manifest_path = self.project_root / "_bmad" / "_config" / "agent-manifest.csv"
        with manifest_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle, quoting=csv.QUOTE_ALL)
            writer.writerow(
                [
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
            )
            writer.writerow(
                [
                    "architect",
                    "Winston",
                    "Architect",
                    "🏗️",
                    "distributed systems",
                    "Architect",
                    "Base architect",
                    "Calm",
                    "Keep it simple",
                    "bmm",
                    "_bmad/bmm/agents/architect.md",
                    "bmad-architect",
                ]
            )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_sync_registers_workflows_and_agents(self) -> None:
        result = subprocess.run(
            ["python3", str(SCRIPT), "--project-root", str(self.project_root)],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertIn("Merged BDA agents", result.stdout)

        skill_root = self.project_root / ".agents" / "skills"
        self.assertTrue((skill_root / "bmad-bda-deploy").exists())
        self.assertTrue((skill_root / "bmad-bda-deploy").is_symlink())
        self.assertTrue((skill_root / "bmad-bda-deployment-verification").exists())
        self.assertTrue((skill_root / "bmad-bda-deployment-verification").is_symlink())

        wrapper = (skill_root / "bmad-devops" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("{project-root}/_bmad/bda/agents/devops.md", wrapper)

        with (self.project_root / "_bmad" / "_config" / "agent-manifest.csv").open(
            newline="", encoding="utf-8"
        ) as handle:
            rows = list(csv.DictReader(handle))

        rows_by_id = {row["canonicalId"]: row for row in rows}
        self.assertEqual(rows_by_id["bmad-devops"]["path"], "_bmad/bda/agents/devops.md")
        self.assertEqual(rows_by_id["bmad-sre"]["module"], "bda")
        self.assertEqual(rows_by_id["bmad-analytics"]["displayName"], "Analytics")

    def test_copy_mode_materializes_workflows(self) -> None:
        subprocess.run(
            ["python3", str(SCRIPT), "--project-root", str(self.project_root), "--copy"],
            cwd=ROOT,
            check=True,
        )
        deploy_dir = self.project_root / ".agents" / "skills" / "bmad-bda-deploy"
        self.assertTrue(deploy_dir.is_dir())
        self.assertFalse(deploy_dir.is_symlink())
        self.assertTrue((deploy_dir / "SKILL.md").exists())
        verification_dir = self.project_root / ".agents" / "skills" / "bmad-bda-deployment-verification"
        self.assertTrue(verification_dir.is_dir())
        self.assertFalse(verification_dir.is_symlink())
        self.assertTrue((verification_dir / "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
