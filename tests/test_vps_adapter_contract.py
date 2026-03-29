import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class VpsAdapterContractTests(unittest.TestCase):
    def test_adapter_no_longer_uses_placeholder_identity_values(self) -> None:
        text = (ROOT / "adapters" / "vps-default" / "adapter.ts").read_text(encoding="utf-8")
        self.assertNotIn("your-app-name", text)
        self.assertNotIn("your-org", text)
        self.assertNotIn("your-project", text)

    def test_config_contract_documents_required_env(self) -> None:
        config_text = (ROOT / "adapters" / "vps-default" / "config.ts").read_text(encoding="utf-8")
        for env_name in (
            "BDA_VPS_APP_LABEL",
            "BDA_VPS_SENTRY_ORG",
            "BDA_VPS_SENTRY_PROJECT",
            "SENTRY_TOKEN",
            "POSTHOG_API_KEY",
        ):
            self.assertIn(env_name, config_text)

        env_example = (ROOT / "adapters" / "vps-default" / ".env.example").read_text(encoding="utf-8")
        self.assertIn("BDA_VPS_APP_LABEL", env_example)
        self.assertIn("POSTHOG_API_KEY", env_example)


if __name__ == "__main__":
    unittest.main()
