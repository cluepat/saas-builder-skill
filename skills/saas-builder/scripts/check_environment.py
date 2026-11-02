#!/usr/bin/env python3
"""Read a simple env file; report configuration issues without emitting values."""
import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

PUBLIC_PREFIXES = ("VITE_", "NEXT_PUBLIC_", "PUBLIC_")
PRIVATE_NAME = re.compile(r"SERVICE_ROLE|SECRET|PRIVATE_KEY|DATABASE_URL|DB_PASSWORD|ACCESS_TOKEN|DODO_PAYMENTS_API_KEY|RESEND_API_KEY|OPENAI_API_KEY|ANTHROPIC_API_KEY")
BILLING_KEYS = ("DODO_PAYMENTS_API_KEY", "DODO_PAYMENTS_WEBHOOK_KEY", "DODO_PRO_MONTHLY_PRODUCT_ID", "DODO_PRO_ANNUAL_PRODUCT_ID")


def parse_env(text):
    result = {}
    for number, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[7:]
        if "=" not in line:
            raise ValueError(f"line {number}: expected KEY=VALUE")
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip()
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key):
            raise ValueError(f"line {number}: invalid setting name")
        if key in result:
            raise ValueError(f"line {number}: duplicate setting {key}")
        if value.startswith(('"', "'")):
            if len(value) < 2 or value[-1] != value[0]:
                raise ValueError(f"line {number}: use a complete single-line quoted value")
            value = value[1:-1]
        else:
            value = re.split(r"\s+#", value, maxsplit=1)[0].rstrip()
        if "$" in value:
            raise ValueError(f"line {number}: expand variables before auditing")
        result[key] = value
    return result


def placeholder(value):
    return not value or bool(re.search(r"YOUR_|REPLACE_|changeme|<[^>]+>", value, re.I))


def origin(url):
    parsed = urlsplit(url)
    return parsed.scheme, parsed.hostname, parsed.port or (443 if parsed.scheme == "https" else 80)


def audit(env, target, billing="off", production_url=None, production_project_ref=None):
    errors = []
    for key in env:
        if key.startswith(PUBLIC_PREFIXES) and PRIVATE_NAME.search(key):
            errors.append(f"{key}: private credential assigned to a public browser prefix")
    if env.get("APP_ENV") != target:
        errors.append("APP_ENV: does not match the explicit target")
    app_url = urlsplit(env.get("APP_URL", ""))
    if not app_url.hostname or app_url.scheme not in ("http", "https"):
        errors.append("APP_URL: provide an absolute HTTP(S) application URL")
    elif target != "development" and (app_url.scheme != "https" or app_url.hostname in ("localhost", "127.0.0.1", "::1")):
        errors.append("APP_URL: hosted targets require HTTPS and a non-loopback hostname")
    if target == "staging":
        if production_url and origin(env.get("APP_URL", "")) == origin(production_url):
            errors.append("APP_URL: staging points at the supplied production URL")
        if production_project_ref:
            production_host = production_project_ref + ".supabase.co"
            for key in ("VITE_SUPABASE_URL", "NEXT_PUBLIC_SUPABASE_URL", "SUPABASE_URL", "VITE_API_BASE_URL", "VITE_WIDGET_API_BASE_URL"):
                if urlsplit(env.get(key, "")).hostname == production_host:
                    errors.append(f"{key}: staging points at the supplied production project")
        if env.get("DODO_PAYMENTS_ENVIRONMENT") == "live_mode":
            errors.append("DODO_PAYMENTS_ENVIRONMENT: live billing is not allowed for staging")
    if billing != "off":
        expected = {"test": "test_mode", "live": "live_mode"}[billing]
        if env.get("DODO_PAYMENTS_ENVIRONMENT") != expected:
            errors.append("DODO_PAYMENTS_ENVIRONMENT: does not match the requested billing mode")
        for key in BILLING_KEYS:
            if placeholder(env.get(key, "")):
                errors.append(f"{key}: configure a non-placeholder server value")
        monthly = env.get("DODO_PRO_MONTHLY_PRODUCT_ID")
        if monthly and monthly == env.get("DODO_PRO_ANNUAL_PRODUCT_ID"):
            errors.append("DODO_PRO_MONTHLY_PRODUCT_ID / DODO_PRO_ANNUAL_PRODUCT_ID: recurring products must differ")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", required=True, type=Path)
    parser.add_argument("--target", required=True, choices=("development", "staging", "production"))
    parser.add_argument("--billing", default="off", choices=("off", "test", "live"))
    parser.add_argument("--production-url")
    parser.add_argument("--production-project-ref")
    args = parser.parse_args()
    try:
        env = parse_env(args.env_file.read_text())
        errors = audit(env, args.target, args.billing, args.production_url, args.production_project_ref)
    except (OSError, ValueError):
        # Error messages from URL parsing can include values; deliberately do not echo them.
        print("Could not parse the env file. Use unique KEY=VALUE entries, single-line quotes, and expanded variables.", file=sys.stderr)
        return 2
    for error in errors:
        print("FAIL " + error)
    if errors:
        print(f"{len(errors)} issue(s). No values were printed or uploaded.")
        return 1
    print("Local configuration checks passed. Provider access, deployed secrets, auth, billing records and end-to-end behavior still require verification.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
