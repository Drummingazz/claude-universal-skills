#!/usr/bin/env python3
"""Zoho Books bank categorisation wrapper for GCE (AU data centre).

Fills the connector gap: the Zoho Books MCP cannot list or categorise
uncategorised bank feed transactions. This wrapper talks to Zoho's REST
API directly using Gareth's own self-client credentials and executes the
vault rule table. SAFETY MODEL: dry-run by default, every write needs an
explicit --apply, and only rules marked approved-auto in the rule table
are ever auto-applied. Prohibited actions (delete, journals, anything
not listed here) are simply not implemented.

Credentials: .zoho_client JSON beside this script:
  {"client_id": "...", "client_secret": "...", "refresh_token": "..."}
Never paste these into chat. Run `setup` once with a grant code to
create the file (see SKILL.md walkthrough).

CONFIRMED LIVE 2026-07-19: `probe` run against the real AU org. Token
refresh works. Of the two candidate list shapes, only
`/banktransactions/uncategorized` responds (34 items under
'transactions'); `/banktransactions?filter_by=Status.Uncategorized`
returns HTTP 400 "The account does not exist." and is dead. The dead
shape is removed below since list_uncat()'s try-first-that-works loop
no longer needs it as a fallback candidate.
"""
import json, sys, csv, re, argparse, urllib.request, urllib.parse, os
from datetime import date

BASE = "https://www.zohoapis.com.au/books/v3"
ACCOUNTS = "https://accounts.zoho.com.au/oauth/v2/token"
ORG = "7007064397"
HERE = os.path.dirname(os.path.abspath(__file__))
CRED_FILE = os.path.join(HERE, ".zoho_client")
# Confirmed live 2026-07-19 via `probe`; see module docstring.
LIST_PATHS = [
    "/banktransactions/uncategorized",
]
CATEGORIZE_PATH = "/banktransactions/uncategorized/{id}/categorize"
MATCH_PATH = "/banktransactions/uncategorized/{id}/match"

def creds():
    if not os.path.exists(CRED_FILE):
        sys.exit("No .zoho_client file beside the script. Run: zoho_bank.py setup --grant-code <code> --client-id <id> --client-secret <secret>")
    return json.load(open(CRED_FILE))

def token():
    c = creds()
    data = urllib.parse.urlencode({
        "refresh_token": c["refresh_token"], "client_id": c["client_id"],
        "client_secret": c["client_secret"], "grant_type": "refresh_token"}).encode()
    r = json.load(urllib.request.urlopen(urllib.request.Request(ACCOUNTS, data=data)))
    if "access_token" not in r: sys.exit("Token refresh failed: " + json.dumps(r))
    return r["access_token"]

def call(method, path, body=None, tok=None):
    sep = "&" if "?" in path else "?"
    url = f"{BASE}{path}{sep}organization_id={ORG}"
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", "Zoho-oauthtoken " + (tok or token()))
    data = None
    if body is not None:
        data = ("JSONString=" + urllib.parse.quote(json.dumps(body))).encode()
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        return json.load(urllib.request.urlopen(req, data))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code} on {method} {path}\n{e.read().decode()[:800]}", file=sys.stderr)
        raise

def cmd_setup(a):
    # Interactive mode: prompt in this window so nothing lands in any chat.
    if not a.grant_code:
        print("Zoho one-time setup. Paste each value from api-console.zoho.com.au and press Enter.")
        a.client_id = input("Client ID: ").strip()
        a.client_secret = input("Client Secret: ").strip()
        a.grant_code = input("Grant code (from the Generate Code tab, valid ~10 min): ").strip()
    data = urllib.parse.urlencode({
        "grant_type": "authorization_code", "code": a.grant_code,
        "client_id": a.client_id, "client_secret": a.client_secret}).encode()
    r = json.load(urllib.request.urlopen(urllib.request.Request(ACCOUNTS, data=data)))
    if "refresh_token" not in r: sys.exit("Exchange failed (grant codes expire in ~10 min): " + json.dumps(r))
    json.dump({"client_id": a.client_id, "client_secret": a.client_secret,
               "refresh_token": r["refresh_token"]}, open(CRED_FILE, "w"))
    os.chmod(CRED_FILE, 0o600)
    print("Saved .zoho_client. Never commit or paste this file.")

def cmd_probe(a):
    tok = token()
    print("Token OK. Probing list endpoints:")
    for p in LIST_PATHS:
        try:
            r = call("GET", p, tok=tok)
            key = next((k for k in r if isinstance(r.get(k), list)), None)
            print(f"  WORKS: {p} -> {len(r.get(key, []))} items under '{key}'")
        except Exception:
            print(f"  fails: {p}")

