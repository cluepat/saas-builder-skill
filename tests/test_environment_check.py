import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills/saas-builder/scripts/check_environment.py"
spec = importlib.util.spec_from_file_location("environment_check", SCRIPT)
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class EnvironmentCheckTests(unittest.TestCase):
    def base(self, target="production", mode="live_mode"):
        return {
            "APP_ENV": target, "APP_URL": "https://staging.example.com" if target == "staging" else "https://example.com/app/",
            "DODO_PAYMENTS_ENVIRONMENT": mode, "DODO_PAYMENTS_API_KEY": "private-fixture-value",
            "DODO_PAYMENTS_WEBHOOK_KEY": "signing-fixture-value", "DODO_PRO_MONTHLY_PRODUCT_ID": "monthly-fixture",
            "DODO_PRO_ANNUAL_PRODUCT_ID": "annual-fixture",
        }

    def test_production_live_configuration(self):
        self.assertEqual(checker.audit(self.base(), "production", "live"), [])

    def test_production_can_intentionally_verify_test_payments(self):
        self.assertEqual(checker.audit(self.base(mode="test_mode"), "production", "test"), [])

    def test_staging_never_accepts_live_billing_even_if_billing_check_is_off(self):
        errors = checker.audit(self.base("staging"), "staging")
        self.assertTrue(any("live billing" in error for error in errors))

    def test_staging_rejects_production_origin_even_with_a_different_path(self):
        errors = checker.audit(self.base("production", "test_mode") | {"APP_ENV": "staging"}, "staging", "test", "https://example.com:443")
        self.assertTrue(any("production URL" in error for error in errors))

    def test_staging_rejects_production_backend_and_widget_destinations(self):
        env = self.base("staging", "test_mode") | {"VITE_WIDGET_API_BASE_URL": "https://prodref.supabase.co/functions/v1/api/"}
        self.assertTrue(any("VITE_WIDGET_API_BASE_URL" in error for error in checker.audit(env, "staging", "test", production_project_ref="prodref")))

    def test_publishable_key_and_dsn_are_allowed_but_private_prefixes_are_not(self):
        env = self.base() | {"VITE_SUPABASE_PUBLISHABLE_KEY": "public-fixture", "NEXT_PUBLIC_SENTRY_DSN": "public-dsn", "VITE_SUPABASE_SERVICE_ROLE_KEY": "never-print-this"}
        errors = checker.audit(env, "production", "live")
        self.assertEqual(len(errors), 1)
        self.assertIn("VITE_SUPABASE_SERVICE_ROLE_KEY", errors[0])
        self.assertNotIn("never-print-this", errors[0])

    def test_distinct_recurring_products_and_complete_secret_configuration(self):
        env = self.base() | {"DODO_PAYMENTS_WEBHOOK_KEY": "", "DODO_PRO_ANNUAL_PRODUCT_ID": "monthly-fixture"}
        errors = checker.audit(env, "production", "live")
        self.assertEqual(len(errors), 2)

    def test_hosted_target_rejects_localhost(self):
        errors = checker.audit(self.base() | {"APP_URL": "http://127.0.0.1:4173/app/"}, "production", "live")
        self.assertTrue(any("non-loopback" in error for error in errors))

    def test_parser_preserves_hash_in_quoted_value_and_rejects_duplicates(self):
        self.assertEqual(checker.parse_env('export KEY="a#b"\nOTHER=value # comment\n'), {"KEY": "a#b", "OTHER": "value"})
        with self.assertRaises(ValueError):
            checker.parse_env("KEY=a\nKEY=b")

    def test_cli_never_prints_secret_values_on_failure(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "private.env"
            path.write_text('APP_ENV=production\nAPP_URL=https://example.com\nVITE_PRIVATE_KEY=sentinel-secret-value\n')
            result = subprocess.run([sys.executable, str(SCRIPT), "--env-file", str(path), "--target", "production"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertNotIn("sentinel-secret-value", result.stdout + result.stderr)
            self.assertIn("VITE_PRIVATE_KEY", result.stdout)

    def test_parser_errors_do_not_echo_a_value(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "private.env"
            path.write_text('APP_ENV=production\nAPP_URL=https://[sentinel-secret-value\n')
            result = subprocess.run([sys.executable, str(SCRIPT), "--env-file", str(path), "--target", "production"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertNotIn("sentinel-secret-value", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
