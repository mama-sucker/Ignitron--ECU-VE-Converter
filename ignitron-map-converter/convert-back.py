# Edited the .csv and want to convert back to .imf 
# use this

import csv
import struct

# ┌── CONFIG ───────────────────────────────────────────────────────────────
INPUT_CSV    = "ve_table.csv"
ORIGINAL_IMF = "VE-Before.imf"
OUTPUT_IMF   = "VE-new-Edited.imf"

# VE block starts at byte offset 172; each entry is 4 bytes, 400 entries total
START = 172
END   = START + 400 * 4  # 172 + 1600 = 1772
# └──────────────────────────────────────────────────────────────────────────

# 1) Load original .imf into a mutable bytearray
with open(ORIGINAL_IMF, "rb") as f:
    orig_data = bytearray(f.read())

# 2) Read the edited CSV, skip its two header rows, and flip vertically
ve_values = []
with open(INPUT_CSV, newline="") as f:
    rows = list(csv.reader(f))
data_rows = rows[2:][::-1]  # drop title + axis header, reverse order

# 3) Parse VE floats, scale ×10, round to int
for row in data_rows:
    for cell in row[1:]:    # skip the leading kPa label
        try:
            ve_values.append(int(round(float(cell) * 10)))
        except ValueError:
            raise ValueError(f"Invalid VE entry in CSV: {cell}")

if len(ve_values) != 400:
    raise RuntimeError(f"Expected 400 VE values, got {len(ve_values)}")

# 4) Build a new 1600-byte VE block
new_block = bytearray()
for ve in ve_values:
    new_block += struct.pack("<I", ve)

# 5) Splice into the original data
if END > len(orig_data):
    raise RuntimeError(f"IMF file too small: can't write up to byte {END}")

out_data = orig_data[:START] + new_block + orig_data[END:]

# 6) Write the patched .imf
with open(OUTPUT_IMF, "wb") as f:
    f.write(out_data)

print(f"Written {OUTPUT_IMF} (VE block {START}–{END} replaced)")
