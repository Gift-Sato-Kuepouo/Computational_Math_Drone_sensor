import argparse
import csv
import math
import random


def read_pairs(path):
    readings = []
    positions = []
    with open(path, newline="") as handle:
        for row in csv.reader(handle):
            if len(row) < 2:
                continue
            try:
                reading = float(row[0])
                position = float(row[1])
            except ValueError:
                continue
            readings.append(reading)
            positions.append(position)
    if len(readings) < 2:
        raise SystemExit("need at least two (reading, position) pairs in %s" % path)
    return readings, positions


def demo_pairs():
    random.seed(11)
    positions = [i / 10.0 for i in range(11)]
    readings = [900.0 - 700.0 * p + random.gauss(0, 8) for p in positions]
    return readings, positions


def fit(readings, positions):
    n = len(readings)
    mean_r = sum(readings) / n
    mean_p = sum(positions) / n
    numerator = sum((r - mean_r) * (p - mean_p) for r, p in zip(readings, positions))
    denominator = sum((r - mean_r) ** 2 for r in readings)
    if denominator == 0:
        raise SystemExit("all readings are identical; recalibrate the sensor")
    a = numerator / denominator
    b = mean_p - a * mean_r
    residual = sum((p - (a * r + b)) ** 2 for r, p in zip(readings, positions))
    total = sum((p - mean_p) ** 2 for p in positions)
    r_squared = 1.0 - residual / total if total else 1.0
    return a, b, r_squared


def main():
    parser = argparse.ArgumentParser(
        description="Fit position = a * reading + b from a gradient-strip calibration CSV."
    )
    parser.add_argument("csv_path", nargs="?", help="CSV with columns reading,position")
    parser.add_argument("--demo", action="store_true", help="run on synthetic calibration data")
    parser.add_argument(
        "--predict",
        type=float,
        action="append",
        default=[],
        help="landing reading to convert to a position (repeatable)",
    )
    args = parser.parse_args()

    if args.demo:
        readings, positions = demo_pairs()
    elif args.csv_path:
        readings, positions = read_pairs(args.csv_path)
    else:
        parser.error("give a CSV path or use --demo")

    a, b, r_squared = fit(readings, positions)
    print("calibration pairs: %d" % len(readings))
    print("fit: position = %.5f * reading %+.4f     R^2 = %.3f" % (a, b, r_squared))
    if r_squared < 0.95:
        print("warning: R^2 below 0.95, the strip or readings may not be linear")

    checks = args.predict if args.predict else [readings[0], readings[len(readings) // 2], readings[-1]]
    for reading in checks:
        print("reading %.0f -> position %.3f m" % (reading, a * reading + b))


if __name__ == "__main__":
    main()
