import argparse
import csv
import math
import random


def plan(points):
    legs = []
    for (x0, y0), (x1, y1) in zip(points, points[1:]):
        dx, dy = x1 - x0, y1 - y0
        legs.append((math.hypot(dx, dy), math.degrees(math.atan2(dy, dx))))
    return legs


def fly(legs, scale, k=0.85, noise=0.03):
    x = y = 0.0
    for distance, heading in legs:
        actual = k * (distance * scale) * (1 + random.gauss(0, noise))
        x += actual * math.cos(math.radians(heading))
        y += actual * math.sin(math.radians(heading))
    return x, y


def parse_points(values):
    points = []
    for value in values:
        parts = value.split(",")
        if len(parts) != 2:
            raise argparse.ArgumentTypeError(
                "points must be pairs like 0,0 (got %r)" % value
            )
        points.append((float(parts[0]), float(parts[1])))
    if len(points) < 2:
        raise argparse.ArgumentTypeError("need at least a start point and one target")
    return points


def print_leg_table(points, legs, speed):
    origin = points[0]
    previous_heading = 0.0
    total_distance = 0.0
    print("leg table (start at %.2f, %.2f):" % origin)
    print("  leg  from            to              d(m)   heading(deg)  turn(deg)  t(s)")
    for index, ((distance, heading), start, end) in enumerate(
        zip(legs, points, points[1:]), start=1
    ):
        turn = heading - previous_heading
        while turn > 180:
            turn -= 360
        while turn < -180:
            turn += 360
        total_distance += distance
        print(
            "  %-4d (%.2f, %.2f)  ->  (%.2f, %.2f)  %.2f  %8.2f     %+8.2f  %6.2f"
            % (index, start[0], start[1], end[0], end[1], distance, heading, turn, distance / speed)
        )
        previous_heading = heading
    print(
        "  total distance %.2f m, predicted time %.2f s at v = %.2f m/s"
        % (total_distance, total_distance / speed, speed)
    )


def run_trials(target, legs, tolerance, k, noise, trials, seed, csv_path, speed):
    if seed is not None:
        random.seed(seed)
    scale = 1.0
    rows = []
    passed = False
    for trial in range(1, trials + 1):
        x, y = fly(legs, scale, k, noise)
        error = math.hypot(x - target[0], y - target[1])
        passed = error <= tolerance
        print(
            "trial %d: scale=%.3f landed=(%.2f,%.2f) error=%.2f m%s"
            % (trial, scale, x, y, error, "   <- inside tolerance" if passed else "")
        )
        rows.append((trial, round(scale, 4), round(x, 3), round(y, 3), round(error, 3), int(passed)))
        if passed:
            break
        planned_distance = math.hypot(*target)
        measured_distance = math.hypot(x, y)
        if measured_distance < 1e-9:
            print("measured distance is zero; cannot correct scale")
            break
        scale *= planned_distance / measured_distance
    if not passed:
        print("did not reach the %.2f m tolerance in %d trials" % (tolerance, trials))
    if csv_path:
        with open(csv_path, "w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["trial", "scale", "landed_x", "landed_y", "error_m", "passed"])
            writer.writerows(rows)
        print("wrote %s (%d rows)" % (csv_path, len(rows)))
    return passed


def main():
    parser = argparse.ArgumentParser(
        description="Simulate the student drone flight, then correct the scale factor."
    )
    parser.add_argument(
        "--points",
        nargs="+",
        default=["0,0", "2,1", "3,3", "1,4"],
        help="start then targets as x,y pairs (default: 0,0 2,1 3,3 1,4)",
    )
    parser.add_argument("--tolerance", type=float, default=0.25, help="pass rule |e| <= tolerance in metres")
    parser.add_argument("--k", type=float, default=0.85, help="fraction of the command the drone actually flies")
    parser.add_argument("--noise", type=float, default=0.03, help="relative noise sigma per leg")
    parser.add_argument("--trials", type=int, default=10, help="maximum number of trials")
    parser.add_argument("--seed", type=int, default=None, help="random seed for a repeatable run")
    parser.add_argument("--speed", type=float, default=0.5, help="measured drone speed in m/s, used for predicted times")
    parser.add_argument("--csv", default=None, help="write the trial table to this CSV file")
    parser.add_argument("--no-table", action="store_true", help="skip printing the leg table")
    args = parser.parse_args()

    try:
        raw_points = parse_points(args.points)
    except argparse.ArgumentTypeError as error:
        parser.error(str(error))
    origin = raw_points[0]
    points = [(x - origin[0], y - origin[1]) for x, y in raw_points]
    target = points[-1]
    legs = plan(points)

    if not args.no_table:
        print_leg_table(raw_points, legs, args.speed)
        print("")
    print("target (%.2f, %.2f), tolerance %.2f m, k = %.2f, noise = %.2f"
          % (target[0], target[1], args.tolerance, args.k, args.noise))
    run_trials(target, legs, args.tolerance, args.k, args.noise, args.trials, args.seed, args.csv, args.speed)


if __name__ == "__main__":
    main()
