# Subscription billing and live activation

## Product contract and server entitlements

Choose plan names, prices, currency, billing intervals, quotas, retention and downgrade behavior with the owner. Monthly and annual billing are useful defaults; weekly plans are not a universal requirement. The public pricing page, provider products and server allowances must agree. An annual display may show a monthly equivalent, but checkout must charge the correct annual total.

Enforce paid features, resource creation and usage limits on the server. Update shared usage counters atomically at acceptance, not by counting a filtered UI list. Decide UTC/calendar or subscription-period resets explicitly. Deleting an item may release storage but should not silently restore a consumed submission allowance unless that is the product's rule.

Derive billing workspace/customer IDs from authenticated ownership. Keep payment API and webhook signing secrets server-side. A checkout redirect must never activate a paid plan. Signed webhooks and verified canonical provider state determine entitlement. Handle duplicate, delayed, out-of-order and superseded-subscription events. Define active, renewal, scheduled cancellation, failed, past-due, on-hold, paused and expired behavior deliberately.

## Checkout reservations

Serialize checkout creation per workspace. Reuse a compatible open session to avoid duplicate subscriptions. On an ambiguous provider timeout, retain the reservation, inspect provider state and reconcile before creating another session. Distinguish expired/cancelled checkout from “request returned an error.”

**Persist environment identity.** Associate checkout intents and provider customer/subscription bindings with provider and mode, not just workspace. Resume a saved checkout only when mode, interval, relevant product mapping and ownership match the current request. Validate the returned checkout origin against the provider's documented origins for that mode. Never return a `test.checkout` URL after switching to live mode.

During migration from an implementation without mode metadata, classify existing bindings and open sessions before cutover. Do not infer that all records are disposable. A saved test session can survive a server environment change and be resumed by the app. Expiring only its local reservation does not revoke the provider's old URL. Inspect ambiguous sessions; get authorization for any existing-record reset and preserve unrelated data and the requested retention grace period.

## Dodo reference setup

Use current Dodo documentation or its connected tools for fields and dashboard paths. Treat the following as configuration requirements, not frozen API payloads:

- Separate recurring monthly/annual products in the chosen currency, with the correct repeat frequency, trial policy and ongoing duration. Frequency and total subscription duration are different settings.
- A product collection when monthly/annual self-service switching is intended. Review upgrade/downgrade timing, proration and failed-change behavior rather than inheriting dashboard defaults blindly.
- A hosted customer portal for the product's cancellation policy, invoices and payment-method updates. Prevent unintended multiple subscriptions per workspace/customer.
- Test/live API keys, product IDs, customer IDs and webhook secrets from the same environment. Dodo's browser OAuth plugin does not replace the application's server-side API key.
- An HTTPS webhook subscribing to the required subscription lifecycle events. Verify Standard Webhooks signature, timestamp and bounded raw body before processing.

A shared Supabase function may need `verify_jwt=false` for external provider callbacks. In that arrangement, every private route must independently authenticate and authorize the Supabase bearer token; only external callback routes use provider signatures instead.

## Cutover order

1. Verify merchant approval and the intended live business/account.
2. Read the existing live products, webhook endpoints and portal settings. Prepare missing resources without duplicating existing ones.
3. Verify the deployed schema/API and production return URL. Review existing test bindings and open checkout intents.
4. Save the live API key, live product IDs and the new endpoint's signing secret privately in the production backend. Verify presence/matching identifiers without printing secrets.
5. Enable live mode only when those values are ready and the user has authorized the change. Retain staging in test mode.
6. Verify the new checkout's mode, currency, amount and interval on a workspace with compatible billing state. Distinguish a configured checkout from a paid transaction verified by a signed webhook.

Installing a plugin, creating products and changing configuration do not prove successful charging. Real payments/refunds and changes to existing subscriptions are consequential actions; use the applicable authorization and do not perform them just to complete a checklist. If the owner wants test records preserved, document how those specific workspaces are excluded from live validation.

Sources: [Dodo checkout](https://docs.dodopayments.com/developer-resources/checkout-session), [subscriptions](https://docs.dodopayments.com/developer-resources/subscription-integration-guide), [test/live separation](https://docs.dodopayments.com/miscellaneous/test-mode-vs-live-mode), [product collections](https://docs.dodopayments.com/features/product-collections), [official agent plugin](https://github.com/dodopayments/dodo-agent-plugin).
