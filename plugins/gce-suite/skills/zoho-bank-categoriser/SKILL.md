---
name: zoho-bank-categoriser
description: Approval-gated wrapper for categorising uncategorised bank feed transactions in Zoho Books, the one capability the Zoho connector lacks. Executes the vault rule table (Engines/GCE/zoho-categorisation-rules.md) against Zoho's REST API with Gareth's own self-client credentials. Use when Gareth says "categorise the bank feed", "run the bank rules", "clear the uncategorised queue", "how many bank items are waiting", or after any statement import lands transactions in Zoho. MUST run from a Claude Code session (the Cowork sandbox has no network to Zoho); in Cowork, stage the run for Code instead of attempting it.
---

# Zoho bank categoriser

Clears Zoho's uncategorised bank transaction queue by executing the rule table, flagging everything the table does not confidently cover. Fills the connector gap recorded in the opus gap list (items 13 and 14).

On invocation, output one header line first: `[Zoho Bank Categoriser]: DD MMM YYYY HH:MM AEST` using the current date and time in AEST.

## Where it runs

Claude Code sessions only. The script needs open network to zohoapis.com.au. If invoked in Cowork, do not attempt network calls; write the run request into the Daily note for the next Code session.

## Safety model (absolute)

- Dry run is the default. `--apply` is required for any write, and even then ONLY rules whose Status is approved-auto in the rule table execute; flagged and unmatched rows are never touched by the script.
- A pattern reaches approved-auto only after Gareth approves it once in a batch review (the standing graduation model). New patterns start as flag.
- Personal rows categorise to Owner's Drawings per the rule table, never to expense accounts.
- Not implemented on purpose: deletes, journal posting, invoice or payment writes, anything beyond categorise, match and exclude. The month-end mixed-use adjustment journal is computed by the Finance Controller and entered with Gareth, not by this script.
- Credentials live in `.zoho_client` beside the script (chmod 600), never in chat, never in the vault, never committed.

## One-time setup (Gareth, about ten minutes)

1. Go to api-console.zoho.com.au and sign in with the Zoho account (the backend Gmail identity that owns Zoho Books).
2. Add Client, choose **Self Client**, Create. Copy the Client ID and Client Secret it shows.
3. On the Generate Code tab: scope `ZohoBooks.banking.ALL,ZohoBooks.settings.READ`, duration 10 minutes, any description. Generate and copy the code (it expires in about ten minutes, so do step 4 immediately).
4. Double-click `SETUP-ZOHO.bat` in the skill folder. A window opens and asks for the three values one at a time; paste each and press Enter. It exchanges the code for a permanent key and writes `.zoho_client`. Done; the ID, secret and code never enter a chat. (Terminal-comfortable alternative: `python zoho_bank.py setup` prompts the same way.)
5. First run ever: `python zoho_bank.py probe` verifies the endpoint paths live (they came from Zoho's docs, not yet exercised); if a path 404s, correct the constants at the top of the script in one edit and record the working shape here.

**Confirmed live 2026-07-19, re-confirmed 2026-08-11.** Token refresh works. Working list endpoint: `GET /banktransactions/uncategorized` (returns items under `transactions`; 34 in the queue at first probe, 52 on 2026-08-11). The other candidate shape, `/banktransactions?filter_by=Status.Uncategorized`, returns HTTP 400 "The account does not exist." and has now actually been removed from the script's `LIST_PATHS`. `categorize`/`match` write paths are still unexercised (dry-run only so far); confirm those the first time `--apply` actually runs.

> [!warning] Setup is already done, do not redo it. A working `.zoho_client` has existed beside the script since 2026-07-19. A later brief assumed it was missing and sent a session off to build a new self-client. Run `probe` first; if it prints "Token OK", setup is done.

**Scope gap, 2026-08-11.** The existing token carries `ZohoBooks.banking.ALL` but NOT `ZohoBooks.settings.READ`, so `GET /chartofaccounts` returns 401 code 57. That call is only needed to resolve account names to ids when writing, so it is now fetched lazily and a dry run no longer needs it. Before the first real `--apply`, either regenerate the self-client with both scopes, or read the chart of accounts through the Zoho MCP connector (`list_chart_of_accounts`) and hand the ids in.

## The working loop

1. `python zoho_bank.py run --rules "<vault>/Engines/GCE/zoho-categorisation-rules.md"` prints the full queue: AUTO rows (approved patterns), flag rows (matched but not graduated), and NO RULE rows.
2. Gareth reviews the printout in batches (batch triage, never line-by-line unless he wants to). New recurring merchants become new rule rows; his yes on a pattern flips its Status to approved-auto in the vault file.
3. `... run --rules ... --apply` executes the approved-auto rows only. Everything else stays queued for the next review.
4. Close by updating the Finance Controller's AgentStatus Note with the remaining queue count, and log the run to the Daily note.

## Related vault files

- Engines/GCE/zoho-categorisation-rules.md (the rule table, canonical)
- Engines/GCE/zoho-history-import-plan.md (bulk history categorisation uses this same wrapper)
- Engines/GCE/zoho-data-model-draft.md (FINAL decisions: accounts, splits, three-account structure)
