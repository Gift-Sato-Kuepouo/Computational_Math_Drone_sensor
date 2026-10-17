# Hardware guide — platform, sensor, and how they integrate

Read this **before buying or mounting anything**. It answers three questions:

1. Which drone (platform) does this project run on?
2. Which light sensor and board do we attach, exactly?
3. How do we know the drone can actually fly with it?

---

## 1. The platform: WhalesBot Eagle 125F

Verified from the manufacturer's product page ([whalesbot.ai/product/eagle-125f](https://www.whalesbot.ai/product/eagle-125f)):

| Spec | Value |
|---|---|
| Price |  **$71 USD** |
| Age range | **6+** |
| Positioning | "The Soccer Drone Built for Active Classrooms" — recommended kit for the **Drone Cup of ENJOY AI 2026** |
| Flight controller | **ARM Cortex-M0, 80 MHz, 64 KB flash, 8 KB SRAM** |
| Onboard sensors | **Built-in Bluetooth, 6-axis gyroscope, barometric pressure sensor** |
| Motors | 4 coreless motors |
| Safety | Fully enclosed propeller design; indoor use (classrooms, gyms, halls) |
| Setup | Ready to fly out of the box; remote or block-based coding |

Related material worth having:

- **WhalesBot Eagle User Guide (V1.2)** — covers the Eagle family (EG101/EG102): flight control,
  laser sensor, optical flow sensor, gyroscope, barometric pressure sensor, runaway protection,
  propeller covers, Bluetooth remote.
- The bigger **Eagle 1003** in the same family is advertised with **20+ add-on sensors and
  actuators** (light, temperature, ultrasonic, gesture …). Ask your WhalesBot distributor whether
  *your* firmware/app exposes an add-on port or a downward sensor reading. If it does, use the
  native add-on light sensor and skip the custom package in section 3.

### Two checks before you start (do these first)

1. **Expansion check** — Many consumer education drones don't accept add-on sensors. Confirm your
   unit can either (a) carry a small sensor package, or (b) is flown while a ground sensor does
   the measuring (Track B below). The Eagle 125F is a sealed micro drone, so assume Track A
   needs a hover test, not a spec sheet.
2. **Payload check** — WhalesBot does not publish a payload figure for the 125F. Coreless-motor
   micro drones are in the **10-gram class**, so design the package (section 4) to **≤ 10 g total**
   and prove it with the hover test in section 6. If it fails, fly Track B — the lesson is
   unchanged, only the sensor's location changes.

---

## 2. Which light sensor? (concrete parts)

All options are **downward-facing reflectance sensors**: an emitter shines at the floor and a
detector reads how much comes back. Dark tape / black square → less light back → the reading
moves. A reflectance sensor carries its own light, so room lighting matters less than with an LDR.

> **Important physics:** reflectance signal strength falls off fast with distance. The QTR parts
> are designed for a few millimetres; a drone sensing pass happens at 3–10 cm. **Always bench-test
> the sensor at your real flight height** (section 7) before trusting it.

