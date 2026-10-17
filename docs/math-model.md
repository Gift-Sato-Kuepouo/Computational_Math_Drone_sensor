# The mathematical model

Everything the students calculate by hand lives here. The simulation
([`code/simulation.py`](../code/simulation.py)) is a literal implementation of these formulas.

## 1. Coordinates and legs

The flight area is a 5 × 5 grid in metres. Each team gets a start point and three targets:

```
points = [(0, 0), (2, 1), (3, 3), (1, 4)]     # start first — the model uses (0, 0) as origin
```

A **leg** is the straight hop between two consecutive points.

| Quantity | Formula | Grade band |
|---|---|---|
| Distance of a leg | `d = √(Δx² + Δy²)` | 5–8 (Pythagorean theorem) |
| Heading of a leg | `θ = atan2(Δy, Δx)` in degrees, 0° = +x axis, counterclockwise | 5–8, 9–12 (atan2) |
| Turn at each corner | `turn = θ_new − θ_old` | 5–8 |
| Predicted flight time | `t = d ÷ v`, where `v` is the drone's **measured** speed | 5–8 (rate problems) |
| Total predicted time | sum of all `t` | 5–8 |

**Measure `v` once per session:** fly one leg of known length timed with a stopwatch (or count
frames on a phone video) and take the median of three runs. Write it on the worksheet — every
prediction depends on it.

## 2. Worked example (the reference scenario)

Points `(0,0) → (2,1) → (3,3) → (1,4)`:

| Leg | Δx | Δy | d (m) | θ (°) | Turn at corner (°) | t at v = 0.5 m/s |
|---|---|---|---|---|---|---|
| 1 | +2 | +1 | √5 ≈ 2.24 | 26.57 | +26.57 (from start heading) | 4.47 s |
| 2 | +1 | +2 | √5 ≈ 2.24 | 63.43 | **+36.87** | 4.47 s |
| 3 | −2 | +1 | √5 ≈ 2.24 | 153.43 | **+90.00** | 4.47 s |
| **Total** | | | **6.71** | | | **13.42 s** |

*(Numbers rounded to 2 decimals; students show the surd form `√5` first.)*

## 3. Error and the pass rule

After the flight, the sensor data gives a measured landing point `(x, y)`:

```
error vector   e = (measured − target) = (x − x_target, y − y_target)
error size     |e| = √(ex² + ey²)
pass rule      |e| ≤ tolerance        (default 0.25 m = one quarter of a square)
```

The tolerance is a **classroom design decision** — tighten it to 0.10 m for grades 9–12,
loosen it to 0.50 m for grades K–4.

## 4. The correction rule (why rescaling works)

Model of the real drone: it covers a consistent fraction `k` of what it is commanded, plus noise:

```
actual distance = k × (commanded × scale) × (1 + noise),   noise ~ N(0, 0.03)
```

`k` is unknown (battery sag, prop wear, air density …), but if it is roughly constant, then
one measurement reveals it. That is the whole idea of the correction:

```
new scale = old scale × (target distance ÷ measured distance)
```

**Why it converges:** suppose `k = 0.85`. With `scale = 1.0` the drone flies 85 % of the plan,
so the measured distance from the start is 0.85 × target. The ratio `target ÷ measured = 1/0.85`
is applied to the scale, and the next flight commands `1.176 × plan`, which the drone again flies
at 85 % → back to the plan. Noise (±3 %) makes the landing wobble around the target instead of
hitting it exactly, which is why **several trials** are normal and why the error-vs-trial graph
levels off instead of reaching zero.

For an error *vector* (position, not just distance), the same ratio is applied using the
straight-line distance from start to target versus start to measured landing point.

## 5. Running the simulation

```bash
python code/simulation.py                     # reference scenario, converges in ~2 trials
python code/simulation.py --points 0,0 1,0 1,1 0,1 --tolerance 0.10
python code/simulation.py --trials 20 --seed 7 --csv trials.csv
```

Expected shape of the output (values wobble with the random seed):

```
trial 1: scale=1.000 landed=(0.37,-0.47) error=0.60 m
trial 2: scale=1.096 landed=(0.10,-0.05) error=0.06 m   <- inside 0.25 m tolerance, stop
```

**Students then replace the simulated `fly` with real sensor readings from the drone.**
That swap — same interface, real data — is the moment the project turns from simulation into
measurement ([ROADMAP.md Phase 4](../ROADMAP.md)).

## 6. Where each formula is used

| Formula | Worksheet | Simulation | Sensor code |
|---|---|---|---|
| `d = √(Δx²+Δy²)` | hand calculation | `plan()` | — |
| `θ = atan2(Δy, Δx)` | hand calculation | `plan()` | — |
| `t = d ÷ v` | hand calculation | printed per leg | — |
| line count × 1 m | recorded | (Track A: real log) | `sensor_logger.ino` |
| `position = a × reading + b` | fitted by hand or script | — | shade thresholds |
| `|e| = √(ex²+ey²)` | hand calculation | trial loop | — |
| scale correction | next trial's command | trial loop | — |
