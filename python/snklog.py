#!/usr/bin/env python3
import os
import time
import glob
from pathlib import Path
import argparse
import sys

LOG_DIR = ".snakemake/slurm_logs/"


def get_sorted_files(directory):
    files = glob.glob(os.path.join(directory, "*"))
    return sorted(files, key=os.path.getmtime, reverse=True)


def list_logs(args):
    files = get_sorted_files(LOG_DIR)
    for i, file in enumerate(files[: args.max_print]):
        mtime = os.path.getmtime(file)
        print(f"{time.ctime(mtime)} - {file}")
        if i >= args.max_print - 1:
            break


def tail_file(file, follow=False):
    with open(file, "r") as f:
        if follow:
            f.seek(0, 2)  # Go to the end of the file
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)  # Sleep briefly
                    continue
                yield line
        else:
            f.seek(0, 2)
            file_size = f.tell()
            f.seek(max(file_size - 1024, 0), 0)
            lines = f.readlines()
            for line in lines[-10:]:
                yield line.strip()


def tail_log(args):
    files = get_sorted_files(LOG_DIR)
    if not files:
        print(f"No log files found in {LOG_DIR}")
        return

    most_recent_log = files[0]
    print(f"Tailing the most recent log file: {most_recent_log}")

    for line in tail_file(most_recent_log, follow=args.follow):
        print(line, end="")


def main():
    parser = argparse.ArgumentParser(description="Manage Snakemake Slurm log files")
    subparsers = parser.add_subparsers(dest="command")

    list_parser = subparsers.add_parser("list", help="List recent log files")
    list_parser.add_argument(
        "--max-print", type=int, default=10, help="Maximum number of files to list"
    )

    tail_parser = subparsers.add_parser("tail", help="Tail the most recent log file")
    tail_parser.add_argument(
        "-f", "--follow", action="store_true", help="Follow the file as it grows"
    )

    args = parser.parse_args()

    if args.command == "list":
        list_logs(args)
    elif args.command == "tail":
        tail_log(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
