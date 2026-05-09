# GPIO pin assignments (BCM) — PRD Appendix C (2026-05-09)

# Year dial (KY-040)
YEAR_CLK = 17
YEAR_DT  = 27
YEAR_SW  = 22  # reserved for future use

# Volume encoder (KY-040)
VOL_CLK  = 5
VOL_DT   = 6
VOL_SW   = 13  # reserved for future use

# Channel encoder (KY-040)
CH_CLK   = 16
CH_DT    = 26
CH_SW    = 12  # reserved for future use

# Language encoder (KY-040) — rotation or SW press toggles ko/en
LANG_CLK = 23
LANG_DT  = 24
LANG_SW  = 25

# Power
TOGGLE_IN  = 4  # SPST toggle: one leg to GPIO4, other to GND; pull_up=True internally
KEEP_ALIVE = 7  # hold HIGH to keep latch on; pull LOW before shutdown (wired in v1.0)

# I2S (GPIO18-21) — reserved for v0.5+ I2S DAC; do NOT use in v0.1

# I2C / OLED
OLED_I2C_PORT    = 1      # /dev/i2c-1 on Pi
OLED_I2C_ADDRESS = 0x3C   # verify with: i2cdetect -y 1  (may be 0x3D)

# Application
YEAR_MIN  = 1970
YEAR_MAX  = 2100
CHANNELS  = ["news", "pop", "ad", "classic"]
LANGUAGES = ["ko", "en"]
VOL_INIT  = 70
