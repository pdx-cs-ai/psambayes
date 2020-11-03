#!/usr/bin/python3

import csv, sys

counts = None
with open(sys.argv[1], "r") as f:
    reader = csv.reader(f)
    for row in reader:
        if counts is None:
            counts = [0] * len(row)
        counts[0] += 1
        for i in range(1, len(counts)):
            counts[i] += int(row[i])

print(f"n: {counts[0]}")
print(f"c: {counts[1]}")
for i in range(2, len(counts)):
    print(f"f[{i-2}]: {counts[i]}")
