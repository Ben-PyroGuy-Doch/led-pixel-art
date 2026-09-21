# ------------------------------------------------------------
#  EMOJI PIXEL ART on an 8x8 LED screen  -  Raspberry Pi Pico W
#
#  TAP the button        -> next emoji
#  HOLD the button (1s)  -> switch between STILL and ANIMATED
#                           (green flash = animated, blue flash = still)
#
#  Language: MicroPython (use the Thonny app to run it)
# ------------------------------------------------------------
from machine import Pin
from neopixel import NeoPixel
import rp2
import time

# ---------- SETTINGS (safe to change!) ----------
DATA_PIN = 15         # the Pico pin the screen's "DIN" wire is plugged into (GP15)
BRIGHTNESS = 0.1      # 0.0 = off, 1.0 = super bright. Keep it LOW (0.1 - 0.3)!
SERPENTINE = True     # True if your screen's rows zig-zag. If the picture looks scrambled, try False

USE_BOOTSEL = True    # True = use the little white BOOTSEL button on the Pico (great for testing)
BUTTON_PIN = 14       # only used if USE_BOOTSEL is False: button between GP14 and GND

ANIMATED = True       # True = emojis wiggle straight away. False = start with still pictures.
HOLD_TIME = 0.6       # how long to hold the button (in seconds) to swap still <-> animated

WIDTH = 8
HEIGHT = 8

# ---------- COLOUR PALETTE ----------
# Each letter is a colour. Colours are (Red, Green, Blue), each 0 to 255.
PALETTE = {
    ".": (0, 0, 0),         # off (black)
    "R": (255, 0, 0),       # red
    "O": (255, 80, 0),      # orange
    "Y": (255, 200, 0),     # yellow
    "G": (0, 255, 0),       # green
    "B": (0, 0, 255),       # blue
    "C": (0, 200, 200),     # cyan
    "P": (150, 0, 200),     # purple
    "K": (255, 20, 100),    # pink
    "W": (255, 255, 255),   # white
}

# ---------- THE EMOJIS ----------
# 8 rows, 8 letters per row. "." means the light is off.
# Each emoji has a MAIN picture, plus some extra pictures that make it move.


# ===== SMILE =====  (it blinks)
SMILE = [
    "..YYYY..",
    ".YYYYYY.",
    "YYBYYBYY",     # blue eyes, so a blink really shows
    "YYYYYYYY",
    "Y.YYYY.Y",
    "YY....YY",
    ".YYYYYY.",
    "..YYYY..",
]
SMILE_BLINK = [          # both eyes shut (the blue vanishes)
    "..YYYY..",
    ".YYYYYY.",
    "YYYYYYYY",
    "YYYYYYYY",
    "Y.YYYY.Y",
    "YY....YY",
    ".YYYYYY.",
    "..YYYY..",
]
SMILE_WINK = [           # one eye shut, the other still blue
    "..YYYY..",
    ".YYYYYY.",
    "YYBYYYYY",
    "YYYYYYYY",
    "Y.YYYY.Y",
    "YY....YY",
    ".YYYYYY.",
    "..YYYY..",
]


# ===== COOL =====  (a shine slides across the sunglasses)
COOL = [
    "..YYYY..",
    ".YYYYYY.",
    "BBBBBBBB",
    "YBBYYBBY",
    "YYYYYYYY",
    "YY....YY",
    ".YYYYYY.",
    "..YYYY..",
]
COOL_SHINE1 = [
    "..YYYY..",
    ".YYYYYY.",
    "BWBBBBBB",
    "YBBYYBBY",
    "YYYYYYYY",
    "YY....YY",
    ".YYYYYY.",
    "..YYYY..",
]
COOL_SHINE2 = [
    "..YYYY..",
    ".YYYYYY.",
    "BBBBBBBB",
    "YWBYYBBY",
    "YYYYYYYY",
    "YY....YY",
    ".YYYYYY.",
    "..YYYY..",
]
COOL_SHINE3 = [
    "..YYYY..",
    ".YYYYYY.",
    "BBBBBWBB",
    "YBBYYBBY",
    "YYYYYYYY",
    "YY....YY",
    ".YYYYYY.",
    "..YYYY..",
]
COOL_SHINE4 = [
    "..YYYY..",
    ".YYYYYY.",
    "BBBBBBBB",
    "YBBYYWBY",
    "YYYYYYYY",
    "YY....YY",
    ".YYYYYY.",
    "..YYYY..",
]


