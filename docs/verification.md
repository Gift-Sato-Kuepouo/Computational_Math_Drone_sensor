# Verification — proving the prediction with sensor data

Two methods, used together:

- **Method A — count the grid lines:** checks **how far** the drone flew.
- **Method B — read the landing square:** checks **where** the drone finished.

A reflectance sensor (IR LED + phototransistor) pointing down gives one number for everything:
**more light coming back → lower reading** (for the Pololu QTR-1A: white floor = low ADC,
black tape = high ADC).

---

## 1. Calibration table

Do this *at the height you will actually sense at*, in the same room lighting you will fly in.

Procedure: hold the drone (battery off) so the sensor sits at sensing height; place each surface
under it; record the average of ~20 readings (the logger prints them continuously).

| Surface | Reading (ADC) | Used as |
|---|---|---|
| White floor | `R_white` (e.g. 250) | low anchor |
| Gray target square | `R_gray` (e.g. 550) | mid anchor |
| Black tape line | `R_tape` (e.g. 800) | line threshold source |
| Black target square | `R_black` (e.g. 850) | high anchor |

**Thresholds derived from the table:**

```
line threshold   = (R_white + R_tape) / 2
shade boundary 1 = (R_black + R_gray) / 2     → below: "gray or white"
shade boundary 2 = (R_gray + R_white) / 2     → below: "white"
```

Enter these three numbers into [`code/sensor_logger/sensor_logger.ino`](../code/sensor_logger/sensor_logger.ino)
constants (or send them over serial — see the [sketch README](../code/sensor_logger/README.md)).

---

## 2. Method A — line counting (checks distance)

**Setup:** black tape grid lines every 1 m across the start→target corridor on a light floor.

**Detection logic (implemented in the sketch):**

1. Smooth the reading (moving average) so prop vibration and ambient flicker don't chatter.
2. `over_line = reading > line_threshold`.
3. On a **rising edge** (floor → line), count **only if** at least `DEBOUNCE_MS` (≈ 300 ms) has
   passed since the last count — one physical line can not be counted twice.

```
measured distance = lines crossed × 1 m
predicted distance = sum of the hand-calculated leg lengths
compare: difference = measured − predicted
```

**What it tells you:** distance along the path.
**What it does *not* tell you:** sideways drift — the drone can slide a whole square sideways and
still count the correct number of lines. That is why method B is mandatory.

*Expected magnitudes (sanity check):* at 0.5 m/s a 1 m line spacing is crossed every 2 s, so
300 ms debounce is safely short; raise it to 500 ms if a single line ever counts twice.

---

## 3. Method B — landing shade (checks final position)

**Setup:** three target squares in different shades (black, gray, white) where the targets sit.

**At touchdown** the logger prints the smoothed reading; nearest-anchor classification gives:

| Condition (on calibrated readings) | Report |
|---|---|
| `reading ≥ boundary 1` | **landed on target: black square** |
| `boundary 2 ≤ reading < boundary 1` | **landed on target: gray square** |
| `reading < boundary 2` | **landed on target: white square** |

Students then compare: *predicted* square (from the plan) vs *reported* square → hit or miss,
and if the drone landed outside all three squares, the nearest anchor still reports its best
guess — record it as a miss.

**Track B (payload-free):** identical procedure — the student places the sensor flat on the
floor at the drone's centre mark right after landing and reads the serial monitor.

---

## 4. Gradient strip — the finer measure (`position = a × reading + b`)

Print a 1 m grayscale ramp across one target square (0 = white at position 0.00 m → 100 = black
at position 1.00 m).

**Collect calibration data:** slide the sensor along the strip in fixed steps (e.g. every 10 cm),
record `(reading, position)` — at least 8 pairs.

**Fit by hand (grades 5–8 use two points or a ruler line; grades 9–12 use least squares):**

```
two-point form:  a = (position₂ − position₁) ÷ (reading₂ − reading₁)
                 b = position₁ − a × reading₁
                 position = a × reading + b
```

Least squares (9–12 / script):

```
a = Σ(rᵢ − r̄)(pᵢ − p̄) ÷ Σ(rᵢ − r̄)² ,    b = p̄ − a·r̄ ,    p = a·reading + b
```

Run [`code/calibrate_gradient.py`](../code/calibrate_gradient.py) on your table (or `--demo` to
see a synthetic example) — it prints `a`, `b` and `R²`. Example output shape:

```
fit: position = -0.00143 * reading + 1.286     R^2 = 0.99
reading 550 -> position 0.50 m
```

*(Those numbers are from synthetic data — your strip, sensor and height give your own.)*

**Using the fit:** at landing, `position = a × reading + b` converts the sensor number into a
position **along the strip** — a continuous measurement instead of a square name, and a real
linear model the students derived, checked and critiqued.

---

## 5. Error, tolerance, correction — from data to the next flight

```
error vector  e = (measured − target)
error size    |e| = √(ex² + ey²)
pass          |e| ≤ 0.25 m
correction    new scale = old scale × (target distance ÷ measured distance)
```

Full formulas and the worked example: [math-model.md](math-model.md).
Record every trial in [worksheet/trials_template.csv](../worksheet/trials_template.csv), then
graph **error vs trial number** — the curve should drop and flatten (that is convergence, not
"the drone got lucky").

---

## 6. Honest limits (say these out loud in class)

| Limit | Consequence | Mitigation |
|---|---|---|
| Line count = distance only | Sideways drift invisible | Landing shade / gradient position (method B) |
| Reading depends on height | Calibrated at 1 cm, sensed at 10 cm → wrong thresholds | Calibrate at flight height; fly sensing passes low and steady |
| Ambient light | LDR option drifts with sun/clouds; IR less so but not immune | Constant lighting; re-zero before each session |
| One shade per square | Can't tell *where* in the square it landed | Gradient strip |
| Sensor noise, battery sag | `k` drifts over the day | Re-measure speed `v` each session; expect a few trials |
| Debounce window | Very fast low flights can miss a count | Check `DEBOUNCE_MS` against actual speed |

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Counts a line twice | Debounce too short, or line too wide | Raise `DEBOUNCE_MS`; use one tape width consistently |
| Counts no lines | Threshold above every reading | Recalibrate at flight height; check sensor is 5–10 mm below frame, not shadowed |
| Readings all near 0 | Sensor wired to GND/3V3 swapped, or LED unpowered | Check VIN/GND/OUT wiring |
| Readings flatline high | Sensor covered / pressed against floor | Re-mount, confirm gap |
| Shade always "black" | Calibrated in different lighting or height than flown | Redo calibration table in flight conditions |
| Landing correct but error large | Drift during flight, not at landing | Trust method B for position; add a second marker mid-course (roadmap Phase 5) |
