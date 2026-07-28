# F1 -- Global Context Files (pass implementation)

**Reference (the why):** `references/anthropic-claude-md.md` (same leanness + specificity principles, applied to Gareth's context files instead of CLAUDE.md).
**Applies to:** `OS_CONTEXT.md` + the 5 global files (`about_gareth.md`, `life_architecture.md`, `operating_principles.md`, `brand_voice.md`, `working_preferences.md`).

## How this pass works

Agentic, not regex-driven. For each check:
- **Framework rule** -- what the principle claims and why it matters for Gareth's OS.
- **Trigger heuristic** -- a fast pattern that surfaces candidates.
- **Agent judgment** -- what to read and reason about before producing a finding.
- **False positives to skip** -- common cases that look like the trigger but are not violations.
- **Finding format** -- every finding includes `reasoning` (1-2 sentences specific to this case).

The agent reads every global file in full, applies every check, and only produces findings the reasoning step confirms.

## Contents

1. [F1.1 -- OS_CONTEXT.md lean budget](#f11--os_contextmd-lean-budget)
2. [F1.2 -- Global file size check](#f12--global-file-size-check)
3. [F1.3 -- Specificity in operating_principles.md](#f13--specificity-in-operating_principlesmd)
4. [F1.4 -- OS_CONTEXT.md current focus freshness](#f14--os_contextmd-current-focus-freshness)
5. [F1.5 -- Platitudes and filler in global files](#f15--platitudes-and-filler-in-global-files)
6. [F1.6 -- Conflicts between global files](#f16--conflicts-between-global-files)
7. [F1.7 -- brand_voice.md engine coverage](#f17--brand_voicemd-engine-coverage)
8. [F1.8 -- life_architecture.md engine dependency map completeness](#f18--life_architecturemd-engine-dependency-map-completeness)
9. [F1.9 -- OS_CONTEXT.md routing vs actual workspace structure](#f19--os_contextmd-routing-vs-actual-workspace-structure)
10. [F1.10 -- Em-dashes in global files (FAIL)](#f110--em-dashes-in-global-files-fail)
11. [Finding schema](#finding-schema)

---

## F1.1 -- OS_CONTEXT.md lean budget

**Framework rule:** OS_CONTEXT.md is the operator's bootstrap file, read every single run. It must stay under 80 lines. Every line past 80 is paid on every scheduled run. The 5 global files are the deep context; OS_CONTEXT.md is the index.

**Trigger heuristic:** `wc -l OS_CONTEXT.md`. > 80 lines = candidate. > 120 lines = strong candidate.

**Agent judgment:**
- Read the file. Is the extra length meaningful routing/constraint content, or is it backstory and context that belongs in the 5 global files?
- A 95-line OS_CONTEXT.md that's mostly routing tables and constraint rules: warn, recommend trimming prose.
- A 130-line OS_CONTEXT.md with whole paragraphs of narrative: fail, recommend moving prose to the relevant global file.

**Severity:** warn > 80 lines, fail > 120 lines.

**Finding format:**
```
OS_CONTEXT.md -- {N} lines
Reasoning: {why the excess is hurting bootstrap cost -- cite what type of content is over the budget}
Action: move {specific section name} to {specific global file}
Citation: passes-global-files.md → F1.1 lean budget
```

---

## F1.2 -- Global file size check

**Framework rule:** each of the 5 global files should be focused. Under 300 lines per file is the target. Beyond 300 lines, the file is likely mixing concerns (identity + strategy + voice in one file, for example).

**Trigger heuristic:** `wc -l {file}`. > 300 lines = candidate.

**Agent judgment:**
- Read the file. Is the length from: (a) real, load-bearing detail -- acceptable; or (b) narrative backstory, repeated context, multiple concerns mixed together -- flag.
- A 350-line `life_architecture.md` that's 80% detailed dependency maps: warn, suggest splitting into architecture + financial-constraints.
- A 400-line `about_gareth.md` that mixes biography, strategy, brand voice, and operating rules: fail, several of those sections belong in the other 4 files.

**Severity:** warn > 300 lines, fail > 500 lines.

---

## F1.3 -- Specificity in operating_principles.md

**Framework rule:** specific constraints earn ~89% compliance from an LLM; vague ones earn ~35%. `operating_principles.md` is the rulebook -- every rule must have a concrete anchor.

**Trigger heuristic:** scan for vague terms:
```
\b(properly|correctly|appropriately|carefully|thoughtfully|as needed|when appropriate|as you see fit|good judgment|best practices)\b
```
Plus known-vague phrases: "be careful", "maintain quality", "keep things organized", "handle edge cases".

**Agent judgment:** for each candidate:
- Is the line a rule or imperative? (Not a heading or example.)
- Does it include a concrete anchor -- an engine name, a financial threshold, a time constraint, a specific tool?
- Example -- "Be careful with cash flow" is vague. "Do not flag Nova Incepta expansion tasks unless GCE + Import/Export combined have 3+ months of operating runway" is specific.
- Is the vagueness irreducible? Some judgment calls are legitimately open-ended. Flag with lower severity if so.

**False positives:** don't flag anchored rules that happen to use these words ("Handle carefully -- see operating_principles.md line 45 for the threshold").

---

## F1.4 -- OS_CONTEXT.md current focus freshness

**Framework rule:** the "Current Focus" section in OS_CONTEXT.md is what the operator uses to route engine activity each run. If it still has template placeholders or stale status lines, every operator run is routing from outdated state.

**Trigger heuristic:** scan for `[e.g.`, `{e.g.`, `TODO`, `TBD`, `[update`, `[fill`, or placeholder brackets `[` immediately followed by content like `"e.g."`.

**Agent judgment:**
- Is the placeholder text still verbatim from the template (the `[e.g. "Q3 corporate pipeline"]` pattern)? Fail -- the section was never filled in.
- Is the status line present but dated more than 30 days ago relative to today? Warn -- likely stale.
- Is the status present and recent? Not a finding.

**Severity:** fail for unfilled placeholders, warn for likely-stale status (> 30 days).

**Finding format:**
```
OS_CONTEXT.md line {N} -- {engine name} current focus is {placeholder or stale}
Reasoning: {why this specific engine's status is missing or stale, and what the operator will do wrong as a result}
Action: update this line to reflect the actual current state of {engine}
Citation: passes-global-files.md → F1.4 current focus freshness
```

---

## F1.5 -- Platitudes and filler in global files

**Framework rule:** instruction-layer files (especially `operating_principles.md` and `working_preferences.md`) are read by an LLM on every relevant run. Every platitude is a token that crowds out the actual rule. Platitudes earn near-zero compliance because they contain no actionable information.

**Trigger heuristic:** scan for:
```
\b(always strive|make sure to|it's important to|keep in mind|don't forget|remember to|feel free to|as always|of course|naturally|obviously)\b
```
Also: closing reminder phrases ("Good luck!", "Feel free to ask questions", "Don't hesitate to"), preamble phrases ("This document is designed to", "The purpose of this file is to").

**Agent judgment:**
- Is the phrase a preamble that could be deleted entirely without losing any constraint? Flag.
- Is the phrase the only signal in a rule ("Make sure to be responsive") with no concrete anchor? Flag.
- Is it a closing note that adds no constraint? Flag.
- Is it embedded in an otherwise-specific rule where it adds emphasis rather than being the whole rule? Lower severity or skip.

---

## F1.6 -- Conflicts between global files

**Framework rule:** the 5 global files are all read by the operator under their respective triggers. If they contradict each other -- especially on engine priorities, tone rules, or operating constraints -- the operator will produce inconsistent output.

**Trigger:** no regex trigger. This is a cross-file synthesis check. Read all 5 files and compare for:
- Contradictions in engine priority order
- Contradictions in the cash-stability rule (is it stated consistently in both `life_architecture.md` and `operating_principles.md`?)
- Brand voice rules in `brand_voice.md` that conflict with output style rules in `working_preferences.md`
- `about_gareth.md` identity claims that don't align with `life_architecture.md` engine descriptions

**Agent judgment:** for each potential conflict:
- Read both passages side by side.
- Is this a genuine contradiction (one says "Nova is secondary to GCE", the other treats them as equal), or a difference in emphasis that's not actually contradictory?
- Only flag actual contradictions, not differences in framing.

**Severity:** fail for contradictions on cash-stability or engine priority; warn for tone/voice inconsistencies.

---

## F1.7 -- brand_voice.md engine coverage

**Framework rule:** `brand_voice.md` should have distinct tone guidance for each engine, since GCE (corporate entertainment), Import/Export (trade), Nova Incepta (creative/music), and AI Backend (technical) require different registers.

**Trigger heuristic:** check that all 4 engine names (or obvious abbreviations) appear in `brand_voice.md`.

**Agent judgment:**
- If an engine is missing, is it because it legitimately uses the same voice as another engine? Acceptable if `brand_voice.md` says so explicitly.
- If an engine section is present but contains only 1-2 lines with no concrete examples or constraints, flag as thin coverage.
- If an engine section has specific examples, register rules, and "do not" items: not a finding.

**Severity:** warn for thin coverage, fail for an engine entirely absent with no explanation.

---

## F1.8 -- life_architecture.md engine dependency map completeness

**Framework rule:** `life_architecture.md` is the funding dependency map. It should explicitly state: which engines fund what, which destabilizes the system, and which accelerates it. Vague or incomplete dependency maps cause the operator to miss cross-engine constraint enforcement.

**Trigger heuristic:** check for the presence of:
- Explicit funding flow statements (e.g., "GCE funds lifestyle")
- What destabilizes the system
- What accelerates the system

**Agent judgment:**
- Is the funding flow directional and explicit? Or is it implied/vague?
- Are all 4 engines covered in the dependency analysis?
- Is the cash-stability constraint (GCE + Import/Export stability before Nova/AI Backend expansion) clearly stated and actionable?

**Severity:** warn for vague dependency descriptions, fail for entirely missing dependencies (e.g., no mention of what destabilizes the system).

---

## F1.9 -- OS_CONTEXT.md routing vs actual workspace structure

**Framework rule:** OS_CONTEXT.md's routing logic must match the actual folder structure in the workspace. If the routing table says engine files live in `Engines\gce\` but that folder doesn't exist, the operator will silently fail to route correctly.

**Trigger:** read OS_CONTEXT.md routing logic section, then compare against actual discovered folders from Step 1.5.

**Agent judgment:**
- Does every engine have a corresponding folder that exists?
- Does every folder path mentioned in OS_CONTEXT.md resolve to a real location?
- Are there engine folders in the workspace that OS_CONTEXT.md doesn't reference?

**Severity:** fail for mismatched paths (OS_CONTEXT.md mentions a path that doesn't exist), warn for undocumented folders.

---

## F1.10 -- Em-dashes in public-facing content (FAIL)

**Framework rule:** Gareth's rule is no em-dashes in public-facing or customer-facing output. Internal files (system docs, operator notes, OS files) are exempt -- em-dashes there are fine.

**Applies to:** global files only when they contain or template public-facing content. `brand_voice.md` and `about_gareth.md` sections describing output for clients, press, or external parties are in scope. Pure system/internal sections (engine routing tables, OS constraints, operator instructions) are out of scope.

**Trigger heuristic:** grep for `--` (em-dash) and `--` (en-dash) in the 5 global files + OS_CONTEXT.md.

**Agent judgment:**
- Is the character inside a code block, URL, or frontmatter? Skip.
- Is the surrounding content clearly internal/system-facing (operator instructions, routing rules, constraint definitions)? Skip -- internal use is fine.
- Is the surrounding content a template for customer output, a brand voice example, a client-facing writing sample, or a public bio? Flag as `fail`.
- Ambiguous prose in a global file: flag as `warn` with a note to check whether it will appear in external output.

**Severity:** `fail` for content that will appear in customer/external output; `warn` for ambiguous prose; skip entirely for internal/system content.

**Auto-fix:** yes for confirmed public-facing instances. Replace `--` → `,` or `:` depending on context. Replace `--` (en-dash) �