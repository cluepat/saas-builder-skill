import { test } from "node:test";
import assert from "node:assert/strict";
import { buildPrompt, resolveStackChoices } from "../docs/prompt-builder.mjs";

test("custom selections use typed values without leaking picker markers", () => {
  const fields = resolveStackChoices({
    framework: "__custom",
    "framework-custom": "SolidJS",
    hosting: "__custom",
    "hosting-custom": "My own server",
    backend: "Firebase",
    payments: "__custom",
    "payments-custom": "Regional provider",
  });
  const prompt = buildPrompt(fields);
  for (const value of [
    "SolidJS",
    "My own server",
    "Firebase",
    "Regional provider",
  ])
    assert.ok(prompt.includes(value));
  assert.doesNotMatch(prompt, /__custom/);
});

test("switching away from custom ignores previously typed values", () => {
  const fields = resolveStackChoices({
    framework: "Vue + TypeScript",
    "framework-custom": "Old choice",
    payments: "None",
    "payments-custom": "Old provider",
    hosting: "__custom",
  });
  const prompt = buildPrompt(fields);
  assert.match(prompt, /Vue \+ TypeScript/);
  assert.match(prompt, /Omit checkout/);
  assert.match(prompt, /Deployment host: Not selected/);
  assert.doesNotMatch(prompt, /Old choice|Old provider|__custom/);
});

test("unspecified choices do not silently select the reference stack", () => {
  const prompt = buildPrompt();
  assert.match(prompt, /Clarify the target user/);
  assert.match(prompt, /Not selected; clarify whether billing is needed/);
  assert.doesNotMatch(prompt, /React|Cloudflare|Supabase|Dodo/);
});

test("Vue, Vercel and Stripe choices are carried into the prompt", () => {
  const prompt = buildPrompt({
    product: " Feedback portal ",
    framework: "Vue + TypeScript",
    hosting: "Vercel",
    backend: "Supabase",
    payments: "Stripe",
  });
  assert.match(prompt, /Product: Feedback portal\n/);
  for (const choice of ["Vue + TypeScript", "Vercel", "Supabase", "Stripe"])
    assert.ok(prompt.includes(choice));
  assert.match(prompt, /rendering model, deployment runtime, SDK/);
});

test("arbitrary stacks are accepted without a predefined connector list", () => {
  const prompt = buildPrompt({
    framework: "Angular",
    backend: "Django + PostgreSQL",
    hosting: "My own Kubernetes cluster",
    payments: "Regional provider",
  });
  for (const choice of [
    "Angular",
    "Django + PostgreSQL",
    "My own Kubernetes cluster",
    "Regional provider",
  ])
    assert.ok(prompt.includes(choice));
});

test("no payments omits billing setup and test-payment instructions", () => {
  for (const payments of ["None", "no payments yet", "OFF"]) {
    const prompt = buildPrompt({ payments });
    assert.match(
      prompt,
      /Omit checkout, subscription products and billing-provider setup/,
    );
    assert.doesNotMatch(prompt, /use test payments/);
  }
});

test("existing products preserve unspecified choices", () => {
  const prompt = buildPrompt({ existing: true, framework: "Angular" });
  assert.match(prompt, /extend this existing SaaS/);
  assert.match(prompt, /Preserve the existing choice/);
  assert.match(prompt, /explain any required migration/);
  assert.doesNotMatch(prompt, /recommend a compatible option/);
});

test("client invocation matches plugin and standalone installation", () => {
  for (const [client, expected] of Object.entries({
    codex: "Use $saas-builder to",
    "claude-code": "/saas-builder:saas-builder",
    "claude-standalone": "/saas-builder",
    cursor: "/saas-builder",
  })) {
    assert.ok(buildPrompt({ client }).startsWith(expected + " "));
  }
  assert.throws(() => buildPrompt({ client: "unsupported" }), RangeError);
});
