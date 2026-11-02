# Product design and verification

## One product language

Respect an approved layout and copy when only color or icons are requested. Centralize surfaces, text, borders, radii and action colors in tokens; landing, pricing, auth, dashboard and standalone widgets should not drift into unrelated themes. A widget shadow root needs its own token bridge.

Use brand colors for identity and primary actions. Use semantic red, amber, green and blue for error/destructive, attention, success/connected and information/progress states. Small violet/teal/orange feature accents are optional. Keep meaning in labels and shapes as well as color. Preserve recognizable provider marks.

Prefer system typography, restrained hierarchy, comfortable targets and short state-driven motion. Respect reduced motion, reduced transparency and increased contrast. Compare competitor flows for useful interaction patterns without copying their product identity or implying endorsement. Apply a dedicated design skill if requested and available.

For pricing, show plan value, actual charges, renewal interval, taxes, limits, retention and cancellation clearly. The subscription picker needs keyboard semantics. Avoid counting a monthly equivalent as the annual checkout charge. Restrict decorative color rather than tinting every panel.

## Component and state practices

Extract shared components and utilities around actual responsibilities. Keep auth/session synchronization out of display components; keep unsaved drafts and selection above conditional views. Fetch independent requests concurrently where useful. Do not add speculative memoization or a global store to shorten prop lists. Use current Vercel React/composition guidance when relevant to the selected framework.

## Behavioral verification

Use tests that would catch a regression, rather than tests that mirror markup or only assert a CSS literal. For auth, billing and isolation changes, include negative paths and server-side decisions. For presentation changes, verify the affected screen plus relevant existing desktop/mobile flows. Follow repository-required lint, type, unit, formatting and build checks.

Exercise 320px layouts and 200% text. A screenshot fitting the viewport does not prove a card has no internal overflow. Test `scrollWidth <= clientWidth` for constrained containers and include a wider fallback font: Linux CI and macOS system fonts can wrap differently. Use `minmax(0, 1fr)`, wrapping flex rows and container-aware price sizing where actual measurements justify them. Do not weaken the assertion to hide clipping.

For dialogs and tabs, verify focus trapping/restoration, nested Escape, arrow/Home/End navigation, touch targets and browser history. Wait for an entrance transform to settle before operating controls inside an iframe when frame-local actionability cannot observe the parent's motion. Avoid arbitrary sleeps.

When CI fails, fetch the exact PR revision and failed test output/artifacts. Reproduce the runner's worker count, environment and fonts as closely as practical. A local pass is not evidence that the linked CI failure is fixed. Push to the same PR and distinguish local validation from a verified green remote run.

Sources: [Vercel React Best Practices](https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices), [Composition Patterns](https://github.com/vercel-labs/agent-skills/tree/main/skills/composition-patterns), [Apple accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility), [WCAG](https://www.w3.org/WAI/standards-guidelines/wcag/).
