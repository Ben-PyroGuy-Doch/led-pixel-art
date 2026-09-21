# LED Pixel Art Project 🎨💡

Make your own light-up pictures on a screen of 64 tiny coloured lights (an 8x8 grid, like a mini Minecraft screen) — and press a button to flip between them!

**You need:**
- Raspberry Pi Pico W (the little computer)
- 8x8 LED screen (it has 3 wires: power, ground, data)
- 3 jumper wires
- A USB cable
- A computer with **Thonny** installed (free app for writing the code)

---

## Step 1: Wire it up

**Unplug the USB cable first, before touching any wires.**

Connect the 3 wires from the LED screen to the Pico like this:

| Wire on the screen | Goes to this pin on the Pico |
|---|---|
| 5V (or VCC, or +) | **VBUS** — top right corner, next to the USB plug |
| GND (or -) | **GND** |
| DIN (Data In) | **GP15** |

There are two data wires on some screens, DIN and DOUT — make sure you use **DIN**.

## Step 2: Open Thonny and connect the Pico

1. Open Thonny on the computer.
2. Look at the bottom right corner — click there and choose **MicroPython (Raspberry Pi Pico)**.
3. Plug the USB cable in now. You should see `>>>` appear at the bottom of the screen — that means the Pico is talking to the computer.

## Step 3: Make one light turn on

This is just a test, to check the wiring works. Type this into the big box in Thonny, then click the green **Play** button (▶):

```python
from machine import Pin
from neopixel import NeoPixel

np = NeoPixel(Pin(15), 64)
np[0] = (20, 0, 0)
np.write()
```

If one dim red light turns on — great, the wiring's good! If nothing happens, double check DIN is on GP15 and the wires are pushed in properly.

*(Curious what the numbers mean? `(20, 0, 0)` is how much Red, Green and Blue to mix — like mixing paint. `np[0]` means "the first light".)*

## Step 4: Run the real project

1. Open the file `main.py` in Thonny (**File → Open**, then find it on the computer).
2. Click **Play** ▶. A smiley face should appear and start blinking its eyes!
3. Find the little white button on the Pico called **BOOTSEL**.

Here's what the button does:

| What you do | What happens |
|---|---|
| **Quick tap** (press and let go fast) | Shows the **next** emoji |
| **Hold it down** for about 1 second | The screen flashes green or blue, and switches between **wiggling** (animated) and **frozen** (still) pictures |

There are 8 emoji to find: smile, sunglasses, heart, daisy, star, ghost, cat, and alien. Keep tapping to see them all, then try holding the button to see them move!

## Step 5: How the animation actually works

Open `main.py` and look near the bottom for a list called `EMOJIS`. Each emoji has its own line, like this:

```python
("heart", HEART, [HEART, HEART_SMALL, HEART, HEART_SMALL], 0.12)
```

That line means: *"This emoji is called heart. Its normal picture is HEART. When animated, flip between these pictures in this order. Wait 0.12 seconds between each one."*

That's the whole trick behind animation — it's not really moving, it's just **swapping between a few slightly different pictures really fast**, like a mini flipbook. Try changing that last number (`0.12`) to `0.5` and see the heartbeat slow right down.

## Step 6: Save it onto the Pico for good

Right now, the code is only running because Thonny is "lending" it to the Pico. Unplug the USB and it forgets everything! To make it work on its own (like a real light you can plug into any charger):

1. With `main.py` still open, go to **File → Save as...**
2. Choose **Raspberry Pi Pico** as the save location (not "This computer").
3. Name it exactly `main.py`.
4. Now unplug it from the computer and plug it into any USB power — a wall charger, a power bank, anything. The light show should start all by itself.

Want to change the code later? Open Thonny, open `main.py` **from the Pico** this time, make your changes, then save it the same way again.

## Step 7: Design your own emoji

Print out `pixel-art-templates.pdf` — it has blank 8x8 grids and the colour key on paper. Best way to invent a new emoji:

1. **Draw it on paper first.** Colour in squares, or write the letter for each colour.
2. **Find `PALETTE` in `main.py`** — this is the key that turns letters into colours (`R` = red, `B` = blue, `.` = off, and so on).
3. **Type your grid into the code**, one row at a time, 8 letters per row, like:
   ```python
   MYPICTURE = [
       "........",
       "..YY....",
       ".YYYY...",
       "..YY....",
       "........",
       "........",
       "........",
       "........",
   ]
   ```
4. **Add it to the `EMOJIS` list** so the button can find it:
   ```python
   ("mypicture", MYPICTURE, [MYPICTURE], 0.3)
   ```
5. Save and run it — your emoji should now show up when you tap the button!

Want it to move? Draw 2 or 3 slightly different versions (like `MYPICTURE_2`) and list them all instead of just `[MYPICTURE]`.

## Step 8: 3D print the case

There's a file called `diffuser1-Body.stl` — a frame to hold the Pico and LED screen. Print it in PLA, and test-fit the screen and Pico in it once it's done, in case anything needs a little trim.

## Good to know

- Keep the lights dim (`BRIGHTNESS` near the top of the code) — very bright lights use a lot of power.
- Nothing lighting up? Check DIN is on GP15 and the wires are firmly pushed in.
- Colours look wrong (red shows as blue, etc.)? Some screens wire their colours in a different order — ask for help checking this.

## Challenge ideas 🌟

1. Make a smiley that blinks both eyes at once, not just one.
2. Design the first letter of your name.
3. Make a rainbow, one colour per row.
4. Invent a character that "walks" across the screen frame by frame.
5. Make your own colour and give it a name in `PALETTE`.
