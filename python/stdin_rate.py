#!/usr/bin/env python3
import sys
import time
import argparse
from collections import deque
import math


def estimate_rate(window_size=10, update_interval=1.0, increment_size=1):
    counts = deque(maxlen=window_size)
    last_update = time.time()
    total_count = 0
    start_time = time.time()

    sum_rates = 0
    sum_squares = 0
    n_updates = 0

    while True:
        line = sys.stdin.readline()
        if not line:
            break

        total_count += 1
        current_time = time.time()
        counts.append(current_time)

        if current_time - last_update >= update_interval:
            if len(counts) > 1:
                time_diff = counts[-1] - counts[0]
                rate = (
                    ((len(counts) - 1) * increment_size) / time_diff
                    if time_diff > 0
                    else 0
                )
            else:
                rate = 0

            n_updates += 1
            sum_rates += rate
            sum_squares += rate**2

            mean_rate = sum_rates / n_updates

            if n_updates > 1:
                variance = (sum_squares - (sum_rates**2) / n_updates) / (n_updates - 1)
                std_dev = math.sqrt(variance)
            else:
                std_dev = 0

            total_units = total_count * increment_size

            sys.stderr.write(
                f"\rTotal: {total_units:.0f} | "
                f"Current: {rate:.2f} | "
                f"μ: {mean_rate:.2f} | "
                f"σ: {std_dev:.2f} u/s"
            )
            sys.stderr.flush()

            last_update = current_time

    sys.stderr.write("\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estimate rate of units from stdin.")
    parser.add_argument(
        "-w",
        "--window",
        type=int,
        default=10,
        help="Window size for rate calculation (default: 10)",
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=float,
        default=1.0,
        help="Update interval in seconds (default: 1.0)",
    )
    parser.add_argument(
        "-s",
        "--size",
        type=float,
        default=1.0,
        help="Increment size per line (default: 1.0)",
    )
    args = parser.parse_args()

    estimate_rate(args.window, args.interval, args.size)
