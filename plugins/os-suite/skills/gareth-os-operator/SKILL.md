---
name: gareth-os-operator
description: Build and schedule a personalized Operator prompt for Gareth's 4-engine AI OS. Reads OS_CONTEXT.md as a lean bootstrap file instead of all 5 global files. Full global files are deep-read on-demand only. Uses Cowork file tools (Read/Write/Edit) instead of vault MCP. Engine scope replaces team profile scope (GCE, Import/Export, Nova Incepta, AI Backend). Use when Gareth says "set up the operator", "build my operator prompt", "schedule my OS", "os operator", or runs /gareth-os-operator.
---

# Gareth OS Operator

Build a personalized Operator prompt that runs Gareth's 4-engine AI Operating System on a recurring schedule. The Operator is a fully autonomous maintenance agent — one session = one run, no questions, no confirmations, executes and reports.

This skill does **four** jobs, in order:

1. **Discover** what the OS already knows. Read `OS_CONTEXT.md` (the lean bootstrap file) and workspace structure silently. The full 5 global files are only read if `OS_CONTEXT.md` does not yet exist.
2. **Ask only the gaps.** Cadence, connectors, budgets. Don't re-ask anything Phase 0 already pulled from the context file.
3. **Render and save** the personalized operator prompt locally.
4. **Schedule it.** Hand off to the `schedule` skill so the trigger is wired before the run ends.

## Reference files

- `references/operator-prompt-template.md` — the parameterized prompt adapted for Gareth's 4-engine system.
- `references/connector-fragments.md` — spliceable body blocks per connector (Todoist, Gmail, Google Calendar, HubSpot, QuickBooks).
- `references/OS_CONTEXT_template.md` — the template Gareth fills in once to create `OS_CONTEXT.md`.

Read both reference files before generating output.

---

## Phase 0 — Silent discovery (no questions, no MCP calls)

The user invokes this skill from inside their workspace folder. Everything here is filesystem-only. Do NOT call any vault MCP tools.

1. **Verify the workspace folder exists.** The workspace is at `C:\Users\Gaming Pc\Documents\Claude\Projects\Gareth Master AI Operating System Build`. If you cannot reach it, tell Gareth and stop.
2. **List the workspace folder contents.** `Glob` pattern `**/*` at the workspace root. Cache the result as `{{WORKSPACE_FILES}}`.
3. **Read OS_CONTEXT.md if it exists** at `C:\Users\Gaming Pc\Documents\Claude\Projects\Gareth Master AI Operating System Build\OS_CONTEXT.md`.
   - If it exists: read it. This is the only file you need for bootstrap. Do NOT read the 5 global files unless a specific section is missing or a deep-read trigger is hit (see below).
   - If it does NOT exist: read the 5 global files as a fallback (`about_gareth.md`, `life_architecture.md`, `operating_principles.md`, `brand_voice.md`, `working_preferences.md`), then offer to generate `OS_CONTEXT.md` from them before proceeding.
