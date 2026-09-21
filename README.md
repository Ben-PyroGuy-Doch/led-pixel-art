# LED Pixel Art — Pico W 8x8 Emoji Light

A tiny, button-driven pixel-art light built around a Raspberry Pi Pico W and an 8x8 WS2812B (NeoPixel) LED matrix. Tap the button to flip through emojis; hold it to switch between still and animated pictures. Built as a hands-on STEM project.

![status](https://img.shields.io/badge/status-in--progress-yellow)

## What's in here

| File | What it is |
|---|---|
| [`main.py`](main.py) | The MicroPython code that runs on the Pico W |
| [`GUIDE.md`](GUIDE.md) | Step-by-step build guide: wiring, Thonny setup, running the code, saving it to the Pico, printing the case |
| [`WORKSHOP.md`](WORKSHOP.md) | A ~2 hour STEM lesson plan built around this project — wiring, coordinates, loops, state machines, 3D printing |
| [`diffuser1-Body.stl`](diffuser1-Body.stl) | 3D-printable frame/case for the Pico + LED matrix (~94 x 84 x 63 mm) |
| [`pixel-art-templates.pdf`](pixel-art-templates.pdf) | Printable 8x8 grid + colour-key worksheets for planning new emoji on paper before typing them in |
| [`board-backup/main.py.from-board`](board-backup/main.py.from-board) | A pre-animation version of `main.py`, pulled off the physical board as a backup |

## Hardware

- Raspberry Pi Pico W
- 8x8 WS2812B / NeoPixel LED matrix (3-wire: 5V, GND, DIN)
- 3 jumper wires
- USB cable
- 3D printer + PLA (for the case)

## Quick start

1. Wire the LED matrix to the Pico (see `GUIDE.md` Step 1).
2. Install [Thonny](https://thonny.org/) and set the interpreter to MicroPython (Raspberry Pi Pico).
3. Open `main.py` in Thonny and run it.
4. Tap the Pico's BOOTSEL button → next emoji. Hold it (~1s) → toggle still/animated.
5. Save `main.py` onto the Pico itself (File > Save as > Raspberry Pi Pico) so it runs standalone off any USB power.

Full details, including how the zig-zag LED wiring maps to an 8x8 grid and how to draw your own emoji, are in [`GUIDE.md`](GUIDE.md).

### This board, specifically

| | |
|---|---|
| Board | Pico W, MicroPython **v1.23.0** (2024-06-02) |
| Serial port | **COM4** |
| Data pin | GP15 (physical pin 20) → matrix `DIN` |
| Matrix | 8x8, serpentine wiring (`SERPENTINE = True`) |
| Button | BOOTSEL (`USE_BOOTSEL = True`), or a button GP14→GND |

Deploy without opening Thonny, using [`mpremote`](https://docs.micropython.org/en/latest/reference/mpremote.html):

```bash
python -m mpremote connect COM4 fs cp main.py :main.py
python -m mpremote connect COM4 exec "import machine; machine.reset()"
```

- **Close Thonny's connection first** (Run → Disconnect, or close Thonny) — it holds the COM port open and `mpremote` fails with "failed to access COM4 (it may be in use by another program)".
- **Always finish with `machine.reset()`** — an `mpremote` session takes over the REPL and leaves `main.py` stopped otherwise; `soft-reset` isn't reliable for this.
- The reset command usually ends with `SerialException: ClearCommError failed` — **that's the success case**, the board just dropped USB mid-command. Confirm it's back with `python -m mpremote devs` (passive check, won't interrupt the running script).
- **Thonny interrupts `main.py` the moment it connects.** If the board "only works unplugged from the PC," that's why, not a code fault.
- Keep `BRIGHTNESS` at 0.1–0.3. All 64 pixels at full white draws roughly 3.8A — far past what USB can supply, and it will brown out the Pico.
- Verify LED colour order with **green or blue test pixels, never red** — red looks correct even when the colour order is swapped.

## Features

- 8 built-in emojis (smile, cool, heart, daisy, star, ghost, cat, alien), each with its own small animation
- Single button controls both emoji selection (tap) and animation mode (hold)
- Adjustable brightness, animation speed, and LED wiring order (`SERPENTINE`) via constants at the top of `main.py`
- Easy to extend — each emoji is just a Python list of 8-character strings, one letter per LED colour

## Customising

Add your own emoji by drawing an 8x8 grid of letters (see `PALETTE` in `main.py` for the colour key), then adding it to the `EMOJIS` list. See `GUIDE.md` Step 7 for the full how-to.

## Status

The case (`diffuser1-Body.stl`) is a first-pass frame — print settings and fit are in `GUIDE.md`, but final assembly notes are still pending a test print.

## License

Personal / hobby project. No license specified yet — add one if you plan to make this repo public.
