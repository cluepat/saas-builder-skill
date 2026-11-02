# Choose your SaaS stack

Invoke the skill with `$saas-builder` in Codex, `/saas-builder:saas-builder` for the Claude Code plugin, or `/saas-builder` for Cursor and standalone Claude Code installations. Then adapt this prompt. Replace bracketed fields; keep undecided choices open.

```text
Build a SaaS for [target users and the problem it solves].
The first complete user flow is [sign in → action → useful outcome].

Project: [new product / existing repository to extend]
Frontend framework and language: [Vue, Angular, React, SvelteKit or any other]
Rendering needs: [CSR / SSR / prerender / recommend based on the product]
Backend/API: [preferred service or runtime / preserve existing / recommend]
Database, auth and storage: [preferences / preserve existing / recommend]
Deployment host: [Vercel, Cloudflare, AWS or any other]
Payments: [Stripe, Dodo, another provider / no payments yet]
Email, monitoring and AI: [only the capabilities actually needed]
Constraints: [budget, region, existing accounts, team experience, design]

Honor the choices I supplied. Inspect an existing repository before proposing
changes. For unspecified choices, preserve the existing stack or recommend
a compatible option with reasons. Ask only about consequential gaps.
Check rendering/runtime, SDK and provider compatibility before scaffolding.
Explain incompatibilities and propose options instead of silently substituting.
Build one complete user flow, then connect and verify the deployed service.
Use isolated staging data and test payments. Keep private credentials out of chat.
```

## Vue + Vercel + Stripe

```text
Build a customer feedback SaaS using Vue with TypeScript, deployed on Vercel,
with Supabase for database/auth/private storage and Stripe subscriptions.
Recommend Vue/Vite or Nuxt based on the landing page and app rendering needs.
Implement submission → private inbox → paid quota as the first complete flow.
Check runtime/SDK compatibility and use Stripe test payments first.
```

## Angular + an existing backend

```text
Extend this Angular application. Preserve its existing API, database and auth.
Use Vercel for the frontend and Stripe for subscriptions, if compatible with
the current backend runtime. Explain any necessary deployment changes first.
Preserve current behavior and add one complete paid-feature flow with tests.
```

## Ask for a recommendation

```text
Build a booking SaaS for independent tutors. I have not selected a stack.
Recommend a frontend, backend/data/auth, host and payment provider based on
my budget and scheduling needs. Explain the tradeoffs and clarify consequential
unknowns before scaffolding. Do not assume the reference stack is mandatory.
```
