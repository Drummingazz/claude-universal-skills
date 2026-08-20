# claude-universal-skills

A Claude plugin marketplace. One public git repo that both **Claude Code** and **Cowork** can
install skills from, so a skill is written once and reaches every surface.

Marketplace name: `gareth-skills`
Owner: Gareth Cohen

> Status: round trip confirmed on both surfaces, and the first migration is in. Skills are grouped
> into suites by engine rather than shipped one plugin per skill, so you install once per engine
> and can switch a whole engine off when you are not working in it.

## What ships

| Plugin | Skills | Contents |
| --- | --- | --- |
| `gce-suite` | 9 | bookings-manager, cold-outreach, command-secretary, finance-controller, risk-reviewer, seo-website, social-campaign, gigscan, tax-return-assistant |
| `ge-suite` | 3 | email-command-centre, freight-quote-intake, ge-debug-verify |
| `os-suite` | 7 | daily-focus, re-fresh, honesty, greenlight-council, gareth-os-operator, gareth-os-optimizer, skill-adapter |
| `writing-suite` | 2 | linkedin-writer, newsletter-writer |
| `roundtrip-test` | 1 | roundtrip-check, the throwaway install prover. Keep it. It is the fastest way to tell whether a surface is working before you debug a real skill. |

### Deliberately not shipped

| Skill | Why |
| --- | --- |
| `agent-stress-test` | ships a live OpenAI key alongside it. Needs the secret moved out first. |
| `zoho-bank-categoriser` | ships Zoho self client credentials, plus a `.bat` and two `.py` files that cannot run in a Linux Cowork session. Already documented as Claude Code only. |
| `ge-command-centre-stress-test` | has no `SKILL.md`. It loads nowhere as it stands. |
| `email-scan`, `email-response-workflow`, `email-scanner-ge` | superseded by `email-command-centre`, which says so in its own description. Shipping four near-identical descriptions makes it unpredictable which one Claude reaches for. They remain in the vault, untouched. |

### Known limitation in `os-suite`

`gareth-os-operator`, `gareth-os-optimizer` and `skill-adapter` contain hardcoded
`C:\Users\...` paths. They work in Claude Code on Gareth's machine and will not work in a Linux
Cowork cloud session. That was already true before this repo existed. Install `os-suite`
anywhere, but expect those three to be Code only until the paths are parameterised.

## What is in here

```
.claude-plugin/
  marketplace.json          the catalogue. Claude reads this file first.
plugins/
  roundtrip-test/
    .claude-plugin/
      plugin.json           this plugin's metadata
    skills/
      roundtrip-check/
        SKILL.md            the skill itself
README.md
```

Two rules explain that layout:

1. `marketplace.json` must live at `.claude-plugin/marketplace.json` in the **repo root**. That is
   the only fixed path. Nothing else about the layout is enforced.
2. Each plugin's `source` in `marketplace.json` is a path **relative to the repo root**, not
   relative to the `.claude-plugin` folder. So `"./plugins/roundtrip-test"` means
   `<repo>/plugins/roundtrip-test`.

## Add the marketplace in Claude Code

Two steps: register the catalogue, then install the plugin you want from it. Adding the
marketplace on its own installs nothing.

Inside a terminal `claude` session that is step 1 and step 2 below, typed as slash commands.
If you are in the **Claude Code desktop app**, `/plugin` opens an interactive terminal panel
that the app does not host, so use the non interactive shell form instead. The desktop app
ships its own copy of the CLI, so you do not need a separate install:

```
C:\Users\<you>\AppData\Roaming\Claude\claude-code\<version>\claude.exe
```

**1. Add the marketplace.** Slash form, then shell form:

```bash
/plugin marketplace add Drummingazz/claude-universal-skills
```

```bash
claude plugin marketplace add Drummingazz/claude-universal-skills
```

The `owner/repo` shorthand works for public GitHub repos.

**2. Install the plugin:**

```bash
/plugin install roundtrip-test@gareth-skills
```

```bash
claude plugin install roundtrip-test@gareth-skills --scope user
```

`gareth-skills` is the `name` field inside `marketplace.json`, not the repo name. That is the
name you always install against. Scopes are `user` (you, everywhere), `project` (everyone on
this repo), and `local` (you, this repo only).

**3. Activate it.** In a terminal session, `/reload-plugins` picks it up without a restart.
Otherwise just start a new session, which is the reliable route in the desktop app.

**4. Run the skill.** Plugin skills are namespaced by plugin name:

```bash
/roundtrip-test:roundtrip-check
```

It should print `ROUNDTRIP-OK-7F3A`. That code appearing is the proof.

Useful checks, in either form:

```bash
claude plugin marketplace list
```

```bash
claude plugin list
```

