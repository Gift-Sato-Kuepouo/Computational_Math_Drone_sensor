# sensor_logger — downward light sensor sketch

Arduino sketch for the Track A package (sensor flying with the drone) and for Track B
(sensor read at the landing square after touchdown).

It does three things:

1. **Line counting** — counts grid-line crossings (threshold + 300 ms debounce).
2. **Shade classification** — reports `white` / `gray` / `black` under the sensor (nearest
   calibrated anchor), which is how the code says "landed on target 2" or "missed".
3. **CSV logging** — one line every 20 ms so the whole flight can be saved and graphed.

## Works with

| Board | Notes |
|---|---|
| Seeed XIAO nRF52840 Sense | pin `A0` (default) |
| ESP32-C3 SuperMini | pin `A0` |
| Arduino Nano 33 BLE / Nano Every / Uno-class | pin `A0` |

Any board with one ADC input works; nothing in the sketch is board-specific.

## Wiring (Pololu QTR-1A)

| QTR-1A | Board |
|---|---|
| VIN | 3V3 (5 V boards: VIN/5 V) |
| GND | GND |
| OUT | **A0** |

Other sensors (S2–S6 in [docs/hardware.md](../../docs/hardware.md)) wire the same way if they
have an analog output.

## Upload

1. Open `sensor_logger.ino` in the Arduino IDE (or `arduino-cli compile`).
2. Select your board and port, upload.
3. Open the Serial Monitor at **115200 baud**.

## Serial commands

Send these characters in the Serial Monitor input box (no newline needed):

| Key | Action |
|---|---|
| `w` | capture **white floor** reading (hold sensor at flight/landing height over white floor) |
| `g` | capture **gray target** reading |
| `t` | capture **tape line** reading |
| `b` | capture **black target** reading |
| `z` | reset the line counter — do this **before every flight** |
| `p` | print a summary: all anchors, the computed line threshold, the current line count |

Each capture averages 50 samples (~1 s) and answers e.g. `captured,w,247`.

## Log format

Header printed at boot:

```
time_ms,reading,line_count,shade
1240,263,0,white
1260,268,0,white
1280,742,1,black
...
```

- `time_ms` — milliseconds since boot
- `reading` — smoothed ADC value (higher = darker)
- `line_count` — grid lines crossed since the last `z`
- `shade` — nearest calibrated anchor under the sensor

**Saving a flight:** start a serial capture (Serial Monitor → log to file, or
`arduino-cli monitor`, or any serial terminal's logging), press `z`, fly, land, wait ~2 s for
the reading to settle, then press `p`. Stop the capture and save as `flight_trialN.csv`.
Spreadsheet-friendly: column 1 = time, column 2 = reading, column 3 = line count.

## Track B (payload-free) workflow

1. Keep the board on the bench, sensor in hand, same calibration.
2. Drone flies with nothing attached.
3. After touchdown, place the sensor **flat on the floor at the drone's centre mark**.
4. Read the `shade` value (or press `p`) → that is the measured landing square.
5. For the gradient strip, slide the sensor along the strip and log readings at each 10 cm mark,
   then fit with [`code/calibrate_gradient.py`](../calibrate_gradient.py).

## Constants you may need to change

| Constant | Default | Meaning |
|---|---|---|
| `SENSOR_PIN` | `A0` | analog input |
| `DEBOUNCE_MS` | `300` | minimum gap between two line counts (raise to 500 if a line counts twice) |
| `SAMPLE_INTERVAL_MS` | `20` | log rate (50 lines/s) |
| `SMOOTHING_FACTOR` | `0.25` | smoothing strength; lower = smoother but laggier |
| anchor defaults | 250 / 550 / 800 / 850 | placeholders — **always re-capture with `w` `g` `t` `b`** |

Thresholds are *derived* from the anchors at runtime (`line threshold = (white + tape) / 2`),
so you only ever calibrate the four surfaces, never edit maths in the code.
