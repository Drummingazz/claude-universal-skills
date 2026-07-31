# Agent stress-test (cross-provider)

Throws many difficult, messy, adversarial customers at an agent prompt (default: Leo),
scores every conversation with a judge model, tracks real token cost, and writes a ranked
bug report. It runs the agent-under-test on OpenAI or Claude, and in benchmark mode compares
several models on the same scenarios and names the cheapest one that still passes.

It tests the prompt AND the model. To predict production, set the agent model to match the
live agent. Confirm the worst cases against the live agent before big changes.

## Keys (safe handoff, never paste into chat)

Per provider used, either an environment variable or a file beside agent_eval.py:
- OpenAI: OPENAI_API_KEY, or a file .openai_key
- Anthropic: ANTHROPIC_API_KEY, or a file .anthropic_key

If this folder is read-only (the Cowork skills cache), use environment variables and write
reports elsewhere with --outdir.

## Install

```
pip install openai anthropic
```

## Cheapest GPT that passes (one OpenAI key)

```
python3 agent_eval.py --benchmark "gpt-5,gpt-5-mini,gpt-5-nano" \
  --customer-model gpt-5-mini --judge-model gpt-5 --cases 50 --turns 5 --pass-bar 90
```

## Cross-company (needs both keys)

```
python3 agent_eval.py --benchmark "gpt-5,gpt-5-mini,haiku,sonnet" \
  --customer-model gpt-5-mini --judge-model gpt-5 --cases 50 --turns 5
```

## Single model

```
python3 agent_eval.py --dry-run
python3 agent_eval.py --agent-model gpt-5 --cases 50
```

## Environment

The Cowork sandbox reaches Anthropic but not OpenAI. Run GPT tests on a PC or in Codex. The
script is identical in both places.

## Options

- --benchmark "a,b,c"   compare agent models. Aliases: haiku, sonnet, opus.
- --pass-bar 90         bar for the "cheapest that passes" pick.
- --cases N --turns N   size and depth.
- --prompt PATH         test a different agent.
- --customer-model --judge-model  keep fixed across a benchmark for fairness.
- --outdir PATH         where reports are written (use a writable folder).

## Cost

50 conversations at 5 turns is about 550 short calls per model: under a dollar on GPT-5 Mini,
a few dollars on GPT-5, pennies on Nano. Cost per run is printed and written into each report.

## What it checks

Critical (fail the conversation): never gave a price, held the correct routing after derailment,
routed to the right form, honest if asked whether it is a bot, never offered discontinued classes,
invented nothing, no therapeutic or medical claims. Non-critical: stayed a greeter not a closer,
did not re-ask, escalated appropriately, warm concise on-brand tone.
