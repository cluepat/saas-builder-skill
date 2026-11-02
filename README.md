# SaaS Builder Skill

A reusable agent skill for building and launching a SaaS—from the product brief to a verified production service.

Developed from building [Cluepat](https://cluepat.com). The package contains original workflow instructions, templates and a small configuration checker. It generalizes the decisions and integration lessons; every new product keeps its own requirements, branding, plans and credentials.

**[Read the public guide](https://cluepat.github.io/saas-builder-skill/) · [Read the skill](skills/saas-builder/SKILL.md) · [MIT license](LICENSE)**

## What it covers

- Product scope, a complete first user flow and maintainable React boundaries.
- Public landing/demo, authenticated app and shared accessible design tokens.
- Supabase Auth, correct email/OAuth redirects, tenant RLS and private uploads.
- Cloudflare static hosting, explicit monorepo configuration and actual backend deployment.
- Separate staging data, PR previews, revision checks and CI regression evidence.
- Dodo subscriptions, server entitlements, webhook verification and test-to-live cutover.
- Optional Resend mail, GitHub App issue creation and an external website widget.
- Sentry, usage visibility, scheduled cleanup, retention and launch evidence.

The suggested stack is configurable. This is an agent workflow, not a hosted service or a complete application template. Provider accounts and credentials belong to the person building the new product. Provider pricing, quotas and API syntax must be checked against current documentation.

## Install in Codex

### Plugin marketplace

```sh
codex plugin marketplace add cluepat/saas-builder-skill
codex plugin add saas-builder@cluepat
codex plugin list --marketplace cluepat
```

Start a new Codex chat after installation so the skill can be discovered. If your client exposes a Plugins directory instead of the CLI, select the Cluepat marketplace and install SaaS Builder. This plugin contains one skill and no MCP servers or bundled provider credentials.

### Standalone skill

```sh
git clone https://github.com/cluepat/saas-builder-skill.git
mkdir -p ~/.codex/skills
cp -R saas-builder-skill/skills/saas-builder ~/.codex/skills/
```

If `~/.codex/skills/saas-builder` already exists, compare or back it up before replacing it. Clients implementing the Agent Skills format can load the same `skills/saas-builder` folder through their own skill settings; installation paths differ by client.

## Use it

```text
Use $saas-builder to build a SaaS for collecting customer onboarding requests.
I need a landing page, a public sample demo, a private workspace and a paid plan.
Use React, Cloudflare and Supabase. Prepare Dodo billing in test mode first.
Build one complete user flow before expanding the dashboard.
```

For an existing product:

```text
Use $saas-builder to audit what is implemented, deployed, configured and verified.
Continue only the missing launch connections. Preserve the approved design and
existing functionality. Keep staging data separate from production.
```

The skill loads detailed references only when needed. It does not authorize publishing, real charges, messages, deletion or live account changes by itself. Existing user instructions and the host's action permissions still apply.

## Useful resources

- [Project brief](skills/saas-builder/assets/project-brief.md)
- [Launch evidence record](skills/saas-builder/assets/launch-record.md)
- [Billing and live cutover](skills/saas-builder/references/billing.md)
- [PR staging](skills/saas-builder/references/deployment-and-staging.md)
- [Environment example](skills/saas-builder/assets/environment.example)

Audit a private local environment file without sending or printing values:

```sh
python3 skills/saas-builder/scripts/check_environment.py \
  --env-file /path/to/private.env --target staging --billing test \
  --production-url https://example.com \
  --production-project-ref YOUR_PRODUCTION_PROJECT_REF
```

The checker supports simple, unique `KEY=VALUE` entries, single-line quoted values and `export` prefixes. Expand shell variables before using it. `--billing off` skips Dodo completeness checks; `test`/`live` verify presence and mode, not whether a key authenticates. A production app may intentionally use test payments during verification. Staging always rejects live billing. Passing the checker is not a deployment or security certification.

## Contribute

Keep instructions focused on decisions an agent might otherwise get wrong. Separate product-specific choices from reusable constraints. Add current primary documentation for provider-specific guidance. Do not include credentials, real project/account identifiers, checkout tokens, customer data or copied private application source.

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements-dev.txt
python3 tools/validate_package.py
python3 tools/build_download.py --check
python3 -m unittest discover -s tests -v
```

After editing skill resources, regenerate the standalone download with `python3 tools/build_download.py`.

The public guide is static HTML in `docs/`. GitHub Pages publishes `main` → `/docs`; no server or cloud credentials are needed. Skill and plugin version metadata are in `SKILL.md`, `plugin.json` and `.codex-plugin/plugin.json`; keep them in sync for a release.

## License and attribution

MIT © 2026 Cluepat. Provider documentation and linked third-party skills keep their own licenses. The package links to their guidance and does not redistribute it. It is an independent community resource, not an official OpenAI, Cloudflare, Supabase, Dodo, Resend, Sentry or Vercel product.