4. **Cache inferred values:**
   - `{{ORG_NAME}}` ← "Gareth Cohen" (always — this is a solo OS)
   - `{{ENGINES}}` ← the 4 primary engines, in order: "Gareth Cohen Experience (GCE)", "Import/Export", "Nova Incepta", "AI Backend". Confirm from `life_architecture.md` if present; these are the defaults if not.
   - `{{OPERATOR_NAME}}` ← "Gareth OS Operator"
   - `{{OPERATOR_HANDLE}}` ← "gareth-os-operator"
   - `{{WORKSPACE_PATH}}` ← `C:\Users\Gaming Pc\Documents\Claude\Projects\Gareth Master AI Operating System Build`
   - `{{OPERATOR_PROMPT_PATH}}` ← `{{WORKSPACE_PATH}}\operator-prompt.md`
   - `{{DAILY_FOLDER}}` ← `{{WORKSPACE_PATH}}\Daily`
   - `{{ENGINE_FOLDER}}` ← `{{WORKSPACE_PATH}}\Engines`
   - `{{REPORTS_FOLDER}}` ← `{{WORKSPACE_PATH}}\Reports`
   - `{{TASK_LIST_PATH}}` ← `{{WORKSPACE_PATH}}\task-list.md`
   - `{{SIGNATURE_BG_COLOR}}` ← `#1a1a2e` (dark navy — Gareth's default)
   - `{{SIGNATURE_FG_COLOR}}` ← `#e0e0e0`
   - `{{NO_EM_DASH}}` ← `true` (hard rule from working_preferences.md — no long dashes in any output)

5. **If OS_CONTEXT.md did not exist and you just read the 5 global files,** offer to auto-generate `OS_CONTEXT.md` now from what you found. If Gareth confirms, write it to `{{WORKSPACE_PATH}}\OS_CONTEXT.md` using `references/OS_CONTEXT_template.md` as the structure, pre-filled with the values inferred from the 5 files. This saves tokens on every future run.

After Phase 0, summarise to Gareth in 4 short lines what you found. Format:

> **Discovered from your OS:**
> - Context source: OS_CONTEXT.md (lean) OR 5 global files (fallback)
> - Engines: GCE, Import/Export, Nova Incepta, AI Backend
> - Workspace: `{{WORKSPACE_PATH}}`
> - Operator path (proposed): `{{OPERATOR_PROMPT_PATH}}`
>
> Anything to override? (Type the field name, or say "looks good" to continue.)

If Gareth wants overrides, accept them inline (one short follow-up) and update the cache. If "looks good", proceed straight to Phase 1.

**Do not re-ask any of the above as standalone questions.** They were inferred. Phase 1 is for things the OS genuinely cannot tell you.

---

## Phase 1 — Ask only the gaps

These are the questions the global files cannot answer. Ask one at a time with `AskUserQuestion`.

### Q1 — Cadence

`AskUserQuestion` with options:

- **Daily** — one run per day at 9am. Best for solo operators.
- **Every 4 hours** — balanced. Catches new activity without spamming.
- **Weekly** — one run per week. Lightweight strategic review only.
- **Custom** — Gareth types a cron expression or phrase.

Save as `{{CADENCE_HUMAN}}` and `{{CADENCE_TAG}}`.

### Q2 — Connectors (probe live, do not just ask)

Don't show Gareth a checklist and trust the answer. **Probe what's actually wired up in this environment**, then confirm.

#### Step 2a — Detect

Inspect the running session's available tools. Look for tool names matching these patterns:

| Category | Detection signal | Live probe (read-only) |
|----------|------------------|------------------------|
| **Todoist** | `mcp__705db4b6*` tools present | Call `find-tasks` with `filter: "today"`. Success = response, no auth error. |
| **Gmail** | `mcp__c41a480a*` tools present | Call `search_threads` with `query: "in:inbox"`, `maxResults: 1`. Success = response. |
| **Google Calendar** | `mcp__b14f2bc0*` tools present | Call `list_calendars`. Success = response. |
| **HubSpot** | `mcp__6ef50a34*` tools present | Call `get_user_details`. Success = response. |
| **QuickBooks** | `mcp__7591fefd*` tools present | Call `company-info`. Success = response. |

Run all detected probes **in parallel** in one batch. Narrate before the batch and after.

For each connector:

- ✅ **Found and probe succeeds** → mark enabled. Capture the MCP namespace prefix as `{{*_MCP_NAME}}`.
- ⚠️ **Found but probe fails** (auth error, 401, empty creds) → mark "wired but broken". Tell Gareth the exact error and ask: (a) skip, (b) pause to fix, or (c) include anyway.
- ❌ **Not found** → mark disabled. Do not ask "do you want to add it?" — that is a separate setup task.

#### Step 2b — Confirm with Gareth

Show one summary block:

> **Connectors detected:**
> - ✅ Todoist — tasks found
> - ✅ Gmail — inbox accessible
> - ✅ Google Calendar — calendars found
> - ✅ HubSpot — account accessible
> - ❌ QuickBooks — not detected
>
> Use these in the Operator? (yes / customize)

If "customize", let Gareth toggle individual entries off. If "yes", proceed.

#### Save

- `{{TODOIST_ENABLED}}`, `{{GMAIL_ENABLED}}`, `{{CALENDAR_ENABLED}}`, `{{HUBSPOT_ENABLED}}`, `{{QUICKBOOKS_ENABLED}}`
- `{{TODOIST_MCP}}` ← `mcp__705db4b6-de70-4704-b17f-355c44f83853`
- `{{GMAIL_MCP}}` ← `mcp__c41a480a-54d1-476d-a0a1-9b70bc538b81`
- `{{CALENDAR_MCP}}` ← `mcp__b14f2bc0-691c-4c9d-bb91-d0be78a116cf`
- `{{HUBSPOT_MCP}}` ← `mcp__6ef50a34-9341-4e5f-bb7f-df0db663dc88`
- `{{QUICKBOOKS_MCP}}` ← `mcp__7591fefd-1363-48f5-a4aa-720af9e9adb5`

Probes are read-only. Never invoke a write/send tool during detection.

### Q3 — Budgets

`AskUserQuestion` with options:

- **Defaults** — 30 file reads, 15 file writes, 20 task checks, 10 email scans, 5 calendar reads, 10 housekeeping fixes per run.
- **Light** — 15 / 8 / 10 / 5 / 3 / 5. Low-volume days.
- **Heavy** — 60 / 30 / 40 / 20 / 10 / 20. High-activity periods.
- **Custom** — Gareth types overrides.

Save as `{{BUDGET_READS}}`, `{{BUDGET_WRITES}}`, `{{BUDGET_TASKS}}`, `{{BUDGET_EMAILS}}`, `{{BUDGET_CALENDAR}}`, `{{BUDGET_HOUSEKEEPING}}`.

---

## Phase 2 — Render

1. Read `references/operator-prompt-template.md`.
2. Read `references/connector-fragments.md`.
3. Replace every `{{PLACEHOLDER}}` with the captured value. For connector-specific placeholders (`{{TODOIST_BOOTSTRAP_LINE}}`, `{{GMAIL_BOOTSTRAP_LINE}}`, `{{CALENDAR_BOOTSTRAP_LINE}}`, `{{HUBSPOT_BOOTSTRAP_LINE}}`, `{{QUICKBOOKS_BOOTSTRAP_LINE}}`, and the corresponding `_STEP_BODY` and `_MCP_BLOCK_LINE` placeholders):
   - Enabled connector → splice in the **Enabled** block from `connector-fragments.md`, then re-run placeholder substitution on any nested placeholders.
   - Disabled → drop the section header AND the placeholder entirely.
4. **Derive path values:**
   - `{{OPERATOR_REPORT_PATH}}` = `{{REPORTS_FOLDER}}\{YYYY-MM-DD}-operator-report.md`
   - `{{ENGINE_GCE_PATH}}` = `{{ENGINE_FOLDER}}\gce\`
   - `{{ENGINE_IMPORT_PATH}}` = `{{ENGINE_FOLDER}}\import-export\`
   - `{{ENGINE_NOVA_PATH}}` = `{{ENGINE_FOLDER}}\nova-incepta\`
   - `{{ENGINE_AI_PATH}}` = `{{ENGINE_FOLDER}}\ai-backend\`
5. Sanity pass: scan the rendered output for any `{{...}}` strings. If any remain, fix or flag before saving.

Show Gareth a short preview (title, cadence line, engines in scope, enabled connectors) and ask one yes/no: "Save it?"

---

## Phase 3 — Save

If yes:

- Use the `Write` tool.
- Path: `{{OPERATOR_PROMPT_PATH}}` (i.e. `C:\Users\Gaming Pc\Documents\Claude\Projects\Gareth Master AI Operating System Build\operator-prompt.md`).
- `Read` it back to confirm content is present.

If the file already exists, ask before overwriting.

---

## Phase 4 — Schedule it (do not stop at "saved")

After the prompt is saved, **immediately invoke the `schedule` skill via the `Skill` tool**. Do not stop at "saved". Do not tell Gareth to run `/schedule create` himself — wire the trigger now.

### Map cadence → cron

| Cadence | Cron |
|---------|------|
| Daily | `0 9 * * *` (9am; ask if a different hour is preferred) |
| Every 4 hours | `0 */4 * * *` |
| Weekly | `0 9 * * 1` (Monday 9am; ask if a different day is preferred) |
| Custom | use what Gareth typed |

### Build the trigger payload

- **Cron expression** — from the table above.
- **Working directory** — `C:\Users\Gaming Pc\Documents\Claude\Projects\Gareth Master AI Operating System Build`.
- **Prompt** — `"Run the Gareth OS Operator. Read and execute operator-prompt.md exactly as written. One run = one report. Stop when done."`
- **Trigger name** — `gareth-os-operator-{{CADENCE_TAG}}`.
- **Description** — `"Gareth OS Operator — {{CADENCE_HUMAN}}"`.

### Invoke the schedule skill

Call the `Skill` tool with `skill: "schedule"` and pass the args described above. Let the schedule skill own its confirmation flow.

If the schedule skill is not installed, fall back to a clear text instruction with the exact cron expression and prompt to paste. Do not pretend the trigger is wired when it isn't.

### After the schedule skill returns

Tell Gareth in one short paragraph:

> Operator prompt saved to `operator-prompt.md` and scheduled {{CADENCE_HUMAN}} (cron `{cron}`). First run will fire on the next tick. Manage the trigger anytime with `/schedule list` or `/schedule update`.

Stop. Do not propose other follow-ups.

---

## Hard rules for this skill

- **Lean bootstrap.** Read `OS_CONTEXT.md` first, not the 5 global files. Only fall back to the full files if `OS_CONTEXT.md` does not exist. Never read all 5 global files on every run — that is the expensive pattern this architecture exists to avoid.
- **Deep-read on demand only.** The full global files (`about_gareth.md` etc.) are only read mid-run when a specific trigger is hit: generating public-facing content (needs brand_voice.md), evaluating a cross-engine dependency (needs life_architecture.md), checking a constraint (needs operating_principles.md), or unsure about output format (needs working_preferences.md).
- **Discovery first.** Read `OS_CONTEXT.md` before asking anything. Never ask for a value it already contains.
- **File tools only for workspace content.** Use `Read`, `Write`, and `Edit` against the local filesystem. No vault MCP.
- **Probe, don't ask.** For Q2 (connectors), inspect available tools in the session and run a read