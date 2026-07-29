---
name: gareth-os-optimizer
description: Framework-driven audit and optimizer for Gareth's 4-engine AI OS workspace. Applies 9 frameworks adapted for a Cowork file-based system (not an Obsidian vault). F1 audits OS_CONTEXT.md + 5 global files. F9 audits 4-engine architecture and workspace discoverability. Uses Read/Write/Edit/Bash instead of vault MCP. Saves reports to the Reports\ folder. TRIGGERS: os optimizer, optimize workspace, workspace audit, ai os audit, clean up workspace, architecture audit, discoverability check. Run from workspace root.
---

# Gareth OS Optimizer

Apply 9 frameworks to every markdown file in Gareth's AI OS workspace. For each framework, read its pass-implementation file, run every check, log findings, walk fixes per item, apply (or save to plan). Save one comprehensive HTML report grouped by framework. **Do not inline the HTML in chat -- only the saved path and a one-paragraph summary.**

## What is different from the original os-optimizer

This skill is adapted for Gareth's 4-engine AI OS workspace (not an Obsidian vault). Key differences:

- **No vault MCP.** All file I/O uses `Read`, `Write`, `Edit`, and `Bash` tools with Windows absolute paths.
- **No CLAUDE.md.** F1 audits `OS_CONTEXT.md` and the 5 global context files (`about_gareth.md`, `life_architecture.md`, `operating_principles.md`, `brand_voice.md`, `working_preferences.md`) instead.
- **Engine scope, not team scope.** The 4 engines (GCE, Import/Export, Nova Incepta, AI Backend) replace vault team profiles. F8 and F9 reason about engine-layer structure.
- **No em-dashes, ever.** G7 treats em-dashes as a `fail` (not `warn`) in this workspace. Gareth's hard rule.
- **Windows paths.** All paths use backslashes. `start` replaces `open` for launching the report.
- **OS_CONTEXT.md is the lean context file.** F1.1 checks it stays under 80 lines. The 5 global files are the deeper context layer.
- **Reports\ folder.** All audit HTML and JSON outputs go to `{{WORKSPACE_PATH}}\Reports\`.

## Operating philosophy

1. Every finding ships a concrete fix. No flag-only, no warn-and-forget.
2. Severity is informational, not gating. Every check produces fixes.
3. Walk per item for semantic fixes; bulk-apply for mechanical ones.
4. Two modes per fix: apply now or save to plan.
5. Visible progress via TaskCreate/TaskUpdate -- never silent.
6. Read and reason, don't just match. Triggers surface candidates; judgment confirms findings.
7. Discover structure, never assume folder names.

## Frameworks

| # | Framework | Reference (the why) | Pass file (the how) | Applies to |
|---|---|---|---|---|
| F1 | Global Context Files | `references/anthropic-claude-md.md` | `references/passes-global-files.md` | OS_CONTEXT.md + 5 global files |
| F2 | Karpathy LLM Wiki | `references/karpathy-llm-wiki.md` | `references/passes-karpathy-wiki.md` | content notes, engine status files |
| F3 | Caveman compression | `references/caveman-compression.md` | `references/passes-caveman.md` | .skill files + global context files |
| F4 | Chroma context rot | `references/chroma-context-rot.md` | `references/passes-chroma-context-rot.md` | every .md |
| F5 | Anthropic Memory | `references/anthropic-managed-memory.md` | `references/passes-anthropic-memory.md` | every .md |
| F6 | Progressive Disclosure | `references/progressive-disclosure.md` | `references/passes-progressive-disclosure.md` | every .skill file |
| G7 | General Hygiene | `references/practitioner-notes.md` | `references/passes-general-hygiene.md` | every .md (em-dash = fail here) |
| F8 | Reflection | `references/anthropic-dreams.md` | `references/passes-reflection.md` | global files + engine folders + recent Daily\ |
| F9 | 4-Engine Architecture | `references/anthropic-architecture.md` | `references/passes-architecture.md` | whole workspace -- OS_CONTEXT.md, engine folders, workspace navigation chain |

---

## Step 0 -- Verify the workspace

Resolve `{{WORKSPACE_PATH}}` first. Never hardcode a drive letter or a user name. Take the first
of these that reaches a real folder:

1. A path Gareth gives you in the invocation.
2. `workspace_root` recorded in `{{WORKSPACE_PATH}}/.claude/workspace-roles.json` or in
   `OS_CONTEXT.md`, if either is already reachable.
3. The default: `<home>/Documents/Claude/Projects/Gareth Master AI Operating System Build`, where
   `<home>` is the current user's home folder (`$HOME` on macOS and Linux, `%USERPROFILE%` on
   Windows).

Use forward slashes in every path you build from it. Windows accepts them as readily as macOS and
Linux do, so one form works on every surface.

Then check the workspace root is present and has at least one .md file. Use `Glob` with the
pattern `*.md` at `{{WORKSPACE_PATH}}`, not a shell command, so the check works on every surface.

If the folder is unreachable or empty → stop:

> Workspace not found or empty. Make sure Claude has access to the workspace folder and re-run. Tell Gareth which paths you tried.

Otherwise tell Gareth one line:

> Auditing your AI OS workspace against 9 frameworks. First I'll discover your structure (Step 1.5) -- I won't assume folder names. Then I walk every fix with you. You'll see each stage as a task.

Proceed into Step 0.5.

---

## Step 0.5 -- Create the visible task list

Mandatory. Create one task per stage + one per framework.

```
[ ] Discover & classify .md files (Step 1)
[ ] Role discovery -- semantic folder/file classification (Step 1.5)
[ ] F1 Global Context Files -- audit OS_CONTEXT.md + 5 global files
[ ] F2 Karpathy Wiki -- content notes, wikilinks, schema
[ ] F3 Caveman -- compression of skill and instruction-layer files
[ ] F4 Chroma Context Rot -- length, distractors, position
[ ] F5 Anthropic Memory -- file size, naming, indexes
[ ] F6 Progressive Disclosure -- .skill file layering
[ ] G7 General Hygiene -- em-dashes (FAIL), frontmatter, H1 rules
[ ] F8 Reflection -- cross-engine synthesis
[ ] F9 Architecture -- engine folder structure, OS_CONTEXT.md routing, discoverability
[ ] Aggregate findings + architectural read (Steps 3 / 3.5)
[ ] Walk every finding through apply / save-to-plan (Step 4)
[ ] Apply approved fixes (Step 5)
[ ] Render dashboard + open (Step 6)
```

Mark `in_progress` when entering a stage; `completed` when leaving it.

---

## Step 1 -- Discover & classify every .md file

### 1.1 -- Universal glob

Use Bash to find all .md files, excluding system folders:

```bash
find "/mnt/Gareth Master AI Operating System Build" -name "*.md" \
  -not -path "*/.git/*" \
  -not -path "*/node_modules/*" \
  -not -path "*/dist/*" \
  -not -path "*/build/*"
