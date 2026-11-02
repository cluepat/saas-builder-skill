# Operations and launch evidence

## Retention and cleanup

Choose retention as a product decision. One possible free/paid model is time-limited Free retention and retention while the paid subscription is active; limits, grace periods and backup obligations still need explicit definitions. “Until manually deleted” must not silently promise infinite storage.

Provision cleanup for abandoned upload intents/objects, expired operational records and records past the chosen retention period. Derive storage deletion and database deletion from the same ownership model. Use bounded batches, retries, concurrency protection and observable outcomes. Exercise dry-run counts before enabling destructive cleanup, and authorize the actual retention/deletion policy.

Implementing a cleanup endpoint is different from provisioning its cron schedule, worker secret and monitoring. Verify the schedule by querying the persisted job state and running a non-destructive probe. Investigate an inactive schedule rather than making CI ignore it. Keep GitHub issues or other externally owned records unless their deletion is separately chosen.

## Monitoring

Configure frontend, backend and widget ingestion deliberately. Backend monitoring should cover API/upload/server failures; ordinary 4xx validation/auth errors usually need metrics rather than new-error alerts. The dashboard captures its runtime errors. A widget reports its own attachment/submission failures without treating every host-page error as an application failure.

Scrub event data and disable unnecessary PII. Exclude public demo submissions from real operational incidents where appropriate. Add each ingestion origin to the right CSP `connect-src`; customers with restrictive CSP may need to allow the widget's ingestion origin. Configuring an SDK/DSN does not create provider alert rules: verify the recipient, production environment filters and notification interval.

Monitor usage and provider spend separately from error reporting. Track rejected uploads, ingestion failures, queue exhaustion, webhook delivery failures and cleanup outcomes. Choose production-only monitoring or staging monitoring according to the owner's preference.

## Launch evidence

Record a concrete result for each applicable path:

| Path            | Evidence                                                                                         |
| --------------- | ------------------------------------------------------------------------------------------------ |
| Public surfaces | Landing, pricing and no-account demo load on the intended domain                                 |
| Auth            | Confirmation, OAuth if offered, recovery and return URLs work on the deployed origin             |
| Tenant data     | Owner succeeds; unauthenticated and other-tenant calls fail                                      |
| Assets          | Private upload/finalization/download and expiration work                                         |
| Optional widget | External-origin modules and actual submission/diagnostics work                                   |
| Optional GitHub | Installation, manual creation, eligible automatic job and disconnect work                        |
| Paid plans      | Correct checkout mode/charge, signed webhook entitlement, duplicate handling and portal behavior |
| PR staging      | Correct URL/revision/backend and green required checks                                           |
| Operations      | Real schedule state, cleanup dry run, monitoring event/alert and usage visibility                |

The [launch record template](../assets/launch-record.md) separates implementation, deployment, provider configuration and verification. Use explicit “not verified” or “not applicable” entries instead of fabricated evidence. Include known shared-staging constraints and preserved test billing records. Do not state that an app is production-ready solely because configuration values exist.

Deliver the branch/PR, deployed URLs, actual checks, remaining owner-only actions and operational guide. Publish only reusable skill content when open-sourcing a workflow; audit the new package for real keys, project identifiers, private sessions, customer data and private repository exports before pushing it.

Sources: [Supabase scheduling](https://supabase.com/docs/guides/functions/schedule-functions), [Sentry alerts](https://docs.sentry.io/product/alerts/), [Sentry data management](https://docs.sentry.io/security-legal-pii/).
