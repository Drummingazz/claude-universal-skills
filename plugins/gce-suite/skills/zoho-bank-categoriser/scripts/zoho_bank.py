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

FIRST-LIVE-RUN NOTE: Zoho's uncategorised-transaction paths are drawn
from Zoho's API docs via Sonnet's 2026-07-16 check but have not yet been
exercised live from this script. The first Code-session run uses
`probe` to verify paths and prints any 4xx body so the constants below
can be corrected in one edit if Zoho's routing differs.
"""
import json, sys, csv, re, argparse, urllib.request, urllib.parse, os
from datetime import date

BASE = "https://www.zohoapis.com.au/books/v3"
ACCOUNTS = "https://accounts.zoho.com.au/oauth/v2/token"
ORG = "7007064397"
HERE = os.path.dirname(os.path.abspath(__file__))
CRED_FILE = os.path.join(HERE, ".zoho_client")
# Candidate endpoint shapes; probe confirms which responds.
LIST_PATHS = [
    "/banktransactions?filter_by=Status.Uncategorized",
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
    rules = []
    for line in open(path, encoding="utf-8"):
        if not line.strip().startswith("|") or set(line.strip()) <= {"|", "-", " ", ":"}: continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or cells[0].lower() in ("pattern",): continue
        rules.append({"pattern": cells[0], "account": cells[1], "pct": cells[2],
                      "tag": cells[3], "status": cells[4].lower(), "notes": cells[5]})
    return rules

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
    acct = accounts_map(tok)
    plan, unmatched = [], []
    for t in txns:
        desc = (t.get("description") or t.get("payee") or "").lower()
        hit = next((r for r in rules if re.search(r["pattern"].lower(), desc)), None)
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
    s = sub.add_parser("setup"); s.add_argument("--grant-code", required=True)
    s.add_argument("--client-id", required=True); s.add_argument("--client-secret", required=True)
    s.set_defaults(f=cmd_setup)
    s = sub.add_parser("probe"); s.set_defaults(f=cmd_probe)
    s = sub.add_parser("run"); s.add_argument("--rules", required=True)
    s.add_argument("--apply", action="store_true"); s.set_defaults(f=cmd_run)
    a = p.parse_args(); a.f(a)

if __name__ == "__main__":
    main()