def load_rules(path):
    """Parse the vault rule table.

    A pattern cell may itself contain regex alternation with '|', which is also
    the markdown cell separator, so cells are taken from the RIGHT: the last
    four are Effective From, Effective To, Notes and (before them) Status, and
    everything left over at the front rejoins into the pattern.
    Columns: Pattern | Account | Business % | Service Line | Status | From | To | Notes
    """
    rules = []
    for line in open(path, encoding="utf-8"):
        if not line.strip().startswith("|") or set(line.strip()) <= {"|", "-", " ", ":"}: continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 8 or cells[0].lower() in ("pattern",): continue
        pattern = "|".join(cells[:len(cells) - 7])
        account, pct, tag, status, eff_from, eff_to, notes = cells[len(cells) - 7:]
        rules.append({"pattern": pattern, "account": account, "pct": pct, "tag": tag,
                      "status": status.lower(), "from": eff_from, "to": eff_to, "notes": notes})
    return rules

def rule_applies(rule, txn_date):
    """Honour the Effective From / Effective To window on a rule row.

    The AI rows are deliberately date-split (50% before 2026-08-03, 70% from
    2026-08-03). Ignoring the window silently applies the first matching row to
    every date, which books the wrong business percentage.
    """
    d = (txn_date or "")[:10]
    if rule["from"] and d and d < rule["from"]: return False
    if rule["to"] and d and d > rule["to"]: return False
    return True

def list_uncat(tok):
    for p in LIST_PATHS:
        try:
            r = call("GET", p, tok=tok)
            key = next((k for k in r if isinstance(r.get(k), list)), None)
            if key: return r[key]
        except Exception:
            continue
    sys.exit("No list endpoint responded; run probe and fix LIST_PATHS.")

def accounts_map(tok):
    r = call("GET", "/chartofaccounts?per_page=200", tok=tok)
    return {a["account_name"].lower(): a["account_id"] for a in r.get("chartofaccounts", [])}

def cmd_run(a):
    tok = token()
    rules = load_rules(a.rules)
    txns = list_uncat(tok)
    plan, unmatched = [], []
    for t in txns:
        desc = (t.get("description") or t.get("payee") or "").lower()
        hit = next((r for r in rules if rule_applies(r, t.get("date"))
                    and re.search(r["pattern"].lower(), desc)), None)
        if hit: plan.append((t, hit))
        else: unmatched.append(t)
    print(f"{len(txns)} uncategorised | {len(plan)} rule-matched | {len(unmatched)} need review\n")
    for t, r in plan:
        auto = "AUTO" if r["status"] == "approved-auto" else "flag"
        print(f"  [{auto}] {t.get('date','?')} {t.get('description','')[:48]:48} ${t.get('amount',0):>9} -> {r['account']} ({r['pct']}% business)")
    for t in unmatched:
        print(f"  [ ?? ] {t.get('date','?')} {t.get('description','')[:48]:48} ${t.get('amount',0):>9} -> NO RULE, review with Gareth")
    if not a.apply:
        print("\nDRY RUN. Nothing written. Re-run with --apply to execute approved-auto rows only.")
        return
    # Fetched lazily: /chartofaccounts needs ZohoBooks.settings.READ, which a
    # banking-only self-client does not have. A dry run must not need it.
    acct = accounts_map(tok)
    applied = 0
    for t, r in plan:
        if r["status"] != "approved-auto": continue
        acc_id = acct.get(r["account"].lower())
        if not acc_id:
            print(f"  SKIP {t.get('description','')}: account '{r['account']}' not in chart"); continue
        body = {"account_id": acc_id, "date": t.get("date"),
                "amount": t.get("amount"), "description": t.get("description", "")}
        call("POST", CATEGORIZE_PATH.format(id=t.get("transaction_id") or t.get("imported_transaction_id")), body, tok)
        applied += 1
    print(f"\nApplied {applied} approved-auto categorisations. Flagged and unmatched rows untouched.")

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("setup"); s.add_argument("--grant-code")
    s.add_argument("--client-id"); s.add_argument("--client-secret")
    s.set_defaults(f=cmd_setup)
    s = sub.add_parser("probe"); s.set_defaults(f=cmd_probe)
    s = sub.add_parser("run"); s.add_argument("--rules", required=True)
    s.add_argument("--apply", action="store_true"); s.set_defaults(f=cmd_run)
    a = p.parse_args(); a.f(a)

if __name__ == "__main__":
    main()
