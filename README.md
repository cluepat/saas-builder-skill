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

## Install

Choose one installation method per client to avoid duplicate skills. All three clients use the same `skills/saas-builder` source. No MCP servers, automatic hooks or provider credentials are bundled.

### Codex

#### Codex plugin marketplace

```sh
codex plugin marketplace add cluepat/saas-builder-skill
codex plugin add saas-builder@cluepat
codex plugin list --marketplace cluepat
```

Start a new Codex chat after installation so the skill can be discovered. If your client exposes a Plugins directory instead of the CLI, select the Cluepat marketplace and install SaaS Builder. This plugin contains one skill and no MCP servers or bundled provider credentials.

For a standalone install, use the [shared installer](#standalone-skill) with `--client codex`.

### Claude Code

Run these inside Claude Code:

```text
/plugin marketplace add cluepat/saas-builder-skill
/plugin install saas-builder@cluepat
```

Start a new session, then invoke the plugin skill:

```text
/saas-builder:saas-builder Build my SaaS from a product brief through a verified launch.
```

For local plugin development, clone the repository and run `claude --plugin-dir ./saas-builder-skill`. To install just the skill instead, use the standalone installer below; its command is `/saas-builder` without a plugin namespace. See the [Claude Code skill documentation](https://code.claude.com/docs/en/skills) and [plugin marketplace documentation](https://code.claude.com/docs/en/plugin-marketplaces).

### Cursor

In Cursor, open **Customize → Plugins → From GitHub Repository** and enter:

```text
https://github.com/cluepat/saas-builder-skill
```

Choose the **SaaS Builder** plugin from the imported Cluepat marketplace and install it. UI labels can vary by Cursor version. This repository includes `.cursor-plugin/marketplace.json` and `.cursor-plugin/plugin.json`; it does not need to be listed in the official Cursor Marketplace to install from GitHub.

Start a new Agent chat and invoke:

```text
/saas-builder Build my SaaS from a product brief through a verified launch.
```

If your Cursor version does not offer GitHub marketplace import, use the standalone installer. See the [Cursor skill documentation](https://cursor.com/docs/skills) and [plugin reference](https://cursor.com/docs/reference/plugins).

### Standalone skill

Clone once, then choose the client:

```sh
git clone https://github.com/cluepat/saas-builder-skill.git
cd saas-builder-skill
python3 tools/install_skill.py --client claude-code
# Or: python3 tools/install_skill.py --client cursor
# Or: python3 tools/install_skill.py --client codex
```

Python 3.9+ is required; no dependencies or account sign-in are needed for this copy step. The installer refuses to overwrite an existing skill. Use `--dry-run` to inspect the target first.

| Client      | Personal skill folder           | Standalone invocation |
| ----------- | ------------------------------- | --------------------- |
| Codex       | `~/.codex/skills/saas-builder`  | `$saas-builder`       |
| Claude Code | `~/.claude/skills/saas-builder` | `/saas-builder`       |
| Cursor      | `~/.cursor/skills/saas-builder` | `/saas-builder`       |

To share a standalone skill with a project, run this from the cloned package:

```sh
python3 tools/install_skill.py --client cursor --scope project --project-dir /path/to/your-project
```

This creates `.cursor/skills/saas-builder` in that project. Substitute `claude-code` or `codex` for the equivalent project folder. Commit the folder to share it with teammates. After installation, open a new client session and confirm the skill appears in its skills or slash-command list. The installer copies files; it does not verify client discovery, sign in to providers or deploy an application.

For the [ZIP download](https://cluepat.github.io/saas-builder-skill/saas-builder.zip), extract `saas-builder/` into the appropriate personal or project skills folder. Keep the whole folder, including references, scripts and assets. Do not install both the plugin and the standalone copy in the same client. Cursor can also discover compatible Claude/Codex skill folders, so use only one shared copy when those are already available.

## Use it

The examples below use Codex syntax. In Claude Code, replace `Use $saas-builder` with `/saas-builder:saas-builder` for the plugin or `/saas-builder` for a standalone install. In Cursor, use `/saas-builder`.

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

The public guide is static HTML in `docs/`. GitHub Pages publishes `main` → `/docs`; no server or cloud credentials are needed. Skill and plugin version metadata are in `SKILL.md` and all four plugin manifests; keep them in sync for a release. Claude and Cursor use their own native manifests and marketplace files while all clients share one skill folder. If Claude Code is installed, run `claude plugin validate .` as an additional native check.

## License and attribution

MIT © 2026 Cluepat. Provider documentation and linked third-party skills keep their own licenses. The package links to their guidance and does not redistribute it. It is an independent community resource, not an official OpenAI, Anthropic, Cursor, Cloudflare, Supabase, Dodo, Resend, Sentry or Vercel product.
