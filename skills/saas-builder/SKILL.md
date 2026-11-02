---
name: saas-builder
description: Build or extend a SaaS from a product brief through a verified launch, including tenant-aware data, auth, billing, staging and operations. Use for substantial SaaS implementation or launch work; a small isolated UI edit does not need the full workflow.
license: MIT
metadata:
  author: cluepat
  version: "1.2.0"
---

# SaaS Builder

Turn the user's product into a working service, then connect and verify the deployed service. Treat this as a configurable implementation workflow, not a fixed starter app.

## Begin with the actual product

Read the repository instructions, current branch, local changes and existing deployment configuration. Preserve work already present. For an existing app, identify the missing slice and continue there; do not restart its design or replace working integrations.

Use the user's brief and connected sources to establish the primary user, core action, workspace/tenant model, public/demo experience, paid value, data sensitivity and launch destination. Ask only for consequential missing choices. Make reversible implementation choices autonomously within the user's scope. See [product and architecture](references/product-and-architecture.md) when defining scope or choosing the stack. The optional [project brief](assets/project-brief.md) records these decisions.

## Let the user choose the stack

Before scaffolding a new product, establish the frontend framework, rendering model, backend/database/auth, deployment host and payment provider (or no payments). Honor choices already in the brief; inspect and preserve an existing app's stack. For consequential gaps, ask one compact question with a free-text option, or offer a reasoned recommendation if the user delegated the choice. Do not require the user to choose every optional service before useful work can begin.

React, Vue/Nuxt, Angular, SvelteKit and other frameworks are valid choices; Cloudflare, Vercel and other hosts are alternatives; Stripe, Dodo and other payment providers are alternatives. This is not a prebuilt connector matrix. Verify the selected framework's rendering/build output, host runtime, SDK support and provider availability before committing to an integration. Explain a concrete incompatibility and propose options; do not silently substitute the reference stack or migrate an existing app.

Read [stack selection](references/stack-selection.md) when choosing or adapting services. Use the editable [stack prompt](assets/stack-prompt.md) to capture the user's preferences and unresolved choices. The optional [project brief](assets/project-brief.md) records the final decisions.

The worked reference stack is React + TypeScript, Cloudflare Workers, Supabase Auth/Postgres/private Storage/Edge Functions, Resend, optional Dodo billing, and Sentry. Use it only when it fits the user's choices. Provider-specific examples, environment keys and helper checks apply to that stack; adapt them deliberately for another stack. Use an AI provider only for an implemented AI capability; an export for an external coding agent is not built-in AI inference.

## Implement one complete path first

Connect the core flow across UI, API, authorization, database and storage before multiplying screens. Keep state ownership clear: shared UI components, domain components, framework-appropriate state/services, API clients and pure utilities. Extract repetition when responsibilities are real; avoid speculative abstractions.

Use shared design tokens for surfaces, type, spacing and primary actions. Semantic error, warning, success and information colors remain independent of the brand palette. Honor the chosen design direction; change only the requested aspects. Read [design and verification](references/design-and-verification.md) for presentation or component/state changes.

## Load the relevant implementation reference

| Work needed                                                  | Reference                                                      |
| ------------------------------------------------------------ | -------------------------------------------------------------- |
| Auth, tenant isolation, redirects, uploads, CORS             | [Auth and data](references/auth-and-data.md)                   |
| Deployment, host/runtime compatibility and PR staging        | [Deployment and staging](references/deployment-and-staging.md) |
| Subscriptions, entitlements, limits and test-to-live cutover | [Billing](references/billing.md)                               |
| Resend, GitHub App or an external website widget             | [Optional integrations](references/integrations.md)            |
| Monitoring, cleanup, retention and final launch evidence     | [Operations and launch](references/operations-and-launch.md)   |

Read only the sections relevant to the current work. Provider SDKs, dashboard labels, pricing, quotas and deployment syntax change: consult current primary documentation or the connected provider tools before relying on them. Prefer a suitable installed provider skill when available; this package does not require another skill to function.

## Keep configuration explicit

Separate public browser identifiers from server credentials. Public Supabase publishable/anon keys are expected browser inputs; service-role keys, payment API keys and signing secrets stay server-side. Ask the owner to configure credentials privately when needed. Never include a real environment file, account export, checkout token or customer record in public examples.

Record the frontend URL, backend project, storage bucket, auth redirects, billing mode and deployed revision for each environment. Choose one hostname with routes when that serves the product; extra `app`, `cdn` and `api` subdomains are optional. A static frontend build cannot execute server API handlers, and frontend environment variables alone do not deploy a backend.

The bundled environment checker supports the Cloudflare/Supabase/Dodo reference configuration only. It does not validate Stripe, Vercel, Firebase or arbitrary environment schemas. For the reference stack, optionally run:

```sh
python3 scripts/check_environment.py --env-file /path/to/private.env --target staging --billing test --production-url https://example.com --production-project-ref PRODUCTION_PROJECT_REF
```

Run the script from this skill's directory, or use its absolute path. It reads local configuration and reports setting names only. It does not connect to providers, deploy anything or certify an environment as production-ready.

## Verify the service, not just the code

Keep these states distinct in updates: **implemented**, **deployed**, **provider configured**, **verified**. A successful build proves implementation compatibility; it does not prove email delivery, a private download, a running scheduled job or paid entitlement activation.

Run checks appropriate to the changed behavior. Integration tests should mock external providers; deployment smoke tests should verify real routing, auth rejection, CORS, asset loading and revision identity. Use disposable accounts in an explicitly chosen non-production environment for mutating tests. Do not purchase a live subscription or send messages merely to demonstrate a flow without the applicable authorization.

Before a production change, make the configuration or patch concrete and reviewable. Preserve the user's existing authorization; request a decision only for an unresolved choice, a new consequential action or a required credential. For a failed or ambiguous provider write, inspect current state before retrying. A timeout is not evidence that nothing was created.

Use the [launch record](assets/launch-record.md) to record observed evidence and remaining owner actions. Do not call a service connected end to end while a required link is still unverified. Distinguish a configuration-complete launch from an actual verified paid transaction.