# ===== HEART =====  (it beats: thump-thump, rest)
HEART = [
    ".RR..RR.",
    "RRRRRRRR",
    "RRRRRRRR",
    "RRRRRRRR",
    ".RRRRRR.",
    "..RRRR..",
    "...RR...",
    "........",
]
HEART_SMALL = [
    "........",
    ".RR..RR.",
    ".RRRRRR.",
    ".RRRRRR.",
    "..RRRR..",
    "...RR...",
    "........",
    "........",
]


# ===== STAR =====  (it twinkles and pulses)
STAR = [
    "...YY...",
    "...YY...",
    "YYYYYYYY",
    ".YYYYYY.",
    "..YYYY..",
    ".YYYYYY.",
    ".YY..YY.",
    "YY....YY",
]
STAR_TWINKLE = [         # white sparks on the tips
    "...WW...",
    "...YY...",
    "WYYYYYYW",
    ".YYYYYY.",
    "..YYYY..",
    ".YYYYYY.",
    ".YY..YY.",
    "WY....YW",
]
STAR_SMALL = [           # arms pulled in
    "........",
    "...YY...",
    ".YYYYYY.",
    "..YYYY..",
    "..YYYY..",
    ".YYYYYY.",
    "..Y..Y..",
    "........",
]


# ===== GHOST =====  (eyes look around, fringe wobbles)
GHOST = [
    "..WWWW..",
    ".WWWWWW.",
    "WWBWWBWW",
    "WWBWWBWW",
    "WWWWWWWW",
    "WWWWWWWW",
    "WWWWWWWW",
    "WW.WW.WW",
]
GHOST_LEFT = [
    "..WWWW..",
    ".WWWWWW.",
    "WBWWBWWW",
    "WBWWBWWW",
    "WWWWWWWW",
    "WWWWWWWW",
    "WWWWWWWW",
    "W.WW.WW.",
]
GHOST_RIGHT = [
    "..WWWW..",
    ".WWWWWW.",
    "WWWBWWBW",
    "WWWBWWBW",
    "WWWWWWWW",
    "WWWWWWWW",
    "WWWWWWWW",
    ".WW.WW.W",
]


# ===== CAT =====  (blinks, then meows)
CAT = [
    "OO....OO",
    "OOO..OOO",
    "OOOOOOOO",
    "OGOOOOGO",
    "OOOOOOOO",
    "OOOKKOOO",
    ".OOOOOO.",
    "..OOOO..",
]
CAT_BLINK = [
    "OO....OO",
    "OOO..OOO",
    "OOOOOOOO",
    "OOOOOOOO",
    "OOOOOOOO",
    "OOOKKOOO",
    ".OOOOOO.",
    "..OOOO..",
]
CAT_MEOW = [             # mouth open
    "OO....OO",
    "OOO..OOO",
    "OOOOOOOO",
    "OGOOOOGO",
    "OOOOOOOO",
    "OOKKKKOO",
    ".OOKKOO.",
    "..OOOO..",
]


# ===== DAISY =====  (middle glows, leaf waves)
DAISY = [
    "..W..W..",
    ".WWWWWW.",
    "WWWYYWWW",
    "WWWYYWWW",
    ".WWWWWW.",
    "...GG...",
    ".G.GG...",
    "..GGG...",
]
DAISY_GLOW = [
    "..W..W..",
    ".WWWWWW.",
    "WWWOOWWW",
    "WWWOOWWW",
    ".WWWWWW.",
    "...GG...",
    ".G.GG...",
    "..GGG...",
]
DAISY_LEAF = [
    "..W..W..",
    ".WWWWWW.",
    "WWWYYWWW",
    "WWWYYWWW",
    ".WWWWWW.",
    "...GG...",
    "...GG.G.",
    "..GGG...",
]


# ===== ALIEN =====  (eyes scan side to side while it talks)
ALIEN = [
    "..GGGG..",
    ".GGGGGG.",
    "GGGGGGGG",
    "GPPGGPPG",
    "GGGGGGGG",
    ".GPPPPG.",
    "..GGGG..",
    "...GG...",
]
ALIEN_LEFT = [
    "..GGGG..",
    ".GGGGGG.",
    "GGGGGGGG",
    "PPGGPPGG",
    "GGGGGGGG",
    ".GGPPGG.",
    "..GGGG..",
    "...GG...",
]
ALIEN_RIGHT = [
    "..GGGG..",
    ".GGGGGG.",
    "GGGGGGGG",
    "GGPPGGPP",
    "GGGGGGGG",
    ".GGPPGG.",
    "..GGGG..",
    "...GG...",
]


