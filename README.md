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

**1. Add the marketplace** (run this inside a `claude` terminal session):

```bash
/plugin marketplace add <OWNER>/claude-universal-skills
```

The `owner/repo` shorthand works for public GitHub repos. There is also a non interactive
shell form, useful for scripting:

```bash
claude plugin marketplace add <OWNER>/claude-universal-skills
```

**2. Install the plugin:**

```bash
/plugin install roundtrip-test@gareth-skills
```

`gareth-skills` is the `name` field inside `marketplace.json`, not the repo name. That is the
name you always install against.

**3. Activate it in the current session** (otherwise it loads on next launch):

```bash
/reload-plugins
```

**4. Run the skill.** Plugin skills are namespaced by plugin name:

```bash
/roundtrip-test:roundtrip-check
```

It should print `ROUNDTRIP-OK-7F3A`. That code appearing is the proof.

Useful checks:

```bash
/plugin marketplace list
```

```bash
/plugin list
```

Note: `/plugin` opens an interactive terminal panel. It works in a real `claude` terminal
session. In the Claude Code desktop app, use the app's own plugin browser instead.

## Add the marketplace in Cowork

Cowork does the same two steps, through the UI rather than slash commands.

1. Open **Customize** in the sidebar, then **Plugins**.
2. Select **Add marketplace** and paste the repo URL. Cowork accepts either
   `https://github.com/<OWNER>/claude-universal-skills` or the shorthand
   `<OWNER>/claude-universal-skills`.
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

## Relationship to `~/.claude/skills/`

`~/.claude/skills/` is the existing local store on Gareth's Windows machine, mirrored there by
a `PostToolUse` hook. It is untouched by this repo and keeps working exactly as it does now.
Migration of those skills into this marketplace is a separate, deliberate step, taken one skill
at a time after the round trip is proven.
