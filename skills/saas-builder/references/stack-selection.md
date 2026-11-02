# Stack selection and adaptation

## Capture choices without forcing the reference stack

For a new product, honor the user's specified services. Group consequential missing choices into one question, for example: “Which frontend framework, backend/data/auth, hosting and payment provider should we use? You can name any stack, keep a choice open for my recommendation, or omit payments.” If the user delegates the decision, recommend a compatible set with reasons tied to their product, team and constraints. Do not keep asking about settled choices.

For an existing product, inspect dependencies, runtime and deployment files first. Preserve them for unspecified fields. An explicit choice that requires migration needs an explanation of affected behavior/data and a migration plan; a library preference does not authorize replacing the whole app.

Use [the prompt template](../assets/stack-prompt.md) to record choices, not to impose a fixed menu. Framework, backend, database, auth, storage, host, payments, mail, monitoring and AI can be chosen independently where compatible. “No payments yet” means no checkout or subscription setup. Optional integrations should follow actual requirements.

## Check compatibility before scaffolding

Record the rendering model (CSR, SSR, prerender or mixed), server runtime, persistence, background work and deployment outputs. Check current official documentation and installed provider skills where relevant. Examples:

- Vue can be a client-rendered app or use SSR; distinguish Vue from a full-stack framework such as Nuxt. Use [Vue's SSR guide](https://vuejs.org/guide/scaling-up/ssr.html) for the requested rendering model.
- Angular may use client, server or prerendered routes. Follow its [rendering guidance](https://angular.dev/guide/ssr) and [style guide](https://angular.dev/style-guide); do not apply React hook rules to Angular services or components.
- For Vercel, verify the selected framework integration, server/edge runtime and preview configuration in its [framework docs](https://vercel.com/docs/frameworks). A static bundle alone cannot run a server webhook, even when the host also supports functions.
- For payments, check SDK/runtime compatibility and the provider's own checkout, signature, event and portal contracts. Stripe and Dodo are distinct integrations; see [billing](billing.md). Do not infer merchant-of-record or tax handling from another provider.

When a combination is unsupported, describe the specific constraint and offer the smallest compatible adjustment. Do not silently switch frameworks, hosts or billing providers. Describe unverified combinations as implementation choices to validate, not as tested connectors bundled with this skill.

## Carry the decisions through the whole build

Use idiomatic components, state management, routing and tests for the selected framework. Keep secrets, tenant authorization, private uploads and billing entitlements on the appropriate server runtime. Map provider-specific configuration names explicitly; renaming an environment variable does not port an integration.

Adapt local development, migrations, API deployment, auth callbacks, webhook destinations, scheduled jobs, preview isolation, CI and rollback to the selected host/backend. Test the chosen stack's core flow in isolation, then verify the deployed endpoints. A successful reference-stack check does not validate another provider's configuration.

The included `check_environment.py` helper understands only the documented Supabase/Dodo reference configuration. For another stack, use provider-native validation or implement focused checks for its actual schema. Do not require unused Supabase or Dodo keys to make a different stack pass.
