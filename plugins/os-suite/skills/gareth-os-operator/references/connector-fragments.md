# Connector Fragments

These are the spliceable body blocks the skill uses to fill the per-connector sections of `operator-prompt-template.md`. Pick the matching block for each enabled connector; drop the section entirely (and remove the placeholder line) for connectors Gareth did not enable.

For any connector left disabled, also strip every reference to that connector's product name and MCP tools from the rendered prompt.

---

## Bootstrap lines

### `{{TODOIST_BOOTSTRAP_LINE}}` -- when Todoist is enabled

> - **Todoist: pull all tasks due today and overdue tasks.** Re-fetch every run; do not trust prior cache.

### `{{GMAIL_BOOTSTRAP_LINE}}` -- when Gmail is enabled

> - **Gmail: pull inbox threads from the last 24h** that are unread or flagged. Used for the email activity digest in step 3.

### `{{CALENDAR_BOOTSTRAP_LINE}}` -- when Google Calendar is enabled

> - **Google Calendar: list today's events and tomorrow's events** so deadlines and prep time are visible.

### `{{HUBSPOT_BOOTSTRAP_LINE}}` -- when HubSpot is enabled

> - **HubSpot: pull open deals and recent contact activity** from the last 24h. Route GCE leads to GCE engine, Import/Export leads to Import/Export engine.

### `{{QUICKBOOKS_BOOTSTRAP_LINE}}` -- when QuickBooks is enabled

> - **QuickBooks: pull outstanding invoices and recent transactions** for a cashflow signal.

---

## `{{ENABLED_CONNECTORS_LINE}}`

A one-liner listing which connectors are queried every run. Examples:

- All five enabled: "Todoist, Gmail, Google Calendar, HubSpot, and QuickBooks are queried every run."
- No connectors enabled: "File system is the only data source this operator uses."
- Partial: "Todoist and Gmail are queried every run."

---

## Step 1 -- Google Calendar

### Enabled

> - List today's events via `{{CALENDAR_MCP}}__list_events` with today's date range.
> - List tomorrow's events to surface upcoming deadlines.
> - For each event, identify which engine it belongs to (GCE = performances/bookings/client calls, Import/Export = supplier calls, Nova Incepta = creative/studio/touring, AI Backend = system maintenance).
> - Extract any action items or prep tasks implied by the events. Append to the relevant engine's daily and to `{{TASK_LIST_PATH}}`.
> - Do not duplicate events already logged in a prior run for the same date.

### Disabled

> _Google Calendar connector not enabled. Skip this step._

---

## Step 2 -- Todoist

### Enabled

> - Fetch tasks due today via `{{TODOIST_MCP}}__find-tasks-by-date` with today's date.
> - Fetch overdue tasks via `{{TODOIST_MCP}}__find-tasks` with `filter: "overdue"`.
> - Classify each task by engine based on its project label or content.
> - Append overdue tasks to the `## Tasks Due / Overdue` section of today's root daily.
> - Any task without a due date that has been open for more than 7 days → flag in housekeeping queue.
> - Do not create duplicate tasks in Todoist. Read before writing.
> - Cap: {{BUDGET_TASKS}} task checks per run.

### Disabled

> _Todoist connector not enabled. Skip this step._

---

## Step 3 -- Gmail

### Enabled

> - Search inbox for unread or flagged threads from the last 24h via `{{GMAIL_MCP}}__search_threads` with `query: "is:unread OR is:starred after:{YYYY/MM/DD}"`.
> - For each thread, classify by engine (GCE = booking enquiries/client comms, Import/Export = supplier/freight/customs, Nova Incepta = booking agents/labels/press, AI Backend = tool/API/service emails).
> - Summarize actionable threads only (requires a reply, a decision, or a follow-up). Ignore newsletters, receipts, and notifications unless they contain a financial flag.
> - Append email activity notes to the relevant engine daily.
> - Append to root daily under `## Email Activity`.
> - Flag any unread thread older than 48h with no reply from Gareth → add to housekeeping queue as a "needs response" item.
> - Cap: {{BUDGET_EMAILS}} email scans per run.
> - This step is read-only on Gmail. Never send emails.

### Disabled

> _Gmail connector not enabled. Skip this step. Drop all email references from the rendered prompt._

---

## Step 4 -- HubSpot

### Enabled

> - Fetch open CRM objects (deals, contacts with recent activity) via `{{HUBSPOT_MCP}}__get_crm_objects`.
> - Route each item to its engine: GCE objects go to the GCE engine daily, Import/Export contacts/deals go to Import/Export engine daily.
> - Flag any deal that has had no activity in more than 7 days → add to housekeeping queue.
> - Append pipeline summary to root daily under `## Pipeline / Leads`.
> - Check campaign analytics if relevant (`{{HUBSPOT_MCP}}__get_campaign_analytics`) for any active GCE or Nova Incepta campaigns.
> - Do not create or update CRM records unless Gareth has explicitly tasked it.

### Disabled

> _HubSpot connector not enabled. Skip this step._

---

## Step 5 -- QuickBooks

### Enabled

> - Fetch outstanding invoices via `{{QUICKBOOKS_MCP}}__qbo_sales_get_invoices`.
> - Fetch AR aging summary via `{{QUICKBOOKS_MCP}}__qbo_accounting_get_ar_aging_summary` to surface overdue receivables.
> - Generate a cashflow signal: if total overdue AR exceeds a meaningful threshold, flag as CASHFLOW ALERT in root daily under `## Cashflow Flag`.
> - Route outstanding invoices by engine (GCE invoices, Import/Export invoices).
> - Do not make any QuickBooks writes (no creating invoices, no payments) unless Gareth has explicitly tasked it.
> - This step is read-only on QuickBooks.

### Disabled

> _QuickBooks connector not enabled. Skip this step._

---

## `{{MCP_BLOCK}}` -- pick the rows that match Gareth's enabled connectors

```
- **File system** (Read/Write/Edit tools): all workspace file I/O. Use absolute paths under `{{WORKSPACE_PATH}}`.
- **{{TODOIST_MCP}}** (Todoist): task management. Read tasks due today and overdue. Never create duplicate tasks.
- **{{GMAIL_MCP}}** (Gmail): email. Read-only digest of last 24h actionable threads. Never send emails.
- **{{CALENDAR_MCP}}** (Google Calendar): calendar. List today and tomorrow's events. Extract action items.
- **{{HUBSPOT_MCP}}** (HubSpot): CRM. Read open deals and recent contact activity. Read-only unless explicitly tasked.
- **{{QUICKBOOKS_MCP}}** (QuickBooks): accounting. Read-only AR aging and invoice status. Never create transactions.
```

Drop the line for any connector Gareth did not enable.
