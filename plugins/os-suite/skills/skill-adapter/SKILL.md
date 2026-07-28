---
name: skill-adapter
description: Adapt, improve, repair, simplify, or extend an existing Claude skill without rebuilding it from scratch. Use when the user says "adapt this skill", "modify this skill", "improve this skill", "fix this skill", "rewrite this skill", "add a layer to this skill", "remove clutter from this skill", "make this skill interview me first", "change how this skill behaves", "keep the useful parts but change the process", "turn this skill into a better version", or pastes a detailed change proposal for an existing skill. Use skill-creator instead when no skill exists yet.
---

# Skill Adapter

Adapts an existing skill. Preserves what works. Changes only what improves it.

## Routing with skill-creator

- No existing skill yet → use `skill-creator`.
- Skill exists and needs change → use this skill.
- User pastes a detailed change-proposal prompt referencing an existing skill → use this skill in **Change-Proposal Mode** (skip interview, treat the proposal as the brief).

## Core principle

Do not assume the user wants a new skill. Assume they want to preserve useful parts and change specific behaviours, outputs, workflows, decision rules, formatting, or interaction layers. Protect what works. Modify only what improves the skill.

## When to use

User says: adapt / modify / improve / fix / rewrite this skill; add a layer; remove clutter; make it interview me first; change how it behaves; keep the useful parts; turn this into a better version. Or: user pastes a detailed change-proposal document (like a "Skill Adapter Guide" PDF) referencing an existing skill.

## When not to use

- No existing skill yet → `skill-creator`.
- User wants a skill description-only optimization with no behaviour change → `skill-creator` (description improver).
- User wants to install or scaffold a plugin → `create-cowork-plugin`.

## Modes

### Mode 1 — Compact (default)

User wants a quick adaptation. Ask 6 questions, batched in 1–2 `AskUserQuestion` calls (max 4 options each):

1. What is the skill supposed to do?
2. What do you want to keep?
3. What is annoying, cluttered, or not working?
4. What new behaviour do you want added?
5. What should happen silently under the hood instead of being shown?
6. What should the final output look like?

### Mode 2 — Deep Audit

User says "audit this skill", "serious improvement pass", "full review". Walk seven sections — Current Purpose, What Works, What Doesn't, User Friction, Desired Changes, Output Design, Guardrails. Batch questions through `AskUserQuestion`. Never dump all questions at once.

### Mode 3 — Change-Proposal Mode

User pastes a detailed change spec (PDF, markdown brief, prompt). Skip the interview. Treat the spec as the change brief. Run diagnosis against the spec. Present the iteration plan. After each rewrite pass, self-check against the spec and iterate until aligned. Only ask the user when the spec is silent on a decision that affects behaviour.

## Workflow

### Phase 1 — Confirm and read the existing skill

1. Identify which skill. If unclear, ask.
2. Resolve its path. Skills live under either:
   - `C:\Users\Gaming Pc\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\...\skills\<name>\SKILL.md` (user-skills + Anthropic skills)
   - `C:\Users\Gaming Pc\AppData\Roaming\Claude\local-agent-mode-sessions\486a8f4f-c7d3-4dfb-a3ce-908dffc91b8a\ce707f27-f4dd-49ec-96de-8fee939d7483\rpm\plugin_<id>\skills\<name>\SKILL.md` (installed plugins)
3. Read the full SKILL.md and any referenced files in `scripts/`, `references/`, `assets/`.
4. If user only described the skill but did not point to the file, build a provisional plan and mark it provisional.

### Phase 2 — Backup (mandatory)

Before any rewrite, copy the original to `SKILL.md.bak-YYYY-MM-DD` in the same folder. Never skip. If the folder is read-only, this step gates Phase 3 — fork instead (see below).

### Phase 3 — Fork rule for read-only skills

If the skill lives under an Anthropic-shipped path (read-only — verified by attempting backup and observing permission), do NOT overwrite. Fork to user-skill space:
- New path: `C:\Users\Gaming Pc\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\...\skills\<original-name>-adapted\SKILL.md`
- Rename `name:` frontmatter to match the new folder.
- Note the fork in the changelog.

### Phase 4 — Interview (or skip in Change-Proposal Mode)

Run the mode's questions. Use `AskUserQuestion` for batched multi-choice. Free-text only when no fixed option set fits.

### Phase 5 — Diagnosis

Produce a clear, practical diagnosis. Nine points:

1. Current skill purpose
2. User's requested changes
3. What to preserve
4. What to modify
5. What to remove
6. What to hide under the hood
7. What new workflow should be added
8. Risks or possible conflicts
9. Recommended adaptation approach

Add three Gareth-specific checks:

10. **Description-field audit** — does the `description:` frontmatter contain the trigger phrasing the user actually uses? Cross-reference `about_gareth.md` and `working_preferences.md` for voice patterns. List any trigger gaps.
11. **OS alignment check** — does the adapted skill respect `operating_principles.md`, `brand_voice.md`, `working_preferences.md`? Flag any conflicts.
12. **Skill-creator overlap** — would this change be better served by re-running `skill-creator` from scratch? If yes, recommend that and stop.

