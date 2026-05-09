from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas

from src.config import OLED_I2C_PORT, OLED_I2C_ADDRESS


def make_device() -> sh1106:
    serial = i2c(port=OLED_I2C_PORT, address=OLED_I2C_ADDRESS)
    return sh1106(serial)


def update(device: sh1106, year: int, channel: str, lang: str) -> None:
    with canvas(device) as draw:
        draw.text((10, 15), str(year), fill="white")
        draw.text((10, 45), f"{channel} · {lang}", fill="white")
