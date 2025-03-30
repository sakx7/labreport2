import pandas as pd
import os
import re

# Define paths
input_dir = "data/diff_units_zerod"
output_dir = "data/same_units"

# Updated conversion factors to bar (now Hg Glass is in kPa)
conversion_factors = {
    "Bourden_Gauge_2_knm2.csv": 0.01,       # 1 kN/m² = 0.01 bar
    "Bourden_Gauge_psi.csv": 0.0689476,      # 1 psi = 0.0689476 bar
    "Bundenburg_Gauge_bar.csv": 1.0,         # Already in bar
    "Hg_Glass_cmHg.csv": 0.01,               # Now 1 kPa = 0.01 bar (since already converted to kPa)
    "Pressure_Calibrator_kPa.csv": 0.01,      # 1 kPa = 0.01 bar
}

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def rename_to_bar(filename):
    """Replace the last unit in filename with '_bar.csv'"""
    return re.sub(r'_([^_]+)\.csv$', '_bar.csv', filename)

# Process each file
for filename, factor in conversion_factors.items():
    input_path = os.path.join(input_dir, filename)
    output_filename = rename_to_bar(filename)
    output_path = os.path.join(output_dir, output_filename)

    if os.path.exists(input_path):
        df = pd.read_csv(input_path)
        
        # Convert only numerical values in these columns
        if {"Positive", "Negative"}.issubset(df.columns):
            df[["Positive", "Negative"]] *= factor
        
        df.to_csv(output_path, index=False)
        print(f"Converted {filename} -> {output_filename}")
    else:
        print(f"Warning: {input_path} not found")

print("All conversions completed.")