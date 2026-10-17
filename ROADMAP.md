# Roadmap — K–12 initiative, phases and room for development

This project is intentionally staged so a classroom can start with **paper, a floor grid and a
laptop**, and grow into full hardware-in-the-loop measurement. Each phase has an exit criterion:
nothing blocks the next phase until the criterion is met.

## Phase status

| Phase | Goal | Exit criterion | Status |
|---|---|---|---|
| **0. Foundation** | Docs, math model, simulation, worksheet templates | Simulation reproduces the reference run (trial 1 ≈ 0.60 m error, trial 2 ≈ 0.06 m) | **done in this repo** |
| **1. Bench lab** | Calibrate the sensor; prove the package flies | Calibration table filled; ADC swing ≥ 100 counts at sensing height; 30 s hover test passed with package mounted | awaiting hardware |
| **2. First flights** | Track A/B flights, line counting + landing shade | One team reaches `|e| ≤ 0.25 m` in ≤ 5 trials with a logged CSV | |
| **3. Linear model** | Gradient strip fit by hand and by script | `R² ≥ 0.95`, landing position from `position = a × reading + b` | |
| **4. Hardware in the loop** | Replace the simulated `fly()` with real logged landings | Same trial loop runs on CSVs from real flights | |
| **5. Second measurement** | Check sideways drift directly (mid-course marker, second sensor, or app telemetry) | Error decomposed into along-track and cross-track components | |
| **6. Publish** | Share a class dataset + worksheet answers guide | Dataset in `data/`, tagged release v1.0 | |

## Extension ideas (by grade band)

- **K–4:** colour-only version — one shade per square, counting instead of calculating.
- **5–8:** multiple teams' data pooled → class-wide convergence curve; median vs mean scale.
- **9–12:** estimate `k` and its drift with battery voltage; uncertainty propagation; compare
  Track A (onboard) vs Track B (ground) measurements of the same flight as a gauge-R&R style study.
- **Robotics club:** closed-loop correction *within* a flight (read lines live, adjust heading);
  AprilTag ground truth; swarm of two Eagle drones sharing the grid.
- **Outdoor variant:** replace tape lines with painted markings and add a GPS/RTK module —
  same math, metre-scale tolerance becomes a discussion about accuracy vs precision.

## Good first contributions

1. Translating the worksheet into another language (framing stays, tables stay).
2. A `--plot` flag for `simulation.py` that draws the path and error curve when matplotlib
   is available (must stay optional — school machines only have the standard library).
3. Recording a real calibration table from your own QTR-1A and adding it as sample data
   (anonymised, in `data/`).
4. ABlockly/makecode stub that issues the same leg commands for schools coding the Eagle 125F
   in the WhalesBot app instead of Python.
5. Improving the sensor sketch: on-board line-crossing timestamps (event CSV) instead of the
   20 ms stream, for slower serial links.

## Design constraints we do not want to break

- **Standard library only** for the student-facing Python (Chromebook-friendly).
- **Any single-ADC board** must be able to run the sensor sketch.
- Every doc must stay usable **without hardware** (Phase 0 must always work).
- Safety rules and the payload/hover-test check stay in the front matter of the hardware docs.

## Open questions (help wanted)

- WhalesBot does not publish a payload figure for the Eagle 125F — crowdsource hover-test
  results with package mass (issue template welcome).
- Does your Eagle firmware/app expose any downward sensor or add-on port? Findings update
  [docs/hardware.md §1](docs/hardware.md).
- Best debounce window vs flight speed — collect real crossing timestamps to settle it.
