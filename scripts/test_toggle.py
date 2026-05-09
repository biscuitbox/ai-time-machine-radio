#!/usr/bin/env python3
"""검증 단계 (e): 토글 스위치.

실행:
    PYTHONPATH=. python scripts/test_toggle.py

토글을 ON/OFF 하면 상태가 출력되어야 함.
shutdown은 실행하지 않음 — 배선과 GPIO 감지만 확인.
Ctrl+C 로 종료.
"""
import os
import signal
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

os.environ.setdefault("GPIOZERO_PIN_FACTORY", "lgpio")

from gpiozero import Button
from src.config import TOGGLE_IN

# 배선: GPIO4 ← 토글 → GND
# pull_up=True: 토글 ON(연결) = LOW = is_pressed=True
#               토글 OFF(개방) = HIGH = is_pressed=False
toggle = Button(TOGGLE_IN, pull_up=True)


def on_pressed():
    print("toggle → ON", flush=True)


def on_released():
    print("toggle → OFF  (main.py에서는 여기서 shutdown 시작)", flush=True)


toggle.when_pressed  = on_pressed
toggle.when_released = on_released

print(f"toggle test ready — GPIO{TOGGLE_IN}  (Ctrl+C to quit)", flush=True)
signal.pause()
