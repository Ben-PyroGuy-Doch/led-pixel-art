# LED Pixel Art — STEM Workshop Plan

**For:** one parent + one child (adapt group size as needed)
**Age guide:** upper primary / early secondary, reading independently
**Time:** ~2 hours, split into 5 modules (stop and resume freely between them)
**Output:** a standalone, 3D-printed LED pixel-art light with a button-driven emoji show

This plan wraps the existing build (`main.py`, `GUIDE.md`, `diffuser1-Body.stl`) into a run-able workshop session: what to say, what to check, and which STEM idea each step is secretly teaching.

---

## Materials checklist

- [ ] Raspberry Pi Pico W
- [ ] 8x8 LED screen (WS2812B / NeoPixel type, 3-wire)
- [ ] 3 jumper wires
- [ ] USB cable + computer with Thonny installed
- [ ] `main.py` (provided)
- [ ] `diffuser1-Body.stl` (provided) + access to a 3D printer
- [ ] Pen and paper (for Module 2's planning exercise)

---

## Learning objectives

By the end, the child should be able to:

1. Explain what each of the 3 wires on the LED screen does (power, ground, data).
2. Read and edit a simple 2D list of characters to change what a picture shows.
3. Explain RGB colour mixing well enough to invent a new colour.
4. Explain, in their own words, what a `for` loop is doing and why it saves typing.
5. Describe the difference between a **tap** and a **hold**, and why the code has to measure time to tell them apart.
6. Say what a "still" list vs "animated" list of pictures does in `EMOJIS` and add one of their own.

---

## Module 1 — Wiring & first light (20 min)

**STEM idea:** *circuits* — power, ground, and a signal wire are three different jobs, and mixing them up is how things break.

1. USB unplugged. Point out the three wires on the screen and ask: which do you think carries power, which is the "return path", and which carries the picture data?
2. Wire it up using `GUIDE.md` Step 1 (5V→VBUS, GND→GND, DIN→GP15).
3. Open Thonny, connect, run the single-pixel snippet from `GUIDE.md` Step 3.
4. **Checkpoint:** one dim red light on. If nothing lights up, this is the moment to recheck wiring — not later once there's more code to untangle.

*Talking point:* ask what would happen if DIN and GND were swapped. (Nothing works, and it's usually not damaging — a good moment to normalise "wired it wrong, no big deal, just fix it.")

## Module 2 — Coordinates & the zig-zag (20 min)

**STEM idea:** *coordinate systems and indexing* — a flat strip of 64 LEDs is turned into an 8x8 grid purely by how the numbers map to positions.

1. Run the row test from `GUIDE.md` Step 4. Confirm rows are straight; if scrambled, flip `SERPENTINE`.
2. On paper, draw an 8x8 grid. Ask the child to number the squares 0–63 the way they think the strip is wired (left-to-right every row). Then show them `pixel_number()` in `main.py` and how the zig-zag (`WIDTH - 1 - x` on odd rows) changes that numbering.
3. Have them predict, before running it, what `np[9]` will look like on the physical screen. Run it and check.

*Why this matters:* this is the same idea as screen pixels, spreadsheet cells, and array indexing generally — a real "aha" moment for how software turns numbers into physical positions.

## Module 3 — Drawing with letters & loops (30 min)

**STEM idea:** *encoding/decoding* (a letter standing in for a colour) and *loops* (why `draw()` doesn't need 64 separate lines).

1. Look at `PALETTE` together. Ask: why use letters instead of typing `(255,0,0)` every time? (Readability — this is exactly why programmers invent shorthand.)
2. Pick an existing picture (e.g. `HEART`) and have the child change a few letters, predicting the result before running it.
3. Walk through `draw()`'s nested loop by hand: cover the code, and have them narrate what it does row by row, like reading a recipe.
4. **Activity:** on paper, design an 8x8 picture as a grid of letters (their own initial, a simple face, anything). Type it in as a new list, following the format of `HEART`.
5. Invent one new colour by adding a line to `PALETTE` (RGB mixing: ask what colour `(255,0,255)` should make before running it).

*Checkpoint:* their own picture is on the screen and they can say what at least 3 of the letters mean.

## Module 4 — Buttons, timing & state (30 min)

**STEM idea:** *input debouncing and state machines* — the code has to actively measure elapsed time to tell a quick tap from a deliberate hold, and it remembers "which mode am I in" between loop cycles.

1. Run `main.py` in full. Tap BOOTSEL — next emoji. Hold it — mode flips (still/animated), screen flashes.
2. Open the code together and find `press_started` and `hold_handled`. Ask: how does the Pico know the difference between a tap and a hold, if both start the same way (button goes down)? Let them find the answer: it's a stopwatch (`time.ticks_diff`) against `HOLD_TIME`.
3. Point at `animated = ANIMATED` near the bottom and the `if animated: ... else: ...` in `show()`. This is a **state variable** — one bit of memory that changes what the same button does next. Ask: what's another device that behaves differently depending on a mode it remembers? (TV remote's input-select, a washing machine dial, a game's pause state are all fair answers.)
4. **Activity:** add one new emoji entry to the `EMOJIS` list — reuse a picture they made in Module 3, give it 2-3 animation frames of their own design, and tune its speed number.

*Checkpoint:* their new emoji appears in the button cycle, in both still and animated mode.

## Module 5 — Saving it for good & the case (20 min, plus print time offline)

**STEM idea:** *firmware vs. a live session* — running code from Thonny is temporary; saving it onto the device's own storage is what makes it work standalone. Plus a first pass at CAD/manufacturing: slicer settings, print orientation, and tolerance (parts that need to physically fit together).

1. Follow `GUIDE.md` Step 6: save `main.py` onto the Pico itself (not "This computer"), unplug from Thonny, power it from something else, and watch it run with no laptop attached.
2. Slice and print `diffuser1-Body.stl` (`GUIDE.md` Step 8). While it prints: ask what they think 15-20% infill means, and why a frame doesn't need to be solid plastic to be strong.
3. Once printed, test-fit the Pico and LED screen into the frame before calling it finished.

---

## Extension challenges (send home / next session)

1. Design a whole new emoji from scratch, animated, and add it to the show.
2. Make one emoji's animation loop faster or slower and describe, in the wiring/timing terms from Module 4, why the number does that.
3. Wire a real push-button (Step in `GUIDE.md`: GP14 + GND) instead of BOOTSEL, and explain what changed in the code (`USE_BOOTSEL = False`) versus what stayed the same.
4. Write a short "user manual" for the finished light — what does a tap do, what does a hold do — as if for someone who's never seen it.

## Facilitator notes

- Every "predict, then run" moment above is deliberate — guessing before testing is the core habit this workshop is trying to build, more than any single Pico fact.
- If short on time, Modules 1–3 alone make a complete, satisfying session (a working, editable pixel-art light) — Modules 4–5 add the button logic and the physical case.
- Keep `BRIGHTNESS` low throughout (0.1–0.3) — worth mentioning why (current draw), not just enforcing it.