```

No role-based skips. Every .md gets audited.

### 1.2 -- Classify each file by role

| Role | Detection |
|---|---|
| `global-context` | `OS_CONTEXT.md`, `about_gareth.md`, `life_architecture.md`, `operating_principles.md`, `brand_voice.md`, `working_preferences.md` at workspace root |
| `engine-gce` | any .md inside `Engines\gce\` or `GCE\` or similar |
| `engine-import-export` | any .md inside `Engines\import-export\` or `Import-Export\` or similar |
| `engine-nova` | any .md inside `Engines\nova-incepta\` or `Nova\` or similar |
| `engine-ai-backend` | any .md inside `Engines\ai-backend\` or `AI-Backend\` or similar |
| `skill` | any .skill file (binary; note as skill, do not deep-read) |
| `daily` | files matching `\d{4}-\d{2}-\d{2}\.md` inside `Daily\` or similar |
| `report` | files inside `Reports\` |
| `task-list` | `task-list.md` at workspace root |
| `operator-prompt` | `operator-prompt.md` at workspace root |
| `note` | everything else |

### 1.3 -- Build supporting indexes

| Index | Built from | Used by |
|---|---|---|
| `workspace_filename_index` | every .md basename, lowercased | F2, F5 |
| `inbound_link_index` | grep for `[[name]]` patterns across workspace | F2.3, F2.4 |
| `headers_index` | per-file H2/H3 list with line numbers | F3, F5 |

### 1.4 -- Show classification summary

```markdown
## Discovery -- {N} markdown files across {F} folders, {B} total