# ---------- THE LIST OF EMOJIS ----------
# Each line is:  ("name", still picture, [animation frames], seconds per frame)
#
# TIP: putting the same picture in the list twice makes it stay on screen longer.
#      That is how the smile holds its eyes open, then blinks quickly.

EMOJIS = [
    ("smile", SMILE,
     [SMILE, SMILE, SMILE, SMILE, SMILE_BLINK, SMILE, SMILE, SMILE_WINK], 0.25),

    ("cool", COOL,
     [COOL, COOL_SHINE1, COOL_SHINE2, COOL, COOL_SHINE3, COOL_SHINE4, COOL, COOL], 0.12),

    ("heart", HEART,
     [HEART, HEART_SMALL, HEART, HEART_SMALL, HEART_SMALL, HEART_SMALL, HEART_SMALL], 0.12),

    ("daisy", DAISY,
     [DAISY, DAISY_GLOW, DAISY, DAISY_LEAF], 0.4),

    ("star", STAR,
     [STAR, STAR_TWINKLE, STAR, STAR_SMALL], 0.2),

    ("ghost", GHOST,
     [GHOST, GHOST_LEFT, GHOST, GHOST_RIGHT], 0.35),

    ("cat", CAT,
     [CAT, CAT, CAT_BLINK, CAT, CAT_MEOW, CAT_MEOW], 0.3),

    ("alien", ALIEN,
     [ALIEN, ALIEN_LEFT, ALIEN, ALIEN_RIGHT], 0.3),
]


# ---------- THE CODE THAT MAKES IT WORK ----------
np = NeoPixel(Pin(DATA_PIN), WIDTH * HEIGHT)

if not USE_BOOTSEL:
    button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)   # pressed = connects to GND


def button_pressed():
    """True while the button is being held down."""
    if USE_BOOTSEL:
        return rp2.bootsel_button() == 1
    return button.value() == 0


def dim(colour):
    """Turn a colour down so it isn't too bright."""
    r, g, b = colour
    return (int(r * BRIGHTNESS), int(g * BRIGHTNESS), int(b * BRIGHTNESS))


def pixel_number(x, y):
    """Work out which LED on the strip is at column x, row y."""
    if SERPENTINE and y % 2 == 1:
        return y * WIDTH + (WIDTH - 1 - x)   # odd rows run backwards
    return y * WIDTH + x


def draw(picture):
    """Draw one picture on the screen."""
    for y in range(HEIGHT):
        for x in range(WIDTH):
            letter = picture[y][x]
            np[pixel_number(x, y)] = dim(PALETTE[letter])
    np.write()   # send it to the LEDs


def flash(colour, times=2):
    """Blink the whole screen one colour, to say 'something changed'."""
    for _ in range(times):
        np.fill(dim(colour))
        np.write()
        time.sleep(0.07)
        np.fill((0, 0, 0))
        np.write()
        time.sleep(0.07)


# ---------- MAIN LOOP ----------
current = 0          # which emoji we are on
frame = 0            # which animation frame we are on
animated = ANIMATED  # still pictures, or moving ones?


def show():
    """Put the right picture on the screen for how we are set up now."""
    name, still, frames, speed = EMOJIS[current]
    if animated:
        draw(frames[frame % len(frames)])
    else:
        draw(still)


show()

was_pressed = False
hold_handled = True                    # stops a long press also counting as a tap
press_started = time.ticks_ms()
last_frame = time.ticks_ms()
hold_ms = int(HOLD_TIME * 1000)

while True:
    now = time.ticks_ms()
    pressed = button_pressed()

    # --- button just went DOWN: start the stopwatch ---
    if pressed and not was_pressed:
        press_started = now
        hold_handled = False

    # --- still held down long enough? swap still <-> animated ---
    if pressed and not hold_handled and time.ticks_diff(now, press_started) >= hold_ms:
        animated = not animated
        hold_handled = True            # only once per press
        flash((0, 255, 0) if animated else (0, 0, 255))
        frame = 0
        last_frame = time.ticks_ms()
        show()

    # --- button just came UP after a quick tap? next emoji ---
    if was_pressed and not pressed and not hold_handled:
        current = (current + 1) % len(EMOJIS)
        frame = 0
        last_frame = now
        show()

    was_pressed = pressed

    # --- move the animation along ---
    if animated:
        name, still, frames, speed = EMOJIS[current]
        if len(frames) > 1 and time.ticks_diff(now, last_frame) >= int(speed * 1000):
            frame = (frame + 1) % len(frames)
            last_frame = now
            draw(frames[frame])

    time.sleep(0.02)                   # tiny pause so the Pico isn't racing flat out
