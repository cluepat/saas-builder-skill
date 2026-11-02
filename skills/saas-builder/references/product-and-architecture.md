# Product and architecture

## Make the scope buildable

Define a small vertical slice: who signs in, what they create, who can see it, what success looks like, and what happens when they reach a limit. Separate public marketing/demo routes from authenticated workspace routes. A demo advertised as no-account must remain usable without auth and must not mutate customer data.

Classify capabilities as implemented, planned or intentionally omitted. Keep pricing and marketing consistent with that classification. Do not sell team seats, AI generation, replay, integrations or automatic workflows that do not exist. Treat prices, allowances and retention as product decisions; do not inherit another SaaS's numbers by default.

For an existing repository, inspect current remote/main, branch dependencies and dirty files before editing. Use a separate branch when requested. Prefer a small reviewable change to a fresh rewrite. If a newer branch already contains the billing, setup and design commits, create one final PR; merging superseded branches adds confusion rather than features.

## Reference deployment shape

| Surface         | Example destination                 | Responsibility                                        |
| --------------- | ----------------------------------- | ----------------------------------------------------- |
| Landing         | `https://example.com/`              | Product explanation and calls to action               |
| Public demo     | `/demo/`                            | Anonymous, isolated sample experience                 |
| App             | `/app/`                             | Login and authenticated workspace                     |
| Optional widget | `/v1/widget.js` and adjacent chunks | Public static assets                                  |
| Backend         | Hosted function URL                 | Authenticated operations and guarded public ingestion |
| Storage         | Private object bucket               | User attachments and exports                          |

This shape is a default, not a requirement. Separate domains when ownership, caching, cookie isolation or independent deployment justifies them. Cloudflare edge assets and a Supabase database do not need identical “CDN regions.” For latency, measure the actual requests and keep backend compute close to the database where possible.

## Boundaries that survive growth

Keep browser auth clients browser-only. Put bearer-authenticated requests in a focused API client. Let a workspace hook own session changes and initial/manual loading; domain components receive data and callbacks. Keep report/detail selections and unsaved drafts above views that unmount during navigation.

Use one canonical server implementation. If moving Next.js handlers to Edge Functions for static hosting, migrate the contracts, validation, authentication and errors as well as the route code. Update every caller, including widget installers and playground iframes.

Prefer explicit refresh initially when real-time data is unnecessary. If the product needs polling, realtime or paid refresh tiers, define that requirement and lifecycle explicitly. Do not accidentally refetch all tenant data on every auth-token renewal or add a timer as a substitute for state management.

## Decision record

Capture core flow, data ownership, selected services, route map, environment map, plan matrix, refresh behavior and deferred work. Keep this short enough to update when decisions change. Do not turn a historical choice into a permanent rule for all future products.
