---
name: roundtrip-check
description: >-
  Proves that a plugin installed from the gareth-skills marketplace actually loaded and can
  be invoked. Does nothing except print one known phrase. Use when Gareth says
  "roundtrip check", "/roundtrip-check", "prove the marketplace works", "did the plugin
  install", or "test the marketplace round trip". Purely diagnostic. It reads nothing,
  writes nothing, and runs no commands.
---

# Round trip check

This skill exists for one reason: to prove that a plugin published in the
`gareth-skills` marketplace was fetched, installed, and loaded on whatever surface
is running right now (Claude Code or Cowork).

## What to do

Output exactly these three lines and nothing else. Do not add commentary,
do not add a preamble, do not summarise.

```
ROUNDTRIP-OK-7F3A
Source: gareth-skills marketplace / roundtrip-test plugin / roundtrip-check skill
Surface: <Claude Code or Cowork, whichever you are running in>
```

Replace only the angle-bracket part on the third line. Leave lines one and two
byte for byte identical, including the code `ROUNDTRIP-OK-7F3A`. That exact code is
the proof: if Gareth sees it, the marketplace round trip worked.

## Rules

- Run no commands, no scripts, and no tools of any kind.
- Read no files.
- Write no files.
- If you cannot determine the surface on line three, write `Surface: unknown`.
