# claude-universal-skills

A Claude plugin marketplace. One public git repo that both **Claude Code** and **Cowork** can
install skills from, so a skill is written once and reaches every surface.

Marketplace name: `gareth-skills`
Owner: Gareth Cohen

> Status: skeleton. It currently ships exactly one throwaway plugin, `roundtrip-test`, whose only
> job is to prove the install path works end to end. Real skills get migrated in deliberately,
> after the round trip is confirmed on both surfaces.

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
2. Select **Add marketplace** and paste the repo URL. Cowork accepts either
   `https://github.com/Drummingazz/claude-universal-skills` or the shorthand
   `Drummingazz/claude-universal-skills`.
3. The plugins from this repo now appear next to plugins from other marketplaces.
   Select `roundtrip-test` and click **Install**.
4. Open the installed plugin to see its skills, and confirm `roundtrip-check` is listed and
   enabled.
5. In a Cowork session, invoke the skill and confirm `ROUNDTRIP-OK-7F3A` comes back.

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
| Marketplace catalogue | The list of what plugins exist | `/plugin marketplace update gareth-skills` in Code. The **Update** button on the marketplace in Cowork. |
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

**The `mirror-skill.js` PostToolUse hook contaminates tests on Gareth's Windows machine.** It
copies any `SKILL.md` written or edited in a Claude Code session into `~/.claude/skills/<name>/`.
Editing a skill in this repo therefore creates a second, local copy that shadows the plugin. When
testing a change here, delete the mirrored copy first:

```bash
rm -rf "$HOME/.claude/skills/<skill-name>"
```

**A session keeps the plugin version it loaded at launch.** Push, refresh the marketplace, then
start a new session. Testing in the session that was already open tells you nothing.

## Relationship to `~/.claude/skills/`

`~/.claude/skills/` is the existing local store on Gareth's Windows machine, mirrored there by
a `PostToolUse` hook. It is untouched by this repo and keeps working exactly as it does now.
Migration of those skills into this marketplace is a separate, deliberate step, taken one skill
at a time after the round trip is proven.