| Role | Count |
|---|---:|
| Global context files | {n} |
| Engine GCE | {n} |
| Engine Import/Export | {n} |
| Engine Nova Incepta | {n} |
| Engine AI Backend | {n} |
| Daily notes | {n} |
| Reports | {n} |
| Task list | 1 |
| Other notes | {n} |

Framework targets:
- F1 Global Context Files → {n} global files
- F2 Karpathy Wiki → {n} content notes
- F3 Caveman → {n} skill/instruction files
- F4 Chroma Context Rot → {N} files
- F5 Memory → {N} files
- F6 Progressive Disclosure → {n} .skill files (if accessible)
- G7 Hygiene → {N} files (em-dash = FAIL)
- F8 Reflection → global files + {n} engine files + recent daily window
- F9 Architecture → workspace root + {n} engine folders

Running role discovery (Step 1.5) now...
```

---

## Step 1.5 -- Role discovery (semantic, not name-based)

This step replaces every hardcoded assumption about folder names. The pass files reference *roles*. Step 1.5 discovers what folder/file in this workspace plays each role -- or records that it is absent.

### How discovery works

For each role, in order until something resolves:
1. Read workspace root folder names. Build a candidate list.
2. Read 3-5 sample files per candidate folder.
3. Score and pick. Highest-confidence candidate wins. No candidate = role is `missing`.

### Standard roles for Gareth's workspace

| Standard role | Layer | What it is | How to recognize it |
|---|---|---|---|
| `global-context` | curated | OS_CONTEXT.md + 5 global files | Root-level files describing identity, engines, constraints, voice |
| `engine-gce` | curated | Gareth Cohen Experience engine files | GCE bookings, proposals, invoices, client content |
| `engine-import-export` | curated | Import/Export engine files | Supplier, freight, margins, trade content |
| `engine-nova` | curated | Nova Incepta engine files | Music, creative, touring, EP production content |
| `engine-ai-backend` | curated | AI Backend engine files | OS integrity, tool health, system content |
| `daily` | session | Per-day logs or operator reports | Date-stamped .md files |
| `reports` | archive | Audit and operator run reports | Files in a Reports\ folder |
| `tasks` | session | Rolling task backlog | task-list.md |
| `operator-prompt` | meta | The rendered operator prompt | operator-prompt.md at workspace root |
| `skills` | meta | .skill binary packages | .skill files (note presence, don't deep-read binary) |
| `folder-index-convention` | meta | Per-folder index file name | Most frequent index filename across engine folders |

### Custom roles

Every remaining folder not matching a standard role gets classified:
- `name` -- slug derived from folder name + content
- `layer` -- curated, session, archive, meta, or unknown
- `purpose` -- 1-line description
- `confidence` -- high / medium / low

Low-confidence custom roles → F9.0 finding asking Gareth to clarify the folder's purpose.

### Output: the role registry

Build once, cache, and persist to `{{WORKSPACE_PATH}}/.claude/workspace-roles.json`. Write the
resolved `{{WORKSPACE_PATH}}` into `workspace_root` so later runs can read it back rather than
guessing:

```json
{
  "workspace_root": "<the resolved {{WORKSPACE_PATH}}, forward slashes>",
  "discovered_at": "2026-05-26T09:00:00Z",
  "folder_index_convention": {
    "name": "README.md",
    "confidence": "medium",
    "evidence": "No consistent per-folder index detected yet",
    "coverage": 0.0
  },
  "roles": [
    {"name": "global-context", "path": ".\\ (root .md files)", "kind": "files", "layer": "curated", "is_standard": true, "confidence": "high", "purpose": "Identity, engines, constraints, voice"},
    {"name": "engine-gce",          "path": ".\\Engines\\gce\\",          "kind": "folder", "layer": "curated", "is_standard": true, "confidence": "high",   "purpose": "GCE engine files"},
    {"name": "engine-import-export","path": ".\\Engines\\import-export\\","kind": "folder", "layer": "curated", "is_standard": true, "confidence": "high",   "purpose": "Import/Export engine files"},
    {"name": "engine-nova",         "path": ".\\Engines\\nova-incepta\\", "kind": "folder", "layer": "curated", "is_standard": true, "confidence": "high",   "purpose": "Nova Incepta engine files"},
    {"name": "engine-ai-backend",   "path": ".\\Engines\\ai-backend\\",  "kind": "folder", "layer": "curated", "is_standard": true, "confidence": "high",   "purpose": "AI Backend engine files"},
    {"name": "daily",    "path": ".\\Daily\\",   "kind": "folder", "layer": "session",  "is_standard": true, "confidence": "medium", "purpose": "Per-day operator logs"},
    {"name": "reports",  "path": ".\\Reports\\", "kind": "folder", "layer": "archive",  "is_standard": true, "confidence": "high",   "purpose": "Audit and operator run reports"},
    {"name": "tasks",    "path": ".\\task-list.md", "kind": "file", "layer": "session", "is_standard": true, "confidence": "high",   "purpose": "Rolling task backlog"}
  ],
  "missing_standard_roles": [],
  "low_confidence_roles": [],
  "unconfirmed_custom_roles": []
}
```

### Show discovery summary

```markdown
## Your workspace structure -- {N} folders classified

