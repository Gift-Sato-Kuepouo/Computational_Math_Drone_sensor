# Student worksheet — Computational Math × Drone Sensor

**Team name:** ______________________  **Date:** ____________  **Drone:** Eagle 125F

**Roles:** Pilot __________ · Calculator __________ · Sensor operator __________ ·
Recorder __________ · Safety spotter __________

**Session info:** speed `v` = ________ m/s (median of 3 timed runs over a ______ m leg)
tolerance = ________ m · Track A / Track B (circle one) · package mass = ________ g

---

## Part 1 — Plan (before flying)

Start point and three targets (teacher gives coordinates):

| Point | x (m) | y (m) |
|---|---|---|
| Start | | |
| Target 1 | | |
| Target 2 | | |
| Target 3 (final) | | |

### Leg table — calculate by hand

Formulas: `d = √(Δx² + Δy²)` · `θ = atan2(Δy, Δx)` · `turn = θ_new − θ_old` · `t = d ÷ v`

| Leg | From → To | Δx | Δy | d (m) | θ (°) | Turn (°) | t (s) |
|---|---|---|---|---|---|---|---|
| 1 | → | | | | | | |
| 2 | → | | | | | | |
| 3 | → | | | | | | |
| **Total** | | | | **Σ d =** | | | **Σ t =** |

*Check with a neighbour before flying: same distances? same headings?*

---

## Part 2 — Calibrate the sensor (bench, before flying)

Sensor at **flight/landing height**, same lighting as the flight area, average of ~1 s of readings:

| Surface | Reading (ADC) |
|---|---|
| White floor `R_white` | |
| Gray target `R_gray` | |
| Tape line `R_tape` | |
| Black target `R_black` | |
| **Line threshold** = (`R_white` + `R_tape`) ÷ 2 | |

**Bench test at sensing height:** sweep the sensor over a tape line.
`ADC_tape − ADC_white` = ________ · Is it ≥ 100?  yes / no (if no: fly lower or see
[hardware.md §8](../docs/hardware.md)).

---

## Part 3 — Fly, measure, correct

Press `z` (reset line counter) before every flight. After landing wait 2 s, then read the shade
and press `p`.

| Trial | Scale sent | Lines crossed → measured distance (m) | Predicted distance (m) | Landing shade / measured (x, y) | Error `|e|` (m) | Pass? (≤ tol) | New scale = old × (target ÷ measured) 


Formulas: `|e| = √((x − x_t)² + (y − y_t)²)` · `new scale = old scale × (target distance ÷ measured distance)`

**Gradient strip (optional, finer measure):** fit `position = a × reading + b`

- Two points used: (reading₁, position₁) = (________, ________), (reading₂, position₂) = (________, ________)
- `a` = ____________ · `b` = ____________ · Landing reading ________ → position ________ m
- Script check: `python code/calibrate_gradient.py ________.csv` → `a` = ________ `R²` = ________

---

## Part 4 — Graph and conclude

**Graph:** x-axis = trial number (1, 2, 3 …), y-axis = error in metres. Draw a horizontal line
at your tolerance.









**Conclusion (4 sentences):**

1. How many trials until `|e|` ≤ tolerance? ______________________________
2. Final scale factor: __________ — what does it mean about the real drone?
   ___________________________________________________________________
3. Did line counting (Method A) and landing shade (Method B) agree? Why/why not?
   ___________________________________________________________________
4. One honest limitation of our measurement: __________________________________

**Error check:** swap worksheets with another team — do you get the same distances?