Validate before you push, so a broken manifest never reaches anyone:

```bash
claude plugin validate .
```

### What the install writes

Adding and installing edits `~/.claude/settings.json`. You can also write these two blocks by
hand, which is the only route available in a cloud session, where the plugin browser does not
exist:

```json
{
  "extraKnownMarketplaces": {
    "gareth-skills": {
      "source": { "source": "github", "repo": "Drummingazz/claude-universal-skills" }
    }
  },
  "enabledPlugins": {
    "roundtrip-test@gareth-skills": true
  }
}
```

The plugin files themselves are copied to
`~/.claude/plugins/cache/gareth-skills/<plugin>/<version>/`. Nothing runs from this git repo
directly.

## Add the marketplace in Cowork

Cowork does the same two steps, through the UI rather than slash commands.

**Cowork is a separate install, not a sync.** Its skills, plugins and connectors come from the
**Customize** configuration, which syncs through your claude.ai account, not from the CLI's
`~/.claude` directory. Installing this plugin in Claude Code does nothing for Cowork, and the
reverse is also true. Every plugin gets installed twice, once per surface. That is the price of
one repo reaching both, and it is still far better than hand copying skill files.

1. Open **Customize** in the sidebar, then **Plugins**.
2. Click **Add**, select **Add marketplace**, and give it the repo. Cowork accepts either
   `https://github.com/Drummingazz/claude-universal-skills` or the shorthand
   `Drummingazz/claude-universal-skills`.
3. Click **Browse**. This opens the Directory, which has three tabs: **Anthropic**, **Partners**
   and **Personal**. It opens on Anthropic. **The plugins from this repo are under Personal.**
4. Select the plugin you want and click the **+** on its card to install.
5. Open the installed plugin to see its skills, and confirm they are listed and enabled.
6. In a brand new Cowork session, invoke a skill from it and confirm it answers.

**The Directory search box only searches the tab you are on.** Searching for one of your own
plugins from the Anthropic tab returns "No plugins match your search", which reads exactly like
the plugin is missing or the marketplace is broken. It is neither. Switch to Personal first.

### Updating an installed plugin in Cowork

There is no Update button, and the help docs do not cover this. The control is called **Sync**
and it is reached through the add dialog:

1. Customize > Plugins > **Add** > **Add marketplace**.
2. Select the already-added repo from the dropdown.
3. The dialog says "This marketplace is already added" in red. Ignore that. Click **Sync**.

If Sync is greyed out, the marketplace registration is fine and the thing you actually want is
to install or reinstall the plugin, not to sync the catalogue. Removing a plugin does not remove
its marketplace, and the two are separate rows in separate places.

There is also a **Sync automatically** toggle in that dialog, described as "Keep plugins up to
date when the repository changes on GitHub". It does not help with a plugin that is not
installed, since there is nothing to update.

### Why this repo is public

Claude Code documents private marketplace repos and explains the git credential setup they
need. The Cowork docs do **not** document private repo support: they say GitHub including
GitHub Enterprise is supported, and that public repos on GitLab and Bitbucket also work.
Since the whole point of this repo is to reach both surfaces, it stays public. Nothing secret,
no credentials, and no client data goes in here. Ever.

## How updates actually propagate

This is the part that trips people up, so it is spelled out.

**Nothing is live.** Neither surface reads your GitHub repo at the moment a skill runs. Both
copy the plugin down into a local cache and run from that copy. Pushing a commit does not
change anything on your machine by itself.

There are two separate caches, and they refresh independently:

| Layer | What it is | How it refreshes |
| --- | --- | --- |
| Marketplace catalogue | The list of what plugins exist | `/plugin marketplace update gareth-skills` in Code. In Cowork, **Sync**. See below. |
| Installed plugin | The actual skill files | Follows the plugin's version. See below. |

**Version resolution.** Claude decides "is this a new version?" using the first of these that is set:

1. `version` in the plugin's `plugin.json`
2. `version` in the plugin's entry in `marketplace.json`
3. the git commit SHA

**This repo deliberately sets no `version` anywhere.** That means rule 3 applies and every new
commit counts as a new version, so changes actually reach you. The trap it avoids: if
`plugin.json` says `"version": "1.0.0"` and you push ten commits without bumping that string,
existing installs see the same version and keep the stale cached copy. If a `version` is ever
added here, it must be bumped on every release.

**Auto update.** Claude Code can refresh marketplaces and plugins in the background shortly
after a session starts, with a randomised delay of up to ten minutes. It is **on by default for
official Anthropic marketplaces and off by default for third party ones like this one.** Turn it
on per marketplace: run `/plugin`, go to **Marketplaces**, pick `gareth-skills`, choose
**Enable auto-update**. Cowork checks for plugin updates from the marketplace a plugin came
from, and warns you before an update would overwrite files you edited locally.

