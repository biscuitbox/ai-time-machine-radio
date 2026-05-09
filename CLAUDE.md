# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository status

This repository currently contains **only a PRD** (`docs/prd.md`). There is no source code, no build system, no tests, and no firmware yet. Any "how to build/test/run" instructions would be fabricated — when implementation begins, replace this section with real commands.

The PRD is written in **Korean**. Treat it as the source of truth for scope; when in doubt, re-read it rather than guessing. Conversation with the user may also be in Korean.

## What is being built

A desktop "vintage radio" toy (`AI 타임머신 라디오`) that plays AI-generated radio broadcasts from a chosen year (1970–2100). The user turns a physical year dial; a Raspberry Pi 5 generates DJ patter via a **local** LLM, synthesizes it via **local** TTS (Piper), mixes in radio-noise SFX, and plays era-appropriate music from a local library.

Hardware target: Raspberry Pi 5 (8GB+, 16GB preferred). The user owns an ESP32-DEV but **this project does not use it** — Pi 5 only. Case is 3D-printed on a Bambu P1S.

## Architectural commitments (from PRD §3, §5)

These are not preferences — they are explicit constraints. Don't propose alternatives without flagging that you're departing from the PRD.

- **Local-only AI.** No cloud LLM APIs (Anthropic, OpenAI, etc.). No API keys. Inference runs on the Pi via llama.cpp or Ollama, with a small quantized Korean-capable model (Qwen 2.5 1.5B/3B, Gemma 2 2B, EXAONE 2.4B are candidates — not yet benchmarked).
- **Local-only TTS.** Piper. Korean voice model not yet selected.
- **No inbound network.** Wi-Fi is allowed only for NTP and (optionally) pulling model/music updates. Nothing listens for inbound connections. No remote-access feature.
- **No real RF.** No FM/AM tuner, no antenna (decorative or otherwise). The "radio" is entirely simulated.
- **No app, no voice control.** All input is physical: toggle power switch, rotary encoder for year, three knobs (volume / channel / KO-EN language).
- **Pre-cache aggressively.** 1970–2026 × {ko, en} × channels should be generated in the background and stored, so dial changes hit cache (≤1s response). Cold generation budget is ≤10s.
- **Run for days unattended.** systemd `Restart=always`, memory watchdog, periodic LLM worker restart to defend against leaks.

Explicit non-goals (PRD `WON'T`): VU meter visuals, analog needle visuals, Spotify/streaming integration, smartphone app, cloud LLM, real RF reception. Do not add these even if they seem like obvious enhancements.

## Versioned milestones (PRD §7)

The PRD defines a strict v0.1 → v0.5 → v1.0 progression with concrete "Done" definitions. Match work to the current milestone — don't skip ahead.

- **v0.1**: Hardware-only. Dial/knobs/switch wired up; OLED shows year; inputs print to serial as `[t=12.3] year=1985 ch=news lang=ko vol=70`. **No AI, no audio yet.** Validation order is prescribed: power → OLED I2C blink → encoder alone → 3 knobs alone → toggle → integration.
- **v0.5**: AI + SFX, no music. LLM/TTS pipeline working, radio noise + tube warmup SFX, auto-inserted intro/outro phrases, background pre-caching, channel + language switching.
- **v1.0**: Era music from local library, polished case, USB-C primary + 18650 backup (1–2h), 7-day unattended uptime verified.

## Open questions (PRD Appendix A)

The PRD contains a TODO list of unresolved decisions: Pi 5 RAM size verification, Korean LLM benchmark, Piper voice audition, music library source/licensing, **LLM hallucination guardrails for historical Korean broadcasts** (don't let the model invent specific names/events/dates from the 1970s–80s — keep it to "typical mood, generalities"), display choice, audio output path (I2S MAX98357 likely — Pi 5 has no 3.5mm jack), encoder model (EC11 24-pulse), future-mode end year, SFX sourcing.

If a task touches any of these, treat the answer as not-yet-decided and surface the choice rather than picking silently.

## Working in this repo

- The project lives under a Google Drive path with Korean characters and spaces. Always quote paths.
- The user is a Korean maker (`biscuitbox@haeyeon.ms.kr`) building this for personal/family use, not a product. Optimize suggestions for one-off hobby builds, not manufacturability.
- The `maker-project-agent` skill is the right vehicle for hardware/firmware work on this repo (Raspberry Pi, part selection, power budgeting, Korea-specific sourcing).
