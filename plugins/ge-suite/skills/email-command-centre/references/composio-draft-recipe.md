# Composio Draft Recipe (the write path)

Reading email is done with the Microsoft 365 connector (it costs no third-party quota).
Creating drafts is done with the connected Composio Outlook toolkit. Composio targets a
message by its Microsoft Graph id, so reply drafts come out correctly threaded with the
quoted history. Bodies are written as HTML so formatting, the context highlights
(`highlighting-rules.md`), and Gareth's signature with logo all render.

You never send. Every draft waits in Outlook Drafts for Gareth to review and send.

## Tools used (Composio gateway)

Discover and run Outlook tools through the Composio meta tools (search, get schemas,
multi-execute, and the remote workbench for HTML work). The Outlook tools this recipe uses:

- `OUTLOOK_SEARCH_MESSAGES` or `OUTLOOK_QUERY_EMAILS` -- find a message id (reply target,
  or a sent email when fetching the signature logo).
- `OUTLOOK_CREATE_DRAFT` -- compose a brand-new draft (Mode B).
- `OUTLOOK_CREATE_DRAFT_REPLY` -- create a threaded reply draft (Mode A), by `message_id`.
- `OUTLOOK_UPDATE_EMAIL` -- set the final HTML body (merged with the quoted thread).
- `OUTLOOK_ADD_MAIL_ATTACHMENT` -- fallback only, to attach the logo inline (cid) if the
  public logo URL is ever unavailable.

**Safety, absolute:** only the draft and search/read tools above. Never call
`OUTLOOK_SEND_EMAIL`, `OUTLOOK_SEND_DRAFT`, `OUTLOOK_REPLY_EMAIL`, `OUTLOOK_FORWARD_MESSAGE`,
or any delete tool, even if discoverable. Gareth keeps these disabled in the Composio
dashboard; the skill must never invoke them regardless.

## Body construction (both modes)

Write the email body as HTML:

1. Greeting, short paragraphs, a numbered list when asking for more than one thing.
2. Bold the few decision-critical details per `highlighting-rules.md`. Sparingly.
3. End the message at "Kind regards," then append the signature block below.
4. No long dashes anywhere.

Signature block to append after "Kind regards," (this is Gareth's real signature; the
mailbox does NOT auto-add a signature to an API-created draft, so the skill supplies it):

```
<p style="margin:0"><b><span style="color:black">Gareth Cohen<br>Global Exporters Australia<br>+0426841514</span></b></p>
<p style="margin:0"><a href="mailto:gareth@globalexporters.com.au" style="color:#C82613"><b>Gareth@globalExporters.com.au</b></a></p>
<p style="margin:8px 0 0 0"><img src="https://www.dropbox.com/scl/fi/5v77k4w0xw76yzmpxpt8v/Logo-1.jpg?rlkey=6ctmuvh2gzooqd9cp9yp28hac&raw=1" alt="Global Exporters" style="border:0"></p>
```

## The signature logo

**Default: serve the logo from the public URL.** The `<img src="...">` above points at the
Global Exporters logo on Dropbox (`?raw=1` direct link). This renders in Outlook with no
attachment step, no S3 key, and works on a brand-new mailbox or first run. Confirmed in
production on 2026-06-03. Use this approach. The current URL is:
`https://www.dropbox.com/scl/fi/5v77k4w0xw76yzmpxpt8v/Logo-1.jpg?rlkey=6ctmuvh2gzooqd9cp9yp28hac&raw=1`

**Fallback only (inline CID attachment).** Use this if the public URL is ever unavailable.
Swap the `src` to `cid:gelogo` and attach the image bytes with `OUTLOOK_ADD_MAIL_ATTACHMENT`
(`contentId` = `gelogo`, `isInline` = true, `contentType` = the image's type, `odata_type` =
`#microsoft.graph.fileAttachment`). Get the bytes from the cached base64 at
`Engines/Global-Exporters/assets/signature-logo-b64.txt`, or, first time, from one of Gareth's
own original sent emails via `OUTLOOK_QUERY_EMAILS` (folder `sentitems`) plus
`OUTLOOK_LIST_OUTLOOK_ATTACHMENTS` (`response_detail: full`). This path fails when no prior
sent email carries the logo and no cached file exists, which is why the public URL is default.

## Mode B -- compose a new draft

1. Confirm the recipient address (vault, or research, never guess).
2. `OUTLOOK_CREATE_DRAFT` with `recipients` (To), `ccRecipients` if any, `subject`, and a
   minimal body (or the full HTML if the tool takes HTML directly).
3. `OUTLOOK_UPDATE_EMAIL` to set the final HTML body (message + highlights + signature with
   the public logo URL). No attachment step needed.

## Mode A -- threaded reply draft

1. Get the source message id (from the M365 read, or via `OUTLOOK_SEARCH_MESSAGES`). Use the
   Composio search id for `OUTLOOK_CREATE_DRAFT_REPLY` so it matches.
2. `OUTLOOK_CREATE_DRAFT_REPLY` with `message_id` and `cc_emails`, and NO `comment`. This
   returns the draft id and a body containing the quoted thread.
3. Build the HTML message (greeting + highlighted body + "Kind regards," + signature with the
   public logo URL). Insert it at the top of the exi