**The reliable manual sequence in Claude Code**, after pushing a change:

```bash
/plugin marketplace update gareth-skills
```

```bash
/reload-plugins
```

**Practical consequence:** a session already running keeps using the version it loaded at
launch. Push, refresh, reload, then test. Do not test in the session that was open before
you pushed.

## Rules for anything added to this repo

- **No PowerShell.** A Cowork cloud session runs Linux and cannot execute a `.ps1`. Anything
  shipped inside a plugin must be portable or must be plain markdown with no scripts at all.
- **No secrets, no credentials, no client data.** The repo is public.
- **No absolute Windows paths** in a skill that is meant to run on both surfaces.
- Every `SKILL.md` needs valid frontmatter with `name` and `description`, or it is never
  discovered.
- A skill's frontmatter `name` should match its directory name.

## Gotchas found the hard way

**Always invoke the namespaced form when testing.** A plugin skill is
`/roundtrip-test:roundtrip-check`. The bare `/roundtrip-check` may resolve to a local copy in
`~/.claude/skills/` and tell you the install worked when it did not. Only the namespaced form
proves the plugin loaded.

**A skill can silently fork, and the copies drift for weeks without an error.** This happened to
`gce-finance-controller` and cost a day on 2026-08-20. The repo copy held the 2026-08-03 pre-send
verification checklist and the 2026-08-11 session clock rule. The account-library copy held the
2026-08-16 standard procedure and approval block. **Neither was a superset**, and nothing warned
that two copies existed.

The mechanism: `save_skill`, and editing a skill through Customize, both write to the account
skill library, which is a **different copy** from the one this repo ships as a plugin. Nothing in
either interface tells you that. A session that improves a skill in Cowork therefore forks it.

**The rule that prevents it: any skill that ships as a plugin is edited in this repo and nowhere
else.** If a session proposes saving one through `save_skill` or Customize, redirect it to the
repo. One canonical home, one distribution path.

**Historical note.** An earlier `mirror-skill.js` PostToolUse hook did something similar,
copying any `SKILL.md` edited in a Claude Code session into `~/.claude/skills/<name>/`. That hook
was **retired on 2026-07-29** and its registration removed from `settings.json`. It is not the
cause of any fork dated after that, and this README previously said otherwise, which sent a
2026-08-20 debugging session down the wrong path for most of a day. Check `settings.json` for a
live `hooks` key before believing any claim about hooks, including this one.

**A session keeps the plugin version it loaded at launch.** Push, refresh the marketplace, then
start a new session. Testing in the session that was already open tells you nothing.

**In Cowork, a newly installed plugin does not reach an already open session, and the error it
gives you is misleading.** An open session showed the skill as a blue recognised name and listed
it in the Context panel, then answered `/roundtrip-check` with
`Unknown command: /roundtrip-test:roundtrip-check`. That looks like a namespacing bug and is not
one. Cowork expands the name internally while the session's registry is still stale. A brand new
Cowork session ran the same skill first time. **Always test in a fresh session before reporting a
Cowork plugin as broken.**

**Cowork does not use the `plugin:skill` namespace when you type it.** Claude Code wants
`/roundtrip-test:roundtrip-check`. In Cowork you type the bare `/roundtrip-check`.

## The other skill stores, and why they matter

This repo is not the only place a skill can live. Knowing which store you are looking at is the
difference between a two minute update and a lost day.

| Store | What it is | How it is changed |
| --- | --- | --- |
| This repo | The canonical source for everything shipped as a plugin | git commit and push |
| Account skill library | Personal skills synced through your claude.ai account, shown in Customize > Skills | Customize UI, or `save_skill` from a session. Deleting the files does nothing, the sync restores them |
| `~/.claude/skills/` | The Claude Code local store on Gareth's Windows machine | files on disk |
| Plugin caches | One per surface, copied down from this repo | never edit these, they are overwritten |

**A skill present in both this repo and the account library is a collision, not a backup.** Both
are exposed to a session at once, with near-identical descriptions, so which one answers a plain
request like "invoice this booking" is not predictable. On 2026-08-20 ten skills were in this
state and the account-library copies were removed to resolve it.

### This repo is not a complete backup

As of 2026-08-20, these exist in the account library or the vault but **nowhere in this repo's
git history**, so nothing here would restore them:

- `daily-close`, which has no ship or no-ship decision recorded anywhere
- `email-scan`, `email-response-workflow`, `email-scanner-ge`, deliberately unshipped, vault is
  their home
- `ge-command-centre-stress-test`, which has never been in this repo in any commit on any branch

Check that list before deleting anything from another store on the assumption that git holds it.