### Phase 6 — Approval gate

Single question: *"Preserve X, remove Y, add Z, hide W. Confirm before I rewrite?"* Wait for explicit yes before touching the file.

### Phase 7 — Rewrite

Apply the 13-element rewrite spec: name, purpose, when to use, when NOT to use, inputs needed, interview flow, audit flow, adaptation logic, hidden-logic rules, visible-output rules, approval gates, final output formats, test prompts.

Apply the 10 adaptation rules:

1. Preserve the original purpose unless the user changes it.
2. Preserve working instructions.
3. Remove redundant or irrelevant sections.
4. Convert visible internal logic into hidden logic where appropriate.
5. Add interview layers when the skill depends on user preferences.
6. Add approval gates when the skill could take action, create files, send messages, or change systems.
7. Add audit layers when the user reports errors or recurring problems.
8. Add output controls when the user complains about clutter.
9. Add priority or triage logic only when it helps the user choose what to do next.
10. Keep final output operational, not theoretical.

### Phase 8 — Dry run

Run one of the suggested test prompts through the adapted skill *in the current conversation* before declaring done. If the trigger fails or the behaviour drifts, iterate once. In Change-Proposal Mode, self-check against the original spec instead.

### Phase 9 — Deliver

Default output bundle:

1. Summary of what changed
2. Clean final SKILL.md (already written to path)
3. Changelog
4. Notes on what is hidden under the hood
5. Suggested test prompts
6. Rollback command (path to the `.bak` file)

## Hidden Logic Rule

These run silently — never appear in user-facing output unless they affect the user's next decision:

priority scoring, routing rules, internal audit checks, contradiction checks, decision hierarchy, failure mode detection, clause matching, confidence estimates, quality control checks.

Bad: *"3B clause triggered due to priority conflict."*
Good: *"Suggested priority: High. Reason: this affects a client response and may block the next step."*

## Visible Output Rule

Prefer: short summaries, clear recommendations, practical next steps, decision menus, before-and-after comparisons, rewritten skill sections, implementation-ready files.

Avoid: internal labels, hidden clause names, overlong process explanations, repeated diagnostic notes, bulky framework text unless requested.

## Output Options

After diagnosis, ask which output the user wants (skip if already specified):

1. Rewrite the full skill
2. Rewrite only the changed sections
3. Produce a patch list
4. Produce a Claude prompt to make the changes
5. Produce a changelog and implementation plan
6. Produce a cleaned-up final SKILL.md
7. Produce a questionnaire layer only
8. Produce an audit layer only
9. Produce a side-by-side diff of changed sections only

## Complaint Translation

User pain → design fix.

| User says | Interpret as |
|---|---|
| "Takes up too much space" | Reduce visible output. Move internal logic under the hood. |
| "Keeps showing the same clause" | Clause may still run, but hide it from user-facing output. |
| "Doesn't ask enough questions" | Add an interview layer before execution. |
| "Asks too many questions" | Use progressive questioning. Minimum required only. |
| "Jumps straight into drafting" | Add a pre-draft alignment step. Require approval before drafting. |
| "I need to see priorities first" | Add a priority summary stage before action generation. |

## Approval Gates

Always gate before: rewriting a major file, removing a section, creating a final deliverable, generating client-facing text, drafting an email, sending a message, changing a workflow, updating a system, making a recommendation that affects business operations.

Gate format: *"Before I rewrite the skill, confirm: preserve X, remove Y, add Z?"*

## Default Behaviour

Vague request → ask the 5 baseline questions (what skill, what's wrong, what to keep, what to change, what to hide) then proceed.

Clear request → diagnosis → approval gate → rewrite.

Change-proposal pasted → diagnosis against the proposal → approval gate → rewrite → self-iterate against the proposal.

## Hard Rules

- Never rewrite the whole skill blindly from scratch.
- Never remove useful behaviour just because the user didn't mention it.
- Never expose hidden internal logic unless the user asks to see it.
- Never overpopulate visible output with procedural clauses, internal labels, audit codes, or diagnostic scaffolding.
- Never produce final skill files before understanding what the user wants changed — unless they explicitly ask for an immediate draft.
- Never skip the backup.
- Never overwrite a read-only Anthropic skill — fork instead.

## Test Prompts

- "Adapt this email scanner skill so it summarizes priority first and does not draft until I approve."
- "Audit this skill and tell me what is cluttered, what is useful, and what should be hidden under the hood."
- "Keep the current workflow but add an interview layer before execution."
- "Rewrite this skill so the visible output is cleaner but the internal quality checks still run."
- "Modify this skill so it asks what I am happy with and unhappy with before making changes."
- "Here is a detailed change proposal for `email-scanner-ge` — iterate on it until aligned."

## Final Instruction

Interview first. Audit carefully. Preserve value. Remove clutter. Hide internal mechanics where appropriate. Produce clean, practical, implementation-ready adaptations.
