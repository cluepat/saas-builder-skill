# Optional integrations

Implement only integrations needed by the product. Check the current official documentation and installed provider tools before using a remembered API or installing another SDK.

## Transactional email / Resend

An inbox on Google Workspace and a transactional email provider solve different problems. Keep the existing mailbox MX records while adding the provider's required DNS verification records. Use a verified sending domain/subdomain and monitor delivery/bounces. Configure the auth service's SMTP settings when it sends auth emails; placing a Resend key on the frontend host does not connect Supabase Auth to SMTP.

Keep confirmation and recovery templates visually consistent, with the correct flow-specific link and a fallback URL. Never publish an actual verification link in documentation or screenshots. Confirm the deployed auth return URL, sender and delivery in an owned inbox. Test fixtures that mock SMTP do not prove email delivery.

## GitHub App issue creation

The SaaS operator configures one GitHub App, its private key, client credentials, callback/webhook and scheduled worker. Customers authorize installation on selected repositories; do not ask every customer to create their own App. Store installation connections per tenant and retrieve only authorized repositories with Issues available.

Manual creation should remain available when configured. For automatic creation, persist the selected rule and test with a new eligible submission after saving. Verify both enqueueing and worker execution; a connected installation badge proves neither. Use retries with bounded attempts and inspect failure/exhaustion. A secret-protected scheduled worker must actually be provisioned, not just implemented in source.

Deleting local records should not silently delete third-party issues. Explain linked-resource consequences in the confirmation UI and implement only the chosen behavior. Support disconnect/reconnect and repository refresh as distinct actions, with connected/success states visually clear.

## External website widget

Keep the loader small; lazy-load expensive capture code. Preserve module base URLs when the API is hosted elsewhere. Validate public installation keys, allowed origins and payload limits on the backend. Exercise an installed widget on another origin, not only a same-origin playground.

Install opt-in diagnostic instrumentation before the events occur and bound its memory use. Differentiate host-page console/network diagnostics from the widget's own Sentry failures. Maintain consent, screenshot review and configured exclusion selectors. Do not assume a screenshot is redacted merely because text fields are masked.

Keep the public demo isolated from real ingestion, auth, paid checkout and third-party issue creation. Make example actions obvious without turning fictional output into claims of an implemented feature.

Sources: [Resend domains](https://resend.com/docs/dashboard/domains/introduction), [Supabase SMTP](https://supabase.com/docs/guides/auth/auth-smtp), [GitHub Apps](https://docs.github.com/en/apps/creating-github-apps/about-creating-github-apps/about-creating-github-apps).