| Path | Role | Layer | Purpose | Confidence |
|---|---|---|---|---|
| .\\ (root files) | global-context | curated | Identity, engines, constraints, voice | high |
| .\\Engines\\gce\\ | engine-gce | curated | GCE engine files | high |
| .\\Engines\\import-export\\ | engine-import-export | curated | Import/Export engine files | high |
| .\\Engines\\nova-incepta\\ | engine-nova | curated | Nova Incepta engine files | high |
| .\\Engines\\ai-backend\\ | engine-ai-backend | curated | AI Backend engine files | high |
| .\\Daily\\ | daily | session | Per-day operator logs | medium |
| .\\Reports\\ | reports | archive | Audit and operator run reports | high |
| task-list.md | tasks | session | Rolling task backlog | high |

Folder-index convention detected: {name or "none yet -- F9.0 will propose one"}

Running F1 now...
```

### Hard rules for downstream frameworks

- Frameworks reference roles by layer, not by name. F8's curated layer = all roles with `layer == 'curated'`.
- Missing roles never block a framework. F8 proceeds without a missing engine folder; F9.0 surfaces the gap.
- Persisted registry is read at the start of Step 1.5 on future runs. Confirmed assignments don't re-prompt.
- No framework hardcodes folder paths. All runtime resolution goes through the registry.

---

## Step 2 -- Iterate frameworks F1 through F9 with judgment

For each framework:
1. Read the pass-implementation file.
2. Determine file scope from the framework table above.
3. For each check: apply trigger heuristic → read context → apply agent judgment → produce finding only if judgment confirms the violation.
4. Every finding includes a `reasoning` field (1-2 sentences specific to this case).
5. Emit one progress line when the framework completes.

F8 runs second-to-last (cross-file synthesis). F9 runs last (largest blast radius).

### G7 override for Gareth's workspace

The standard G7 pass treats em-dashes as `warn`. In this workspace, the severity depends on whether content is public-facing:

- **Public-facing content** (client proposals, quotes, briefs, press releases, marketing copy, anything sent to a customer or external party) → em-dash is `fail`. Gareth's hard rule applies here.
- **Internal content** (daily notes, task lists, operator reports, engine status files, system documentation, skill files) → em-dash is not flagged. Internal systems can use them freely.

The G7.1 pass must classify each file before flagging. If a file's role, name, or content suggests it is or will be shared externally, apply the `fail` severity. If it is clearly internal, skip the em-dash check entirely for that file. When ambiguous, use the file's engine context: GCE proposals and Import/Export quotes are public-facing; AI Backend notes and Daily logs are not.

### F1 override -- global context files instead of CLAUDE.md

F1 in this workspace audits `OS_CONTEXT.md` + the 5 global files, not CLAUDE.md. Read `references/passes-global-files.md` (not `passes-anthropic-claude-md.md`) when running F1. The checks are adapted for the global file structure.

### F9 override -- 4-engine workspace architecture

F9 in this workspace audits the 4-engine folder structure, OS_CONTEXT.md routing accuracy, engine folder index presence, and workspace-level discoverability. Read `references/passes-architecture.md` -- the adapted version for this workspace.

### Finding schema

```json
{
  "framework": "F1",
  "check_id": "F1.4",
  "check_name": "OS_CONTEXT.md current focus staleness",
  "path": ".\\OS_CONTEXT.md",
  "line": 62,
  "severity": "warn",
  "excerpt": "Nova Incepta: [e.g. ...]",
  "reasoning": "The Current Focus section still has the template placeholder text '[e.g. ...]' rather than an actual status line. The operator reads this every run to route engine activity correctly.",
  "action": "Replace the placeholder with the current state of each engine.",
  "fixable": true,
  "fixed": false,
  "citation": "passes-global-files.md → F1.4 Current Focus freshness"
}
```

The `reasoning` field is mandatory. Every finding has it.

---

## Step 3 -- Aggregate findings + compute score

Same scoring formula as the original:

```
For each framework F1..G7:
  deduction = (fail_count × 5) + (warn_count × 1)
  capped_deduction = min(deduction, 25)
