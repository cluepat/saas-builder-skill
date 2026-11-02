const invocation = {
  codex: "Use $saas-builder to",
  "claude-code": "/saas-builder:saas-builder",
  "claude-standalone": "/saas-builder",
  cursor: "/saas-builder",
};

export function buildPrompt(options = {}) {
  const client = options.client || "codex";
  if (!Object.hasOwn(invocation, client))
    throw new RangeError("Unknown client");
  const value = (key) => (options[key] || "").trim();
  const existing = Boolean(options.existing);
  const unresolved = existing
    ? "Preserve the existing choice; inspect the repository."
    : "Not selected; recommend a compatible option with reasons.";
  const payments = value("payments");
  const noPayments = /^(none|no payments(?: yet)?|off)$/i.test(payments);
  return `${invocation[client]} ${existing ? "extend this existing SaaS" : "build a SaaS"}.
Product: ${value("product") || "Clarify the target user and first complete user flow."}

Frontend framework: ${value("framework") || unresolved}
Backend, database, auth and storage: ${value("backend") || unresolved}
Deployment host: ${value("hosting") || unresolved}
Payments: ${noPayments ? "None. Omit checkout, subscription products and billing-provider setup." : payments || (existing ? unresolved : "Not selected; clarify whether billing is needed.")}

${existing ? "Inspect the repository first. Preserve existing behavior and unspecified stack choices; explain any required migration before making it." : "Honor the choices above. Clarify consequential gaps before scaffolding; do not silently substitute the reference stack."}
Check the rendering model, deployment runtime, SDK and provider compatibility.
Use the selected framework's own component, state and testing practices.
Build one complete user flow, then connect and verify the deployed service.
Keep staging data separate from production${noPayments ? "." : "; use test payments if billing is needed."}
Keep private credentials out of chat. Report implemented, deployed, configured
and verified states separately.`;
}
