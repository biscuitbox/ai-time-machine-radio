#!/usr/bin/env python3
"""v0.1 통합 스크립트 — 검증 단계 (f): 전체 입력 통합.

실행:
    PYTHONPATH=. python src/main.py
"""
import os
import signal
import subprocess
import time

os.environ.setdefault("GPIOZERO_PIN_FACTORY", "lgpio")

from gpiozero import Button, OutputDevice, RotaryEncoder

from src.config import (
    CH_CLK, CH_DT, CHANNELS,
    KEEP_ALIVE,
    LANG_CLK, LANG_DT, LANG_SW, LANGUAGES,
    TOGGLE_IN,
    VOL_CLK, VOL_DT, VOL_INIT,
    YEAR_CLK, YEAR_DT, YEAR_MAX, YEAR_MIN,
)
from src.display import make_device, update as oled_update

# ── State ─────────────────────────────────────────────────────────────────────
_year     = 1985
_ch_idx   = 0
_lang_idx = 0
_volume   = VOL_INIT
_t0       = time.monotonic()


def _log():
    t = time.monotonic() - _t0
    print(
        f"[t={t:.1f}] year={_year} ch={CHANNELS[_ch_idx]} "
        f"lang={LANGUAGES[_lang_idx]} vol={_volume}",
        flush=True,
    )


# ── Encoders ──────────────────────────────────────────────────────────────────
year_enc = RotaryEncoder(YEAR_CLK, YEAR_DT)
vol_enc  = RotaryEncoder(VOL_CLK,  VOL_DT)
ch_enc   = RotaryEncoder(CH_CLK,   CH_DT)
lang_enc = RotaryEncoder(LANG_CLK, LANG_DT)

_prev_steps = {"year": 0, "vol": 0, "ch": 0, "lang": 0}


def _on_year():
    global _year
    delta = year_enc.steps - _prev_steps["year"]
    _prev_steps["year"] = year_enc.steps
    _year = max(YEAR_MIN, min(YEAR_MAX, _year + delta))
    oled_update(display, _year, CHANNELS[_ch_idx], LANGUAGES[_lang_idx])
    _log()


def _on_vol():
    global _volume
    delta = vol_enc.steps - _prev_steps["vol"]
    _prev_steps["vol"] = vol_enc.steps
    _volume = max(0, min(100, _volume + delta))
    _log()


def _on_ch():
    global _ch_idx
    delta = ch_enc.steps - _prev_steps["ch"]
    _prev_steps["ch"] = ch_enc.steps
    _ch_idx = (_ch_idx + delta) % len(CHANNELS)
    oled_update(display, _year, CHANNELS[_ch_idx], LANGUAGES[_lang_idx])
    _log()


def _on_lang():
    global _lang_idx
    delta = lang_enc.steps - _prev_steps["lang"]
    _prev_steps["lang"] = lang_enc.steps
    if delta:
        _lang_idx = (_lang_idx + 1) % len(LANGUAGES)
        oled_update(display, _year, CHANNELS[_ch_idx], LANGUAGES[_lang_idx])
        _log()


year_enc.when_rotated = _on_year
vol_enc.when_rotated  = _on_vol
ch_enc.when_rotated   = _on_ch
lang_enc.when_rotated = _on_lang

# Language SW: press also toggles (either rotation or press works)
lang_sw = Button(LANG_SW, pull_up=True)
lang_sw.when_pressed = _on_lang

# ── Power toggle ──────────────────────────────────────────────────────────────
# Wiring: one leg → GPIO4, other leg → GND.
# Toggle ON  = GPIO4 pulled LOW  (Button.is_pressed = True)
# Toggle OFF = GPIO4 floats HIGH (Button.is_pressed = False) → shutdown
keep_alive = OutputDevice(KEEP_ALIVE, initial_value=True)
toggle     = Button(TOGGLE_IN, pull_up=True)


def _on_power_off():
    print("[power] toggle OFF — graceful shutdown", flush=True)
    keep_alive.off()  # releases latch (effective in v1.0 hybrid wiring)
    subprocess.run(["sudo", "shutdown", "-h", "now"])


toggle.when_released = _on_power_off

# ── Start ─────────────────────────────────────────────────────────────────────
display = make_device()
oled_update(display, _year, CHANNELS[_ch_idx], LANGUAGES[_lang_idx])
_log()
print("[radio] v0.1 ready — Ctrl+C to exit", flush=True)

signal.pause()
