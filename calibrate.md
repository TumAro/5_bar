# Setup and calibration

How to bring the rig up from scratch and check it works. Run everything from the repo root.

## Hardware

Servos are ProRange OT5330M. Each has four wires: the three normal ones plus a white wire soldered to the pot wiper for position feedback.

| Wire | Left servo | Right servo |
|---|---|---|
| Brown (GND) | PSU black | PSU black |
| Red (V+) | PSU red | PSU red |
| Yellow (signal) | Arduino D9 | Arduino D10 |
| White (pot wiper) | 1k resistor, then A0 | 1k resistor, then A1 |

- Run one wire from PSU black to an Arduino GND pin. Without it the servos twitch randomly and the Arduino can reset mid-move.
- The Arduino is powered from USB only. Nothing red goes near its 5V or VIN pins.
- PSU at 5.0 V with a 3 A current limit. 6 V is fine too; the wiper never goes above ~3.3 V.
- Push every jumper in firmly. A loose white wire made the servos grind and wander, and it took a while to find.

## Flash the Arduino

```
arduino-cli compile -u -p /dev/ttyACM0 src/arduino/five_bar_servo
```

The sketch takes `left,right` in degrees over serial at 115200 and replies with the two pot readings (raw counts, 0 to 1023). Each reply is read right after the command, before the servo has moved, so it shows the previous position. Send a command twice if you want the settled reading.

Settings in the sketch:

- `US_MIN` / `US_MAX` (500 / 2500 µs): pulse widths for 0 and 180. These give the full 180 degree sweep on this servo.
- `L_MIN`, `L_MAX`, `R_MIN`, `R_MAX` (30 to 150): every command is clamped to these so the cranks can't hit the frame. To find the real limits, jog each servo until the crank touches, back off about 5 degrees and put that number in.

Close any serial monitor before running the Python scripts. Only one program can hold the port.

## Servo offsets

With the linkage on, send `95,98` from the serial monitor. Both cranks should point straight towards the end effector, at right angles to the line between the two shafts. If they don't, nudge the numbers until they do, then set in `config.toml`:

```
[servo]
OFFSET_L = 5.0   # left number - 90
OFFSET_R = 8.0   # right number - 90
```

If a crank is more than about 7 degrees off, re-seat the horn one tooth over first (the spline has 25 teeth, 14.4 degrees each) and tighten the horn screw. A marker line across the horn and the servo top shows if it ever slips.

## Hardware check

Take the couplers off first. This test sends each servo to random positions on its own, which the assembled linkage can't follow.

```
uv run python -m test.serial_stress_test
```

It makes 30 random moves and checks each one against the pot reading. Expect 0 fails and a worst error of around 3 to 4 degrees. If it fails:

- Fails on big moves only: the servo hadn't arrived yet. Raise `SETTLE`.
- Fails always on one servo: check its white wire, horn screw and solder joint.
- "Arduino reset during move": ground or power. Check the GND wire and the PSU's CC light.

## Camera

The overhead camera is a Logitech C920. `config.toml` finds it by USB id, so any port works:

```
CAM = "/dev/v4l/by-id/usb-046d_HD_Pro_Webcam_C920_A0B57DCF-video-index0"
```

If it opens but gives no frames, something else is using it (a browser tab with camera access is the usual culprit).

Mount it looking straight down. Check with a phone level app held flat against the front of the camera. Tilt skews every angle.

## Markers

Print `markers/markers_A4.pdf` at actual size (not fit to page) on matte paper. Measure a black square afterwards; it must be 40 mm. Glue them to card.

| ID | Where |
|---|---|
| 10 | Left anchor: on the frame, beside the left servo |
| 11 | Right anchor: same on the right |
| 0 | Middle of the left proximal link, one edge along the link |
| 1 | Middle of the right proximal link, same way |
| 2 | End effector (not used yet) |

Raise the anchors on blocks so they sit at the same height as the crank markers. Ours are 14 cm out from each pivot. The exact distance doesn't matter for angles.

The crank angle comes from the crank marker's own rotation, measured against the line between the two anchors. That's why the anchors don't need to be on the pivots, and why moving or rotating the camera doesn't change the calibration.

## Camera calibration

Linkage on. This moves both cranks to home, averages 30 frames and writes `THETA_OFFSET_L` / `THETA_OFFSET_R` into `config.toml`.

```
uv run python -m test.aruco_calibrate
```

Run it every time the camera is remounted. Compare with the last values:

| Date | L | R | Spread |
|---|---|---|---|
| 2026-09-28 | 1.5663 | 1.4579 | |
| 2026-10-09 | 1.5588 | 1.4694 | 1.29 deg |

A change under 1 degree is normal. More than that means a marker moved or the camera is tilted.

The spread is how much the angle wobbled between frames. Under 1 degree is good. Higher usually means camera vibration or a marker that's too small in the image.

## Full check

Linkage on.

```
uv run python -m test.aruco_smoke_test
```

The arm draws a 50 mm circle one way, then back the other way, 8 seconds per loop. The window shows each detected marker, plus two lines:

- `cmd`: angle sent to each crank
- `cam`: angle the camera measured

`cam` trails `cmd` a little. That's the servos lagging behind the moving target, and it's what the ILC is meant to fix. Press `q` to stop; the cranks go back home.

## Every session, short version

1. Plug in the Arduino and the camera. PSU on.
2. Camera level, all four markers in view.
3. `uv run python -m test.aruco_calibrate` and compare the offsets with the table above.
4. `uv run python -m test.aruco_smoke_test`

Run the stress test only if something seems off with the servos.
