# Lesson plan — the K–12 initiative

A 4-step, hands-on module where students predict a drone's path with mathematics, fly it, and
verify the prediction with light-sensor data. **Core target: grades 5–8** (the original K–5–8
initiative), with built-in adaptations down to K–4 and up to 9–12.

---

## The four steps (every grade band)

| Step | Students do | Artifact |
|---|---|---|
| **1. Start point and three targets** | Each team draws coordinates on the 5×5 grid | Marked grid on the floor, team points |
| **2. Calculate and code** | Hand-calculate distances, headings, times; write the flight commands | Worksheet: leg table ([math-model.md](math-model.md)) |
| **3. Fly and verify** | Drone logs line crossings + landing shade; students record the measured landing point and compute the error | Trial log (CSV + worksheet table) |
| **4. Adjust and repeat** | Apply `new scale = old scale × (target ÷ measured)`; fly again until `|e| ≤ tolerance` | Error-vs-trial graph |

---

## Suggested schedule (5 × 60 min)

| Session | Content | Prep |
|---|---|---|
| 1 | Grid on the floor; introduce the 4 steps; teams get points; start calculations | Tape the 5×5 grid |
| 2 | Finish calculations; measure drone speed `v`; **calibrate the sensor** (white floor, tape, shades) and bench-test at flight height | Sensor + board on USB; gradient strip printed |
| 3 | Simulation first ([`code/simulation.py`](../code/simulation.py)), then Track A/B flights; trial 1 + trial 2 with correction | Hover test, battery charged |
| 4 | Trials 3+ until inside tolerance; gradient fit `position = a × reading + b` | Calibration CSV |
| 5 | Graph error vs trial, present results, honest-limits discussion | Poster/graph paper or spreadsheet |

---

## Grade-band adaptations

### K–4 (primary — "count, predict, check")
- Grid squares are counted, not calculated: `d = how many squares along`.
- Teacher (or older buddy) flies; students are the **measurement team**: they call the line
  crossings out loud and place a marker where they think the drone landed.
- Verification: **Track B only** — the sensor reads the landing shade after touchdown; "Did it
  land on black, gray, or white?" is the pass/fail question.
- Big-language math: more/less, halfway, nearest, compare prediction vs measurement with cubes.
- Output: one worksheet row per team + a class bar chart of "squares off".

### 5–8 (core — the original initiative)
- Full hand calculations: `d = √(Δx² + Δy²)`, `θ = atan2(Δy, Δx)`, `t = d ÷ v`, turn angles.
- **Track A** flights: line counting for distance, landing shade (or gradient fit) for position.
- Error vector and tolerance `0.25 m`; the correction rule applied between trials.
- Gradient strip becomes a genuine linear-model exercise: fit `position = a × reading + b`,
  discuss slope, intercept, and how straight the line really is (`R²` via
  [`code/calibrate_gradient.py`](../code/calibrate_gradient.py)).
- Output: trial table + error-vs-trial graph + a one-paragraph conclusion.

### 9–12 (extension — physics, stats, engineering)
- Treat `k` as a measured system parameter: estimate `k` from data, report mean ± SD over trials.
- Uncertainty: propagate sensor noise (±3 %) into predicted landing error; compare Track A vs
  Track B measurements of the same flight.
- Statistics: linear regression by hand (least-squares formulas) before using the script;
  residual plot of the gradient calibration.
- Engineering: timing model `t = d ÷ v` vs video-measured leg times; discuss acceleration,
  ground effect and why `k` drifts as the battery drains.
- Coding: students modify `simulation.py` (add wind, per-leg noise, a heading error) and justify
  each change.

---

## What each team hands in

1. Completed [student_worksheet.md](../worksheet/student_worksheet.md) — leg table, calibration
   values, trial table.
2. Trial data file (`worksheet/trials_template.csv` filled in, or the simulator's `--csv` output).
3. Error-vs-trial graph (hand-drawn or plotted).
4. Conclusion: how many trials to pass, the final scale factor, and one honest limitation
   (e.g., "line counts distance but not sideways drift").

## Assessment rubric (quick)

| Criterion | Emerging | Proficient | Advanced |
|---|---|---|---|
| Calculations | ≥1 error in legs | All distances/headings correct | Includes turn angles + predicted times, correct rounding |
| Verification | Readings recorded incompletely | Calibration values + measured landing point recorded | Uses gradient fit with `a`, `b` and checks `R²` |
| Correction | Scale updated incorrectly | Rule applied correctly each trial | Explains *why* the rule works; notes when it stalls |
| Communication | Table only | Graph + 1-paragraph conclusion | Discusses limits (drift, height dependence, noise) |

## Standards alignment (examples)

- **CCSS 5.G.A.1** — graph points on the coordinate plane (the grid IS the coordinate plane).
- **CCSS 8.G.B.7** — Pythagorean theorem to find unknown sides (`d = √(Δx²+Δy²)`).
- **CCSS 8.EE.B.5 / 8.F.A.3** — interpreting `t = d ÷ v` and `position = a·reading + b` as linear functions.
- **CCSS HSS.ID.C.6 / C.7** (9–12) — fitting a function to data; interpreting slope/intercept in context.
- **NGSS ETS1** — define problems, evaluate solutions with data.

## Safety rules

1. **Propeller guards on** every flight (the Eagle 125F is fully enclosed — keep it that way).
2. Fly **only inside the marked area**; spectators behind the line.
3. **Faces, hands and hair out of the flight volume** — no one leans over the grid.
4. Sensor, battery and mounting changes **only with the drone battery removed**.
5. One designated pilot, one spotter per drone; everyone else holds position.
6. Land to change batteries — never catch a flying drone.
7. Stop the session if a guard is cracked, a motor sounds rough, or the package shifts.

## Roles in each team (rotate per session)

| Role | Job |
|---|---|
| Pilot | Executes the code/commands, calls "landing" |
| Calculator | Hand calculations, correction factor |
| Sensor operator | Calibration, downloads the CSV, reads the shade |
| Recorder | Worksheet tables, graph |
| Safety spotter | Checks guards, area, and the stop rules |
