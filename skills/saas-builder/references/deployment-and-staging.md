# Deployment and PR staging

## Selected host and runtime

Determine whether the app produces static assets, server-rendered routes or a long-running server. Match that output to the chosen host and its current framework integration. With Vercel, verify the framework preset, monorepo root, output, server runtime, environment scopes and preview behavior in the current [framework documentation](https://vercel.com/docs/frameworks). Use the corresponding provider guidance for other hosts. Do not add Wrangler or move APIs into Supabase solely because the reference stack does so.

For a full-stack host, keep server routes there when compatible; for a static-only deployment, deploy server logic separately. In both cases, verify secrets stay server-side and callbacks/webhooks reach the actual deployed endpoint.

## Explicit targets

Use a checked-in deployment configuration for each deployable app. For a monorepo, set the correct project root or use an explicit configuration path; do not depend on framework auto-detection guessing a workspace root. In the Cloudflare reference setup, use an explicit Wrangler configuration. Build the frontend that the selected host actually serves. A Vite/static deployment and an optional Next.js server build are different outputs.

For a static app, deploy API handlers to the backend service and update the dashboard, widget and installer API destinations. Browser public variables configure clients; they do not create database tables, Auth providers or server functions. Keep provider secrets in the server's secret store, not frontend build variables.

Deploy compatible database migrations and backend functions before a frontend that depends on them. Use additive/backward-compatible schema changes when another version may still be running. Roll back code without assuming applied schema migrations can safely be reversed.

## PR previews

Use a separate backend project for staging if tests need real auth, storage or integrations. An isolated frontend URL pointing at production is not an isolated test environment. Refuse the production project/ref/key in staging build and deploy scripts. Keep staging billing in test mode.

Run CI checks first, then deploy the same PR revision to staging. Publish its URL and revision in the Actions summary and preferably a GitHub deployment/environment link. A small public build-info resource and a visible staging indicator make previews distinguishable from production. Apply `noindex` and appropriate preview cache headers.

If PR frontends share one staging backend, say so. Serialize backend deployments, reject obsolete runs, and verify frontend/API revisions match before integration tests. A PR-specific hostname does not make its schema or data private to that PR. Migrations should use version checks and appropriate database locking.

Give fork PRs verification checks without deployment secrets. Use reviewed same-repository branches for deployment. Avoid `pull_request_target` executing untrusted PR code with privileged credentials. A staging-required merge gate must reject a skipped/failed deploy; it should not become green merely because a job did not run.

Choose one owner for preview deployments. If GitHub Actions deploys isolated staging, disable a competing native preview job that would build PRs using production configuration. Keep normal main-branch production deployment intact. On PR close, remove only that PR's frontend preview; do not delete a shared staging backend.

## Cache and widget files

Serve a small versioned loader with a short cache lifetime; use immutable caching for content-hashed chunks. Resolve chunks relative to the loader's asset URL, and API requests relative to the configured backend. Ensure CORS applies to every lazy-loaded module, not just the loader. Test an installation from a different website origin.

## Smoke checks

Check landing, anonymous demo, app sign-in, public asset MIME type, widget chunks, API health/revision and unauthorized private calls. Confirm the actual frontend API destination after build. A deployment marked successful by the host can still serve stale files or the wrong backend.

Sources: [Cloudflare Workers configuration](https://developers.cloudflare.com/workers/wrangler/configuration/), [static assets](https://developers.cloudflare.com/workers/static-assets/), [GitHub deployment environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/managing-environments-for-deployment), [Supabase functions](https://supabase.com/docs/guides/functions).
