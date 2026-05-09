#!/usr/bin/env python3
"""검증 단계 (c): 연도 다이얼 단독.

실행:
    PYTHONPATH=. python scripts/test_encoder.py

다이얼을 돌리면 year 값이 1970~2100 범위 내에서 변해야 함.
Ctrl+C 로 종료.
"""
import os
import signal
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

os.environ.setdefault("GPIOZERO_PIN_FACTORY", "lgpio")

from gpiozero import RotaryEncoder
from src.config import YEAR_CLK, YEAR_DT, YEAR_MIN, YEAR_MAX

enc = RotaryEncoder(YEAR_CLK, YEAR_DT)
_prev = 0
_year = 1985


def on_rotated():
    global _year, _prev
    delta = enc.steps - _prev
    _prev = enc.steps
    _year = max(YEAR_MIN, min(YEAR_MAX, _year + delta))
    print(f"steps={enc.steps:+d}  year={_year}", flush=True)


enc.when_rotated = on_rotated
print(f"encoder ready — initial year={_year}  (Ctrl+C to quit)", flush=True)
signal.pause()
