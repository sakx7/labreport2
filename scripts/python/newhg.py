import pandas as pd

# Constants for pressure calculation
DENSITY = 13600  # kg/m^3 (mercury density)
GRAVITY = 9.81    # m/s^2
CONVERSION_FACTOR = 2 * DENSITY * GRAVITY * 1e-5  # 2*ρ*g*cm→m*Pa→kPa

def calculate_pressure(h_cm):
    """Convert height difference (cm Hg) to pressure (kPa) while preserving sign"""
    return h_cm * CONVERSION_FACTOR  # Remove abs() to keep signs

# Read the CSV file
file_path = "data/diff_units/Hg_Glass_cmHg.csv"
df = pd.read_csv(file_path)

# Calculate pressures while preserving signs
df['Positive'] = df['Positive'].apply(calculate_pressure)
df['Negative'] = df['Negative'].apply(calculate_pressure)

# Overwrite the original file with new values
df.to_csv(file_path, index=False, float_format='%.3f')

print(f"File '{file_path}' updated with signed pressures (kPa)")
print("First 3 rows:")
print(df.head(3))