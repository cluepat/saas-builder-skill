# Workspace collaboration and invitations

Use this reference when the product needs shared accounts, teammates or included seats. Do not add collaboration to a single-user product merely because the reference exists. Choose roles, limits and grace policies for the actual product; none of the example stack's prices or seat counts are defaults.

## Access and state boundaries

Define an operation matrix before implementing roles. Separate viewing and contributing from administration, deletion, integrations setup and payments. Enforce the same decisions in server handlers, database policies and narrow privileged operations; hiding controls is not authorization. A member's allowed operation must also verify that its resource belongs to the selected accessible workspace.

Treat the active-workspace header/parameter as a request, never proof of access. Joining a shared workspace must not silently transfer personal projects, ownership or subscriptions. Charge usage and resolve entitlements against the selected workspace. Where members can consume pooled allowances, show which workspace they belong to, usage/limits/reset dates and actionable owner guidance; exclude payment details and billing controls unless their role permits those operations.

Scope loaded records, private evidence, drafts, selection and in-flight requests to both signed-in identity and workspace. On switch, close or deliberately scope detail dialogs, clear incompatible drafts and ignore late responses. Token renewal should not accidentally reset drafts or refetch an entire workspace. Removal/suspension must reject subsequent requests; already-issued signed URLs remain accessible until their expiry unless the storage design supports earlier revocation.

Keep contribution attribution after removal. Save a stable author identity and suitable display data without falsely labeling everyone as an owner or exposing unrelated account details. Decide whether teammate emails are visible to other members; apply that directory policy server-side.

## Invitation lifecycle

For email-bound invitations, require sign-in with the intended verified email before revealing private invitation context or joining. Support new accounts, existing accounts and configured social providers. Preserve the pending invitation through auth callbacks without accepting it automatically. Show the workspace, inviter, role, expiry and current account clearly; provide wrong-account, expired, missing-link and retry paths. Joining is explicit and must not start checkout.

Use database-backed versioned invitations with expiry, revocation and single-use acceptance. A server-signed link can bind invitation ID, version and expiry while recipient details remain in the database; an equivalent opaque-token design must store only an appropriate hash. Do not log raw bearer tokens or retain them in visible URLs/analytics after capture. Use the provider's supported secure auth-state/callback mechanism. Browser-only memory may cover storage failures, but do not claim cross-reload persistence where it cannot exist.

Normalize recipient addresses according to the auth provider's identity rules. Prevent duplicate pending invitations. Reserve seats for unexpired pending invitations if that is the product policy. Serialize reservations and acceptance atomically against workspace capacity, including concurrent final-seat attempts and the owner counted once. Expired/revoked reservations must not consume seats.

Resending should renew expiry and invalidate old links. Replayed acceptance by the same existing member should be harmless; it must not restore an explicitly removed member through a stale invitation. A delivery failure must preserve a valid invitation and copyable link, with retryable status. Use bounded delivery leases and provider idempotency where available. Freeze the recipient and rendered payload for an idempotency key; changing workspace names or templates midway through a retry can conflict with the provider. Respect the provider's idempotency window rather than blindly reusing a key forever.

## Seats and plan transitions

Define who counts: owner, active members, invitations, suspended members and guests may have different rules. Keep a seat grace period separate from data-retention grace. If excess members retain temporary access after downgrade, persist its deadline once, let the owner select retained access if supported, and define deterministic fallback ordering. Enforce the deadline during authorization, not only in a scheduled job. Repeated webhooks/page visits must not restart grace. Natural subscription expiry and webhook-driven changes should converge on the same policy.

Block new reservations/joins above current capacity. Define which pending invitations are revoked when limits shrink. Upgrades may restore plan-suspended members within capacity; do not automatically restore explicitly removed or departed members. Preserve accounts and contributions when access is suspended. Ownership transfer and owner departure need their own policy and must not emerge accidentally from a generic leave endpoint.

## Verify and roll out

Cover owner/member permissions, cross-workspace resources and private assets, direct database restrictions, shared quota attribution, removed/suspended access, draft isolation and delayed responses. Exercise verified-email mismatch, callback recovery, expiry/revocation/resend, delivery retries, replayed acceptance and concurrent capacity changes. Include repeated billing events, natural expiry, grace deadlines and upgrade restoration.

Apply additive schema/policy changes first, then dependent API, then clients. Preserve legacy personal-workspace behavior deliberately where required. Document private sender/signing configuration separately from frontend variables and test with authorized disposable accounts; mocked mail delivery does not prove real delivery.
