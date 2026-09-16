---
name: gareth-os-operator
description: Run a bounded Gareth OS daily review, or configure its prompt and schedule when requested. Reconcile current evidence into the Daily note and rolling backlog using available authorized read-only connectors.
---

# Gareth OS Operator

Run once when asked to execute the Operator. Use [the portable run procedure](references/portable-run.md). A setup request configures that procedure; it does not itself authorize a recurring schedule or a second run.

Resolve the workspace from the user's path or verified local configuration. Discover the context, backlog, Daily and report locations; do not assume they are at the root. If required input cannot be read, preserve it and continue only independent work.

For setup, infer paths, timezone, enabled capabilities and budgets from current evidence. Ask only for missing choices that affect the requested behavior. Generate a small local launcher that points to this procedure and records the workspace configuration. Back up an existing launcher before replacing it and read back the result. Do not generate a second copy of the whole operating procedure.

Create or change a schedule only when requested. Inspect existing schedules first, use the host's supported scheduling tool, preserve its notification intent, and verify the saved target and cadence. Report unsupported scheduling separately from a successfully saved prompt.

Older connector fragments, OS_CONTEXT template and operator-prompt template are retained as historical source material. They are not active instructions. Do not restore their fixed provider identifiers, old cash thresholds, four-engine defaults, unconditional scheduling, or unreadable-backlog-as-empty behavior.
