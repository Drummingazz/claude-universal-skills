---
name: agent-stress-test
description: >-
  Cross-provider mass adversarial tester for Gareth's AI agents. Runs many
  difficult, messy, multi-turn fake-customer conversations against an agent's
  exact prompt (default Leo, the GCE front-door assistant), scores each with a
  judge model against the agent's own rules, tracks real token cost, and writes a
  ranked bug report. Runs the agent-under-test on OpenAI or Claude, and in
  benchmark mode compares several models on the same scenarios and names the
  cheapest one that still passes. Catches personal-story derailment after correct
  qualification, price pressure, ambiguous or multi-service requests, discontinued
  class requests, agency enquiries, bot challenges, and NDIS-sensitive wording.
  Reusable across agents by pointing it at a different prompt file. Use when
  Gareth says "stress test Leo", "test the agent", "run the bug test", "benchmark
  the models", "which model is cheapest that works", "adversarial test", or after
  any change to an agent prompt to check for regressions.
---

# Agent stress-test

On invocation, first output one header line: `[Agent Stress-Test] — DD MMM YYYY HH:MM AEST` (current AEST).

Finds where an agent breaks by throwing hundreds of realistic difficult customers at its exact
prompt, then reports failures ranked by frequency and severity, with real token cost. Tests the
prompt AND the model, so set the agent model to match production and flag that caveat.

## Self-contained

The harness ships inside this skill folder: `agent_eval.py`, `prompts/leo.md`, `README.md`. Run
`agent_eval.py` in place. It resolves its own folder, so bundled prompts and defaults work wherever
the skill is installed.

Locate the skill folder and run from it. In a shell:

```
DIR=$(dirname "$(find / -path '*/agent-stress-test/agent_eval.py' 2>/dev/null | head -1)")
cd "$DIR"
```

If the skill folder is read-only (the Cowork skills cache), do NOT rely on a key file or the
default `reports/` inside it. Instead pass keys as environment variables and write reports to a
writable folder with `--outdir` (the vault `Engines/GCE/agent-tests` or the build workspace).

## Keys (never accept pasted into chat)

Per provider used: `OPENAI_API_KEY` and/or `ANTHROPIC_API_KEY` as environment variables, or files
`.openai_key` / `.anthropic_key` beside `agent_eval.py` when the folder is writable. Only the
providers you actually use are required. If a key is missing, stop and ask Gareth to add it.

## Environment note

The Cowork sandbox can reach Anthropic but NOT OpenAI. Claude-model runs work inside Cowork; any
OpenAI or GPT run happens where OpenAI is reachable (Claude Code on Gareth's PC, or Codex). Same
script both places.

## Key runs

Install deps first: `pip install openai anthropic` (whichever providers you use; add
`--break-system-packages` in the Cowork sandbox).

Cheapest GPT that passes (one OpenAI key, judge on GPT-5):

```
python3 agent_eval.py --benchmark "gpt-5,gpt-5-mini,gpt-5-nano" \
  --customer-model gpt-5-mini --judge-model gpt-5 \
  --cases 50 --turns 5 --pass-bar 90 --outdir <writable-folder>
```

Cross-company (needs both keys):

```
python3 agent_eval.py --benchmark "gpt-5,gpt-5-mini,haiku,sonnet" \
  --customer-model gpt-5-mini --judge-model gpt-5 --cases 50 --turns 5 --outdir <writable-folder>
```

Always `python3 agent_eval.py --dry-run` first to confirm the plan at no cost.

## Testing another agent

Point `--prompt` at any agent's prompt file to reuse this harness on the Bookings Manager or any
other conversational agent. Note: the tactics and rubric here are tuned for a front-door greeter
(Leo). For a different agent, adapt `TACTICS` and `RUBRIC` in `agent_eval.py`, or add a per-agent
test pack, before trusting the scores.

## After the run

- Read the report(s) in the chosen outdir. Summarise for Gareth: pass rate, top failure modes,
  weakest tactics, cost per 1000 conversations, and for a benchmark the cheapest model that passed.
- Save a copy of the report into the vault at `Engines/GCE/agent-tests/` (create if needed) and
  link it from a daily note.
- Propose concrete prompt or knowledge-base fixes for the top failures, then offer to re-run.
- No dashes in any Gareth-facing summary, per house style.
