# For users of ignitron ecu 
# if you want to convert your ignitron VE map file (.imf) into (.csv)

import struct
import numpy as np
import csv

INPUT_FILE = "VE-Before.imf"
OUTPUT_FILE = "ve_table.csv"

# === READ FILE ===
with open(INPUT_FILE, "rb") as f:
    data = f.read()

# === SCAN FOR VE-LIKE BLOCK ===
ve_values = []
start_offset = None

for i in range(0, len(data) - 3, 4):
    val = struct.unpack("<I", data[i:i+4])[0]
    if 800 <= val <= 1300:  # VE range: 80.0 to 130.0
        ve_values.append(val / 10.0)
        if len(ve_values) == 400:
            start_offset = i - (399 * 4)
            break
    else:
        ve_values = []  # Reset if value is out of range

if start_offset is None:
    raise ValueError("Could not locate VE block by value clustering.")

# … after you’ve found start_offset …
#print(f"VE block starts at byte offset: {start_offset}")

# === SHAPE MATRIX ===
ve_matrix = np.array(ve_values).reshape((20, 20))[::-1]

# === HARD-CODED AXES ===
rpm_axis = [500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 3000,
            3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000]

kpa_axis = [300.0, 280.0, 260.0, 240.0, 220.0, 200.0, 180.0, 160.0, 140.0, 120.0,
            100.0, 90.0, 80.0, 70.0, 60.0, 50.0, 40.0, 30.0, 20.0, 15.0]

# === WRITE TO CSV ===
with open(OUTPUT_FILE, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Volumetric Efficiency Map"])
    writer.writerow(["kPa (load) \\ RPM"] + [f"{rpm} RPM" for rpm in rpm_axis])
    for kpa, row in zip(kpa_axis, ve_matrix):
        formatted_row = [f"{v:.1f}" for v in row]
        writer.writerow([f"{kpa:.1f} kPa"] + formatted_row)
