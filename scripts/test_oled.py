#!/usr/bin/env python3
"""검증 단계 (b): OLED I2C blink.

실행:
    PYTHONPATH=. python scripts/test_oled.py

SH1106이 올바르게 연결되면 화면이 켜졌다 꺼지기를 반복.
아무것도 안 보이면: i2cdetect -y 1 로 주소 확인 후 config.py OLED_I2C_ADDRESS 수정.
"""
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.display import make_device
from luma.core.render import canvas

device = make_device()
print(f"OLED detected at address {device.serial_interface._i2c_address:#x}")

for i in range(6):
    with canvas(device) as draw:
        if i % 2 == 0:
            draw.text((10, 25), "HELLO 1985", fill="white")
        # odd iterations → blank canvas = screen off
    time.sleep(0.8)

print("blink test done")
