# F9 -- 4-Engine Architecture & Discoverability (pass implementation)

**Reference (the why):** `references/anthropic-architecture.md`.
**Applies to:** the whole workspace -- `OS_CONTEXT.md`, the 4 engine folders, all folder-index files (under the discovered convention), and every .md reachable from the workspace root. Reads the global context files (especially `life_architecture.md` and `about_gareth.md`) to understand Gareth's world and judge whether structure matches intent.

**Out of scope (F9 never edits without per-item user approval):** `OS_CONTEXT.md`, any global context file, any .skill file. These can be *targeted* by F9 fixes (e.g., F9.1 updates OS_CONTEXT.md routing, F9.7 adds an orientation section), but only via walk-and-confirm -- never automated.

## How this pass works

Whole-workspace structural reasoning. Triggers are mechanical (does the folder exist? does an index file exist? does the routing entry match reality?), but every finding requires reading folder contents, judging alignment with Gareth's stated engine intent, and proposing a concrete change. Nothing in F9 ships as flag-only.

## Contents

1. [Setup -- read global files, build navigation graph](#setup)
2. [F9.0 -- Missing structural roles](#f90--missing-structural-roles)
3. [F9.1 -- OS_CONTEXT.md routing truthfulness](#f91--os_contextmd-routing-truthfulness)
4. [F9.2 -- Engine folder index presence and freshness](#f92--engine-folder-index-presence-and-freshness)
5. [F9.3 -- Discoverability walk](#f93--discoverability-walk)
6. [F9.4 -- Cross-engine file misplacement](#f94--cross-engine-file-misplacement)
7. [F9.5 -- Engine scope duplication](#f95--engine-scope-duplication)
8. [F9.6 -- Workspace reorganization proposals](#f96--workspace-reorganization-proposals)
9. [F9.7 -- OS_CONTEXT.md fitness as workspace orientation](#f97--os_contextmd-fitness-as-workspace-orientation)
10. [Cross-framework constraints](#cross-framework-constraints)
11. [Finding schema](#finding-schema)

---

## Setup -- read global files, build navigation graph

Before running any F9 check, do this once and cache:

1. **Read `OS_CONTEXT.md`** -- extract engine names, routing logic, hard constraints, and the "Deep-Read Triggers" section to understand which global file governs what.
2. **Read `life_architecture.md`** -- extract the engine dependency map: what each engine funds, what destabilizes the system, cash priority order. F9.1 and F9.4 use this to judge whether the folder structure matches the stated engine priorities.
3. **Read `about_gareth.md`** -- extract role, primary focus, current phase of each engine. F9.7 uses this to judge OS_CONTEXT.md fitness.
4. **Build the navigation graph:**
   - Node = file or folder.
   - Edge = "reachable from" (OS_CONTEXT.md routing section → engine folder → engine index file → child files).
   - Compute hop distance from workspace root for every .md.
5. **Build the folder inventory:**
   - For each folder: list .md children, list subfolders, check for index file presence under the discovered convention, record mtime of index file if present.
6. **Sample engine folder contents:**
   - For each engine folder with 3+ files: read 3-5 files (newest, oldest, median by size). Cache first 1500 chars + headers. F9.1 / F9.4 use these to judge alignment with the engine's stated purpose.

---

## F9.0 -- Missing structural roles

Three tiers of findings based on how load-bearing the gap is:

### Tier 1 -- Critical gaps (fail)

These are missing in a way that makes the operator unreliable:

- **OS_CONTEXT.md missing** -- the operator cannot bootstrap. Propose creating it from `references/OS_CONTEXT_template.md`.
- **task-list.md missing** -- the operator has nowhere to track its backlog. Propose creating it with standard sections.
- **Any engine folder referenced in OS_CONTEXT.md that does not exist** -- the operator will route to a non-existent path. Propose creating the folder and an initial index file.

### Tier 2 -- Functional improvements (warn)

These make the workspace harder to navigate or maintain:

- **No folder-index convention established** -- no per-engine or per-folder index files detected. Propose adopting a convention (default: `README.md` per folder, as it is universally understood).
- **Reports\ folder missing** -- the operator and optimizer have nowhere to save reports. Propose creating it.
- **Daily\ folder missing** -- the operator has no daily log folder. Propose creating it.

### Tier 3 -- Optional enhancements (info)

- **No explicit version or change log for global files** -- the operator cannot detect when global files have been updated vs. when they last ran. Propose adding a `last_updated:` frontmatter field.

---

## F9.1 -- OS_CONTEXT.md routing truthfulness

**What it checks:** every engine path, folder reference, and file reference mentioned in OS_CONTEXT.md must correspond to something that actually exists in the workspace.

**Navigation graph query:**
- For each path-like string in OS_CONTEXT.md (anything matching `\\[^\\]+\\` or `[A-Za-z]:` or relative paths like `.\\Engines\\`):
  1. Resolve the path relative to the workspace root.
  2. Check whether the file or folder exists.
  3. If not: candidate for F9.1 finding.

**Agent judgment:**
- Is this a template placeholder (e.g., `{{WORKSPACE_PATH}}`) that was never rendered? Fail -- the OS_CONTEXT.md was not properly set up from the template.
- Is this a real path that no longer exists (folder was renamed/deleted)? Fail -- routing is broken.
- Is this a path that exists but is different from what OS_CONTEXT.md says (e.g., folder is named `GCE\` but OS_CONTEXT.md says `Engines\gce\`)? Warn -- routing will fail silently.
- Is the path present and resolving correctly? Not a finding.

**Severity:** fail for broken paths, warn for mismatched paths.

**Finding format:**
```
OS_CONTEXT.md line {N} -- path "{path}" does not resolve
Reasoning: {why this broken path matters -- what will fail at operator runtime}
Action: either create the folder/file at the referenced path, or update OS_CONTEXT.md to match the actual path
Citation: passes-architecture.md → F9.1 routing truthfulness
```

---

## F9.2 -- Engine folder index presence and freshness

**What it checks:** each engine folder should have an index file (under the discovered `folder_index_convention.name`, or `README.md` as default) describing what the folder contains and the engine's current status.

**For each engine folder (GCE, Import/Export, Nova Incepta, AI Backend):**
1. Check whether an index file exists under the discovered convention.
2. If it exists: read it. Check whether it covers: (a) engine purpose, (b) current status, (c) key files in the folder, (d) any hard constraints specific to this engine.
3. Check mtime: if the file was last modified more than 30 days ago, flag as potentially stale.

**Agent judgment:**
- Index file missing: surface as F9.2 finding with a drafted index template.
- Index file present but thin (< 5 meaningful lines, no status, no file list): warn.
- Index file present but stale (mtime > 30 days, status section still describes a state inconsistent with recent files in the folder): warn.
- Index file present, substantive, and recent: not a finding.

**Severity:** fail for missing index on a non-trivial engine folder (3+ files), warn for thin or stale index.

**Drafted engine index template:**
```markdown
---
status: active
type: engine-index
engine: {Engine Name}
tags: [engine, {engine-slug}]
last_updated: {YYYY-MM-DD}
---

# {Engine Name}

**Purpose:** {1-line statement of what this engine does and its role in the OS}

**Cash role:** {Primary income | Future upside | Protection layer}

**Current status:** {1-line current state -- updated manually or by operator}

## Key files

- {filename.md} -- {1-line description}

## Hard constraints

- {specific constraint for this engine, from operating_principles.md}

## Updated

{YYYY-MM-DD} -- auto-generated by os-optimizer F9.2.
```

---

## F9.3 -- Discoverability walk

**What it checks:** every .md file in the workspace should be reachable within 3 hops from the workspace root:

- Hop 1: OS_CONTEXT.md (routing section) → engine folder
- Hop 2: engine folder → engine index file
- Hop 3: engine index file → child file

Files reachable in more than 3 hops are navigation orphans.

**Navigation graph query:**
- Compute hop distance from workspace root for every .md (using the graph built in Setup).
- Files with hop distance > 3 or hop distance = unreachable (no inbound link from any index): candidates.

**Agent judgment:**
- Is the file in the `Daily\` or `Reports\` folder? These are session/archive layer -- exempt from the 3-hop rule (they are not navigated, they accumulate).
- Is the file a task-list.md or operator-prompt.md at the workspace root? Hop distance 1 -- not an orphan.
- Is the file a deeply nested note in an engine subfolder with no mention in the engine index? Real navigation orphan -- flag.
- Is the file a template, draft, or scratch file that intentionally lives outside the navigation chain? Lower severity if the file has clear draft/template markers.

**For each navigation orphan:**
- Option A: add the file to the relevant engine's index file (apply now).
- Option B: add a routing entry in OS_CONTEXT.md (for files that deserve top-level routing).
- Option C: move the file to the correct engine folder (flag -- do not auto-move without confirmation).
- Option D: archive the file (if it is clearly stale).

---

## F9.4 -- Cross-engine file misplacement

**What it checks:** files should live in the engine folder that matches their content. A file about a music release living in the GCE folder is misplaced. A supplier quote living in the Nova Incepta folder is misplaced.

**Engine routing guide** (from `life_architecture.md` + `OS_CONTEXT.md`):
- **GCE:** performances, corporate bookings, entertainment client proposals, invoices to entertainment contacts, cruise ship enquiries
- **Import/Export:** supplier contacts, freight, customs, margin analysis, trade quotes, import/export invoices
- **Nova Incepta:** booking agents, labels, press, studio sessions, Armageddon EP, touring logistics, creative collaborators
- **AI Backend:** tool errors, MCP issues, skill updates, system audits, API/service alerts

**Agent judgment for each candidate:**
- Read the file. Does its content match the engine folder it's in, or another engine?
- Is the file intentionally cross-engine (e.g., a GCE booking that also involves Nova Incepta touring)? If so, it should be in the primary engine folder with a cross-reference wikilink to the secondary engine.
- Is the misplacement accidental (file dropped in the wrong folder, named ambiguously)?

**Severity:** warn for clear misplacement, info for ambiguous cross-engine files.

**Finding format:**
```
.\\{current-path} -- likely belongs in .\\{correct-engine-folder}\\
Reasoning: {why the file's content matches the other engine -- cite specific content from the file and the engine routing guide}
Action: move to {proposed path}; add a cross-reference in {current engine index} if relevant to both engines
Citation: passes-architecture.md → F9.4 cross-engine misplacement
```

---

## F9.5 -- Engine scope duplication

**What it checks:** two or more engine folders accumulating files with overlapping purpose -- not cross-engine collaboration, but genuine duplication of the same concern in two places.

**What to look for:**
- Similar filenames across two engine folders (e.g., `status.md` in both GCE and Import/Export that describe the same pipeline state).
- Near-identical content snippets across engine dailies.
- Two engine folders both tracking the same type of asset (e.g., both GCE and Nova Incepta tracking "booking enquiries" without a clear scope boundary).

**Agent judgment:**
- Read both files. Is this genuine duplication (same content, same purpose, same constraints) or two different views on a shared topic (one from a GCE lens, one from a Nova lens)?
- Genuine duplication: flag. Propose making one canonical, the other a cross-reference stub.
- Two different views: not a finding, but suggest a cross-reference in the engine indices so both views are explicitly linked.

**Severity:** warn for genuine duplication, info for unlinked dual views.

---

## F9.6 -- Workspace reorganization proposals

**What it checks:** structural patterns across the workspace that suggest a reorganization would materially improve navigability or engine-layer separation.

This check fires only when F9.0-F9.5 surface a cluster of related findings pointing to a structural cause, not individual file issues.

**Trigger patterns:**
- 3+ navigation orphans in the same unnamed subfolder → propose giving the folder a proper role + index file.
- 2+ engine folders with no index file → propose establishing the folder-index convention workspace-wide.
- A folder at the workspace root that does not match any standard role or custom role with high confidence → propose classifying it or absorbing it into an existing engine folder.
- Files from two engines sharing the same parent folder (e.g., both GCE and Import/Export files in a generic `Clients\` folder) → propose splitting by engine.

**Agent judgment:**
- Is the proposed reorg grounded in Gareth's actual stated structure (from `life_architecture.md` and `OS_CONTEXT.md`), or is it imposing a convention Gareth hasn't chosen?
- Only propose reorgs that resolve a real observed problem. "BenAI organizes vaults this way" is not a valid justification.

**Every F9.6 finding:** save to plan by default (not apply now). These are high-blast-radius changes. The user can choose "apply now" and walk the migration steps if they want immediate execution.

---

## F9.7 -- OS_CONTEXT.md fitness as workspace orientation

**What it checks:** does OS_CONTEXT.md actually orient a new agent (or the operator) in Gareth's specific world? An agent reading only OS_CONTEXT.md should be able to: (a) identify the 4 engines and their priorities, (b) enforce the cash-stability constraint, (c) route any task to the correct engine folder, (d) know the key voice rules for output, (e) know where to find deeper context if needed.

**Five orientation questions to assess:**

1. **Engine identification:** does OS_CONTEXT.md name all 4 engines with their cash roles in a scannable format? (fail if missing)
2. **Cash priority rule:** is the cash-stability constraint explicitly stated as a rule (not just implied)? (fail if missing)
3. **Routing logic:** does OS_CONTEXT.md include a routing table or routing heuristics sufficient to classify any task to an engine? (fail if missing)
4. **Voice rules:** are the key voice rules (no em-dashes, direct output, no fluff) explicitly stated? (warn if absent)
5. **Deep-read triggers:** does OS_CONTEXT.md tell the operator when to read each of the 5 global files? (warn if absent)

**Agent judgment:**
- Read OS_CONTEXT.md in full. Check each of the 5 orientation questions.
- Do not flag sections that are present but terse -- a one-line rule that is specific is better than a paragraph that is vague.
- Draft proposed additions for any missing orientation question, ready for Gareth to confirm in the walk.

**Severity:** fail for missing engine identification, cash-priority rule, or routing logic; warn for missing voice rules or deep-read triggers.

---

## Cross-framework constraints

- F9 never edits OS_CONTEXT.md or any global file automatically. All F9.1 / F9.7 fixes are walk-and-confirm.
- F9 never moves files between engine folders without per-item confirmation (F9.4). The agent proposes; Gareth confirms.
- F9 never proposes a structure purely because BenAI uses that convention. Every proposal cites specific evidence from Gareth's workspace or global files.
- F9 does not score the cash-stability constraint as a cosmetic issue. Cross-engine scope creep (Nova Incepta expansion blocking GCE priority) is a `fail`.
- F9.6 reorg proposals are always save-to-plan first. The user must explicitly choose "apply now" and walk each migration step.

---

## Finding schema

```json
{
  "framework": "F9",
  "check_id": "F9.2",
  "check_name": "Engine folder index presence",
  "path": ".\\Engines\\import-export\\",
  "line": null,
  "severity": "fail",
  "excerpt": "No index file found (README.md or equivalent)",
  "reasoning": "The Import/Export engine folder has 7 .md files but no index. An operator routing to this folder cannot determine which file is the current status, which are historical, or what the engine's current constraints are without reading every file. Per life_architecture.md, this is a Cash Engine B -- missing structural clarity here directly risks routing errors on cash-sensitive tasks.",
  "action": "Create .\\Engines\\import-export\\README.md using the engine index template. Cover: engine purpose, current status, key files, hard constraints.",
  "fixable": true,
  "fixed": false,
  "citation": "passes-architecture.md → F9.2 engine folder index"
}
```
