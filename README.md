FOR IGNITRON ECU USERS

Overview
This toolkit provides two scripts:

export.py: Reads the 20×20 VE map block from an .imf file and writes it to a labeled CSV.

convert-back.py: Takes the edited CSV, repacks it into the original 1600-byte block, and splices it back into the .imf.

With these, you can pull your VE table into a spreadsheet, tweak values for tuning, then seamlessly upload the modified map back into Ignitron.

Prerequisites
Python 3.x installed

A stock or previously exported Ignitron .imf file

Installation
Clone or download this repository.

Place your target IMF file in the project folder.

Ensure both export-ve.py and convert-back.py are executable or call them with python3.

Usage
1. Export VE Map to CSV
bash
python3 export-ve.py \
  --input engine_dump.imf \
  --output ve_table.csv
This will:

Read the fixed VE block starting at byte offset 172.

Unpack 400 little-endian 32-bit integers, divide each by 10.

Write a 20×20 CSV with labeled headers for kPa and RPM axes.

2. Edit the CSV
Open ve_table.csv in your favorite spreadsheet or text editor. Make tuning changes under the headers—leave the first two rows intact.

3. Convert Edited CSV Back to IMF
bash
python3 convert-back.py \
  --input edited_ve_table.csv \
  --original engine_dump.imf \
  --output engine_tuned.imf
This will:

Parse your 20×20 map (skipping the header rows).

Flip the table back to Ignitron’s bottom-up order.

Multiply each VE entry by 10, round, and pack as little-endian ints.

Splice the new 1600-byte block into the original .imf at offset 172.

Upload engine_tuned.imf to Ignitron—your ECU will load it without issues.

Script Configuration
Both scripts embed default settings at the top:

START_OFFSET = 172

NUM_CELLS = 400 (20×20)

CELL_SIZE = 4 bytes

Modify these if your firmware layout changes.

Who Is This For
Tuners and hobbyists using Ignitron ECUs

Engineers who prefer spreadsheet-based VE calibration

Anyone needing a reproducible, scriptable workflow for VE map editing