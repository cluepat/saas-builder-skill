# Maintaining context across tasks

Use when a product grows across multiple chats or an implementation needs a handoff. Start from existing repository instructions and docs; update them instead of creating competing summaries. Keep this product-specific context in the project, not in the installed generic skill.

## Small maintained context, not a conversation archive

Maintain a concise entry point linked from the repository instructions or README. It should route a new task to:

- Product purpose, current implemented capabilities and links to feature guides.
- Architecture, canonical source locations, entry points and environment separation.
- Current design source of truth, shared components/tokens and approved layouts.
- Plan/role boundaries, core security/privacy invariants and behavior to preserve.
- Relevant checks and setup/smoke-test guides, with implementation/deployment/configuration/verification distinguished.
- A short roadmap separating selected work from ideas and explicit exclusions.

The optional [project context template](../assets/project-context.md) provides these headings. Adapt names and structure to the repository. Do not duplicate every feature guide in the overview, load all references by default, or preserve an entire chat transcript. Keep secrets, live tokens, private user records and real customer evidence out.

## On entry to a new task

Read the overview and only the guides/source/tests relevant to the requested slice. Inspect current Git state rather than trusting a historical branch name. Verify code against documentation before building a supposedly missing feature. Deferred ideas are not authorization to implement them. Existing design tokens and recent accepted decisions take precedence over an old reference aesthetic; resolve contradictory guidance instead of copying it forward.

Preserve the owner's requested Git/deployment workflow. A handoff should record that boundary without turning one project's preference into a universal skill restriction. Do not infer authorization to send email, mutate production data, publish or deploy from a request to document the project.

## On completion or interruption

Update the feature guide when behavior, authorization, configuration, rollout or verification changes. Update the overview for product/architecture/plan decisions and the roadmap for agreed scope/completion. Remove superseded statements where they would mislead the next task; do not merely append a contradictory paragraph.

Keep temporary task state in a separate short handoff when work is unfinished: goal, branch/base, decisions, completed/remaining steps, exact failure/reproduction, checks run and blockers. Link it only while active. Stable project context should not imply a particular dirty tree or live deployment. Historical test totals are not current guarantees; point to CI and record exact validation for the actual revision.

A useful new-chat prompt is: “Read the repository instructions and project overview, then only the guides/source for [task]. Preserve existing behavior and the recorded workflow. Implement, verify and update the relevant docs.”