| # | Part (exact name) | Output | Useful at | Weight | Best for | Approx. price |
|---|---|---|---|---|---|---|
| **S1** | **Pololu QTR-1A reflectance sensor, 2-pack (Pololu item #2458)** — *recommended default* | **Analog** (lower voltage = more reflection) | ≤ ~5 cm, and at landing (1–3 cm) | ≈ 0.2 g | Line counting, gradient linear fit, shade classes | ≈ $4 / 2-pack |
| S2 | Pololu QTR-L-1A reflectance sensor | Analog | Longer range when mounted perpendicular to the floor | ≈ 0.2 g | Higher sensing passes than S1 | check [Pololu QTR category](https://www.pololu.com/category/123/pololu-qtr-reflectance-sensors) |
| S3 | Sharp GP2Y0D810Z0F reflective object sensor | Digital (threshold) | **~100 mm** | ≈ 3 g (module) | Line counting at normal drone height (5–10 cm) | ≈ $6–8 |
| S4 | Adafruit VCNL4010 (I²C proximity + ambient light) | Digital | ~20 cm proximity **plus a light channel for shade** | ≈ 1 g (breakout) | Both methods at 10–20 cm height | ≈ $10–13 |
| S5 | TCRT5000 module | Analog + digital | ≤ 12 mm | ≈ 1 g | Cheapest bench practice / desk experiments | ≈ $1–2 |
| S6 | LDR + 10 kΩ resistor (voltage divider) | Analog | Any, but **ambient-light dependent** | ≈ 0.5 g | Teaching voltage dividers indoors with fixed lighting | ≈ $0.20 |

**Pick S1 for the K–5–8 core** (it lands at 1–3 cm, which is exactly where the QTR is happy, and
its analog values power the `position = a × reading + b` exercise). **Add S3 or S4 if your sensing
passes fly higher than ~5 cm.** Details on thresholds and calibration: [verification.md](verification.md).

The Pololu QTR family has an official Arduino library if you prefer it over raw `analogRead()`:
[github.com/pololu/qtr-sensors-arduino](https://github.com/pololu/qtr-sensors-arduino).

---

## 3. Two integration tracks

### Track A — sensor package flies with the drone (full experience)

The package = **sensor + tiny logger board + its own small battery**, strapped under the belly.
It records continuously and prints/downloads a CSV after landing.

```
        ┌─────────────────────────── Eagle 125F belly ───────────────────────────┐
        │   foam tape pad                                                        │
        │      ┌───────────────┐   thin 30 AWG wires, strain-relieved            │
        │      │ XIAO nRF52840 │───────────────┬─────────────┐                   │
        │      │   Sense (4g)  │               │             │                   │
        │      └───────┬───────┘          ┌────▼────┐   ┌────▼─────┐             │
        │              │                  │ QTR-1A  │   │ 1S LiPo  │             │
        │              └── A0 ────────────│ OUT     │   │ 250 mAh  │             │
        │                 GND ────────────│ GND     │   │ (~5 g)   │             │
        │                 3V3 ────────────│ VIN     │   └──────────┘             │
        │                                 └────┬────┘                             │
        └──────────────────────────────────────│──────────────────────────────────┘
                                          faces the floor
                                     (mounted flat, parallel,
                                      at the lowest frame point)
```

**Payload-free variant (Track B):** the drone flies with **nothing attached**. Immediately after
touchdown the student places the sensor package flat on the floor **at the drone's centre mark**
and reads the shade. Distance check for Track B comes from the grid/tape measurement instead of
live line counting. Same math, same data tables, zero payload risk.

### Which track?

| Situation | Track |
|---|---|
| Hover test passes with ≤ 10 g package | **A** (line counts + landing shade, live) |
| Drone sags, won't hold height, or specs unknown | **B** (landing shade only, zero payload) |
| Grades K–4 | **B** — less to crash, teacher handles the drone |
| Grades 5–8 core | **A**, fall back to B if the hover test fails |
| Grades 9–12 | A, plus compare Track A vs B as an uncertainty exercise |

---

## 4. Concrete bill of materials (Track A)

| Qty | Item | Mass | Notes |
|---|---|---|---|
| 1 | WhalesBot Eagle 125F | — | Platform, $71; guards built in |
| 1 | Pololu QTR-1A reflectance sensor (2-pack, #2458) | 0.2 g | One fitted, one spare |
| 1 | Seeed XIAO nRF52840 Sense (headers **not** soldered) | ≈ 4 g | 12-bit ADC, BLE, LiPo charging |
| 1 | LiPo 1S 150–300 mAh with JST connector | 4–6 g | Powers only the logger; charge between trials |
| 1 m | Silicone wire 30 AWG (3 colours) | ≈ 0.3 g | Signal, GND, 3V3 |
| — | Double-sided foam tape + one zip tie | ≈ 0.5 g | Mounting; also secures the battery |
| **Total package** | | **≈ 6–8 g** | **Budget: keep ≤ 10 g** |

**Logger board alternatives** (same sketch, same wiring):

| Board | Mass | Why choose it |
|---|---|---|
| Seeed XIAO nRF52840 Sense | ≈ 4 g | Lightest full option (BLE + charger) |
| ESP32-C3 SuperMini | ≈ 3.5 g | Cheapest (≈ $5); Wi-Fi + BLE |
| Arduino Nano 33 BLE | ≈ 7 g | Classroom-familiar Arduino IDE workflow |
| Arduino Nano Every | ≈ 7 g | 5 V, works with 5 V-only sensors |

**Alternatives for the sensor** are the S2–S6 rows in section 2; wiring is identical
(`OUT → A0`, `GND → GND`, `VIN → 3V3`), except S4 (VCNL4010), which is I²C (`SDA`/`SCL`).

---

## 5. Wiring (Track A, QTR-1A + XIAO)

| QTR-1A pin | XIAO pin |
|---|---|
| VIN | 3V3 |
| GND | GND |
| OUT | **A0** (any ADC pin) |

Notes:

- The QTR-1A output is an **analog voltage: more reflected light → lower voltage → lower ADC
  number.** So white floor = low reading, black tape = high reading.
- Powering the LED from a GPIO instead of 3V3 is possible to save power — not needed here;
  the logger sleeps between flights instead.
- Never hot-plug the LiPo while the drone's own battery is connected.

The matching sketch: [`code/sensor_logger/sensor_logger.ino`](../code/sensor_logger/sensor_logger.ino).

---

## 6. Mounting + hover test protocol

**Mounting**

1. Sensor flat and **parallel to the floor**, at the lowest point of the belly, dead centre
   (off-centre mounting changes the drone's trim and biases every reading).
2. Lens/LED 5–10 mm below the frame so the frame cannot shadow it.
3. Wires taped down within 20 mm of the board (strain relief — loose wires walk into props).
4. Battery on the centreline opposite the board to keep CG neutral.
5. Total package ≤ 10 g; weigh it on a kitchen scale, write the mass on the worksheet.

**Hover test (before every session)**

1. Drone unarmed, props guarded, area clear.
2. Take off to 0.5 m, hover **30 s on the controller only** (no payload corrections).
3. Pass criteria: altitude held without fighting, no unusual motor sound, package does not shift.
4. If it fails → remove the package, fly **Track B**.

---

## 7. Floor, grid and calibration setup

| Element | Build | Why |
|---|---|---|
| **Grid** | 5 × 5 m area, **24 mm black tape** lines at every 1 m on a light floor | Each line = exactly 1 m of travel; the sensor dips per crossing |
| **Start** | Marked origin (0,0) with a taped cross | All student coordinates are relative to it |
| **Target squares** | 3 squares ≈ 0.5 m, filled **black / gray / white** (vinyl, painted board, or printed sheets taped flat) | Landing shade tells the code *which* square |
| **Gradient strip** | 1 m printed grayscale ramp (0 = white → 100 = black) across one square | Continuous reading → `position = a × reading + b` |
| **Lighting** | Constant; note it on the worksheet | IR sensors are less sensitive to room light, but still calibrate in the same light you fly in |

**Calibrate first:** with the sensor at *flight/landing height*, record three readings — white
floor, tape line, and each shade — and set thresholds halfway between them
([verification.md §1](verification.md#1-calibration-table)). This takes 5 minutes and prevents
every "why did it count 47 lines" mystery.

**Height matters:** the reading changes with flying height, so keep the drone low and steady
near the floor when sensing, and never calibrate on the bench at 1 cm if you sense at 10 cm.

**Honest limits:** the line-count method checks distance, not sideways drift, so use the landing
shade or a second marker to check direction.

---

## 8. Bench test before first flight (10 minutes)

1. Tape a line on the floor; hold the drone (battery **off**) so the sensor is at the exact
   sensing height; sweep it across the line while watching the serial monitor.
2. Record `ADC_white`, `ADC_tape`, `ADC_black_shade` at that height.
3. Accept the sensor if `ADC_tape − ADC_white ≥ 100` counts (on a 10-bit/12-bit ADC scaled to
   0–1023). If not: fly lower for sensing passes, or switch to S2/S3/S4 from section 2.
4. Write the numbers into the worksheet's calibration table — they become the thresholds in the
   sketch.

## Safety

- Propeller guards on at all times (the 125F's frame is already enclosed).
- Sensor/battery changes only with the drone battery removed.
- Fly only inside the marked area; keep faces, hair and loose sleeves out of the flight volume.
- One pilot, one spotter, everyone else behind the line.