score = max(0, 100 - sum(capped_deduction for F1..G7))
```

F8 and F9 do not affect the score.

| Score | Interpretation |
|---|---|
| 90-100 | Well-tuned. Run audit monthly. |
| 70-89 | Visible drift. Address top findings. |
| 50-69 | Bloat is hurting performance. |
| <50 | System rot. Major cleanup needed. |

Emit one short table after scoring, then proceed to the architectural read.

---

## Step 3.5 -- Architectural read

Write a short architectural read of the workspace -- top 1-3 things wrong with the structure as a whole, with reasoning grounded in the global context files. This is the layer Gareth explicitly asked for. Under 250 words total. Goes verbatim into the HTML dashboard.

---

## Step 4 -- Walk every finding through apply-now / save-to-plan

Same walk flow as the original skill. Fire one opening AskUserQuestion with the apply mode options:

1. **Bulk-apply** -- every finding gets applied; walk prompts only fire where the agent genuinely cannot pick a target.
2. **Selective walk** -- per-finding prompt for every fix.
3. **Save everything to plan** -- write all proposed fixes as checklist steps to `{{WORKSPACE_PATH}}\Reports\{YYYY-MM-DD}-reorg-plan.md`.
4. **Cancel** -- abort before any fixes.

---

## Step 5 -- Apply approved fixes

Same fix order as the original: mechanical fixes first (G7 em-dashes, duplicate H1), then wikilinks, then caveman, then skill rewrites, then reflection, then architecture. Smallest blast radius first.

**Save-to-plan path:** `{{WORKSPACE_PATH}}\Reports\{YYYY-MM-DD}-reorg-plan.md` (replaces `Intelligence/decisions/`).

After all fixes: re-measure metrics (Step 5.9), recompute score, compute deltas.

---

## Step 6 -- Render, save, open

### 6.1 -- Compute per-framework metrics (before and after)

Same variable set as the original. Additional workspace-specific variable:

- `{{ENGINE_COVERAGE}}` -- which of the 4 engines have at least one status/index file in their folder (e.g. "GCE: yes, Import/Export: no, Nova Incepta: yes, AI Backend: yes")

### 6.2 -- Build the HTML

Use the same four templates:
- `references/report-template.html`
- `references/report-row-template.html`
- `references/report-section-template.html`
- `references/report-finding-template.html`

Substitute `{{ORG_NAME}}` with "Gareth Cohen AI OS".

Framework `{{FRAMEWORK_WHY}}` strings (fixed):

- F1: "The global context files (OS_CONTEXT.md + 5 global files) are what the operator reads on every run. Lean files with specific constraints earn high compliance; bloated or vague files waste tokens and produce drift."
- F2: "Karpathy's LLM Wiki: knowledge is compiled once and kept current. Lint catches dead links, orphans, contradictions, and undigested sources across the workspace."
- F3: "Caveman compression: every token competes for attention. Strip filler, hedging, and verbose connectors from skill files and instruction-layer context files."
- F4: "Chroma context rot: every model degrades with length; distractors hurt; position matters. Lead with the load-bearing rule and keep the auto-load budget tight."
- F5: "Anthropic Memory: per-file under 10KB recommended. Multiple focused files beat one mega-file. The agent navigates by name."
- F6: "Progressive Disclosure: the context window is a public good. Skill metadata loads always; bodies on relevance; references on demand."
- G7: "Workspace rules: em-dashes are a FAIL (Gareth's hard rule), frontmatter compliance, no H1 duplicating filename."
- F8: "Reflection: per-file lint cannot see contradictions, duplicates, or stale assumptions across the 4-engine system. Cross-engine synthesis surfaces them with concrete fix proposals."
- F9: "4-Engine Architecture: walk the path the Operator actually takes (OS_CONTEXT.md → engine folder → engine status file). Verify routing entries match folder reality, every engine folder has an index file, every file is reachable in 3 hops from the workspace root."

### 6.3 -- Save

Save HTML to `{{WORKSPACE_PATH}}\Reports\{YYYY-MM-DD}-workspace-audit.html`.
Save findings JSON to `{{WORKSPACE_PATH}}\Reports\{YYYY-MM-DD}-workspace-audit-findings.json`.

Read back to confirm content present. Retry once on mismatch.

### 6.4 -- Open and summarize

Open: `Bash`: `start "{{WORKSPACE_PATH}}\Reports\{YYYY-MM-DD}-workspace-audit.html"` (Windows).

Emit full saved HTML in an html code fence. Then summary:

```
Optimizer run complete -- here's what changed:
Report: {{WORKSPACE_PATH}}\Reports\{YYYY-MM-DD}-workspace-audit.html
Score (F1-G7): {score_before} → {score_after} ({delta_sign}{delta}) -- "{interpretation_before}" → "{interpretation_after}"
{N} files audited · {applied_total} fixes applied · {failed_total} mechanical failures
Em-dashes (FAIL): {em_before} → {em_after} (-{em_delta}) · Frontmatter coverage: {fm_pct_before} → {fm_pct_after}
Engines covered by folder index: {engine_coverage_before} → {engine_coverage_after}
Tokens saved: {tokens_saved} (~{annual_savings} tokens/year at {sessions}/week)
```

Stop. Do not propose follow-up actions.

---

## Hard rules

- **Never** assume a folder by name. Always resolve through the role registry built in Step 1.5.
- **Never** use vault_* MCP tools. All file I/O uses Read, Write, Edit, and Bash with Windows absolute paths.
- **Never** apply a CLAUDE.md change (there is no CLAUDE.md in this workspace). F1 edits only the 5 global files and OS_CONTEXT.md, via walk-and-confirm.
- **Em-dashes are always `fail` severity in this workspace.** Never downgrade to `warn`.
- **Never** render the dashboard with only the BEFORE score. Step 5.9 is mandatory.
- **Never** leave a finding open after Step 5. Every finding ends with `fix_status`: applied, saved_to_plan, declined, or failed.
- **Never** bulk-apply semantic fixes (F2 wikilinks, F8 reflection, F9 architecture). Walk per item.
- **Never** skip a framework. F1-F9 all run every audit.
- **Never** run silently. Step 0.5 creates the visible task list; every framework transitions in_progress → completed.
- **Never** ship a half-rendered template. Sanity-check for `{{placeholder}}` strings before saving.
- *