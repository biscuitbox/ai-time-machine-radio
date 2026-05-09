#!/usr/bin/env python3
"""검증 단계 (d): 노브 3개 단독 (볼륨 / 채널 / 언어).

실행:
    PYTHONPATH=. python scripts/test_knobs.py

각 노브를 돌리거나 언어 SW를 누르면 변화가 출력되어야 함.
Ctrl+C 로 종료.
"""
import os
import signal
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

os.environ.setdefault("GPIOZERO_PIN_FACTORY", "lgpio")

from gpiozero import Button, RotaryEncoder
from src.config import (
    CH_CLK, CH_DT, CHANNELS,
    LANG_CLK, LANG_DT, LANG_SW, LANGUAGES,
    VOL_CLK, VOL_DT, VOL_INIT,
)

_vol    = VOL_INIT
_ch_idx = 0
_lang_idx = 0

vol_enc  = RotaryEncoder(VOL_CLK,  VOL_DT)
ch_enc   = RotaryEncoder(CH_CLK,   CH_DT)
lang_enc = RotaryEncoder(LANG_CLK, LANG_DT)
lang_sw  = Button(LANG_SW, pull_up=True)

_prev = {"vol": 0, "ch": 0, "lang": 0}


def on_vol():
    global _vol
    delta = vol_enc.steps - _prev["vol"]
    _prev["vol"] = vol_enc.steps
    _vol = max(0, min(100, _vol + delta))
    print(f"vol={_vol}", flush=True)


def on_ch():
    global _ch_idx
    delta = ch_enc.steps - _prev["ch"]
    _prev["ch"] = ch_enc.steps
    _ch_idx = (_ch_idx + delta) % len(CHANNELS)
    print(f"ch={CHANNELS[_ch_idx]}", flush=True)


def on_lang():
    global _lang_idx
    delta = lang_enc.steps - _prev["lang"]
    _prev["lang"] = lang_enc.steps
    if delta:
        _lang_idx = (_lang_idx + 1) % len(LANGUAGES)
        print(f"lang={LANGUAGES[_lang_idx]}  (rotation)", flush=True)


def on_lang_sw():
    global _lang_idx
    _lang_idx = (_lang_idx + 1) % len(LANGUAGES)
    print(f"lang={LANGUAGES[_lang_idx]}  (SW press)", flush=True)


vol_enc.when_rotated  = on_vol
ch_enc.when_rotated   = on_ch
lang_enc.when_rotated = on_lang
lang_sw.when_pressed  = on_lang_sw

print("knobs ready — rotate or press (Ctrl+C to quit)", flush=True)
signal.pause()
