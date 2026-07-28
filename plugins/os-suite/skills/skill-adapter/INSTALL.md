# Install skill-adapter into the user-skills plugin folder

Cowork couldn't write directly to the plugin folder. To activate the skill so it auto-triggers, copy this folder into the skills directory.

Open PowerShell and run:

```powershell
Copy-Item -Path "$env:USERPROFILE\Documents\Claude\Projects\Gareth Master AI Operating System Build\skill-adapter" -Destination "$env:APPDATA\Claude\local-agent-mode-sessions\skills-plugin\ce707f27-f4dd-49ec-96de-8fee939d7483\486a8f4f-c7d3-4dfb-a3ce-908dffc91b8a\skills\" -Recurse -Force
```

Restart Cowork. The skill will appear in `<available_skills>` and trigger on the phrases listed in its `description:` field.

## Verify

After restart, ask: "What skills do I have installed?" — `skill-adapter` should appear in the list.

## Test prompt

"Adapt the `email-scanner-ge` skill so it summarizes priority first and doesn't draft until I approve."

## Rollback

Delete the `skill-adapter` folder from the destination path above and restart.
