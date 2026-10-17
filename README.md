# Computational Math & Drone Sensor a K–12 initiative

An independent project for K–12 initiative (core: grades 5–8) to implement a real-life
mathematical simulation with the Eagle 125F drone and a little light sensor attached to it.
The student will do their mathematical calculation manually, then integrate the result in the
drone and leave the drone to follow the path the student have chosen for the drone to operate.

Students predict with mathematics, fly, then **check the prediction with sensor data instead of
eyeballing it**, and iterate until the drone lands inside the tolerance.

---

## The four steps (every team, every grade band)

1. **Start point and three targets** — each team gets coordinates on the 5×5 grid.
2. **Calculate and code** — students find the distances and headings by hand, then write the
   flight commands (`d = √(Δx² + Δy²)`, `θ = atan2(Δy, Δx)`, `t = d ÷ v`).
3. **Fly and verify** — the drone logs line crossings and the landing shade, and students
   record the measured landing point and compute the error `|e| = √(ex² + ey²)`.
4. **Adjust and repeat** — apply `new scale = old scale × (target distance ÷ measured distance)`
   and fly again until `|e| ≤ 0.25 m`, then graph error against trial number.

The math behind every step is in [docs/math-model.md](docs/math-model.md).
The lesson flow, grade-band adaptations and assessment are in [docs/lesson-plan.md](docs/lesson-plan.md).

## Two ways students verify the flight

| Method | What it checks | How |
|---|---|---|
| **A. Count the grid lines** | distance travelled | Dark tape lines on a light floor; the downward sensor dips at each crossing; measured distance = lines crossed × 1 m (threshold + short debounce so one line is not counted twice). |
| **B. Read the landing square** | final position | Three target squares in black / gray / white; at landing the sensor reports the shade. For a finer measure, a printed gradient strip gives `position = a × reading + b` — a real linear-model exercise. |

Method A checks distance only, not sideways drift — so teams always finish with method B.
Full procedures, calibration tables and honest limits: [docs/verification.md](docs/verification.md).

## Hardware at a glance

Concrete, verified part choices are in **[docs/hardware.md](docs/hardware.md)** — read it before
buying anything.

| Role | Chosen part | Why |
|---|---|---|
| **Platform** | **WhalesBot Eagle 125F** (≈ $71, age 6+) | Indoor soccer drone with fully enclosed props, ARM Cortex-M0 80 MHz / 64 KB flash, Bluetooth, 6-axis gyro and barometer; recommended kit for the ENJOY AI 2026 "Drone Cup". |
| **Light sensor** | **Pololu QTR-1A reflectance sensor (2-pack, item #2458)** | Own IR emitter + phototransistor, so room lighting matters less; tiny (12.7 × 7.6 mm, ≈ 0.2 g), analog output for the linear-fit exercise. |
| **Onboard logger** | **Seeed XIAO nRF52840 Sense** (≈ 4 g bare) | 12-bit ADC, Bluetooth LE, LiPo charger, thumb-sized — the whole sensor package stays near 10 g. |
| **Payload-free track** | Same sensor + board, kept on the ground | If the drone cannot lift the package, the sensor reads the landing square *after* touchdown. Zero payload, same data. |

> limit with the hover test in [docs/hardware.md](docs/hardware.md) before every flight session.

## Repository layout

```
├── README.md                    ← you are here
├── ROADMAP.md                   ← K–12 initiative phases & room for development
├── docs/
│   ├── hardware.md              ← platform + sensor BOM, wiring, mounting, floor setup
│   ├── math-model.md            ← formulas, worked example, why the correction works
│   ├── lesson-plan.md           ← 4-step flow, grade bands K–4 / 5–8 / 9–12, safety
│   └── verification.md          ← line counting, landing shade, gradient calibration
├── code/
│   ├── simulation.py            ← run the model before flying (stdlib only)
│   ├── calibrate_gradient.py    ← fit position = a × reading + b
│   └── sensor_logger/
│       ├── sensor_logger.ino    ← Arduino sketch: line counter + shade classifier (CSV)
│       └── README.md            ← wiring, serial commands, log format
└── worksheet/
    ├── student_worksheet.md     ← handout: calculations, data tables, error graph
    └── *_template.csv           ← trial log & calibration templates
```

## Quick start (no hardware needed)

```bash
python code/simulation.py            # the reference scenario: converges in ~2 trials
python code/simulation.py --help     # fly your own team's points
```

Then calibrate a gradient strip with real readings:

```bash
python code/calibrate_gradient.py --demo                 # synthetic strip, see the fit
python code/calibrate_gradient.py my_calibrations.csv    # your own (reading,position) table
```

Both scripts use only the Python standard library, so they run on school laptops and
Chromebook Linux containers unchanged.

## Safety

Keep propeller guards on (the Eagle 125F is fully enclosed), fly only in the marked area,
keep faces and hands out of the flight volume, and mount/unmount the sensor with the battery
removed. Full rules in [docs/lesson-plan.md](docs/lesson-plan.md#safety-rules).

## Status & development

This repository starts as documentation + simulation (Phase 0 of
[ROADMAP.md](ROADMAP.md)); bench calibration, first flights, hardware-in-the-loop data and
contributions from classrooms are the next phases. Ideas for good first contributions are
listed at the bottom of the roadmap.

## License

[MIT](LICENSE)
