import pandas as pd
import os
import numpy as np

# Define paths and constants
input_dir = "data/diff_units_zerod"
ATM_PRESSURE_BAR = 1.01325

# Updated conversion factors (1 SOURCE UNIT = X TARGET UNIT)
# Note: Hg_Glass now uses kPa conversion factors since data is already in kPa
conversion_factors = {
    "Bourden_Gauge_2_knm2.csv": {"psi": 0.145038, "bar": 0.01, "cmHg": 0.750062, "kPa": 1.0, "bar_abs": 0.01},
    "Bourden_Gauge_psi.csv": {"bar": 0.0689476, "kPa": 6.89476, "cmHg": 5.17149, "bar_abs": 0.0689476},
    "Bundenburg_Gauge_bar.csv": {"psi": 14.5038, "kPa": 100, "cmHg": 75.0062, "bar_abs": 1.0},
    "Hg_Glass_cmHg.csv": {"bar": 0.01, "psi": 0.145038, "cmHg": 0.750062, "bar_abs": 0.01},  # Changed to kPa factors
    "Pressure_Calibrator_kPa.csv": {"bar": 0.01, "psi": 0.145038, "cmHg": 0.750062, "bar_abs": 0.01}
}

def clean_filename(filename):
    return '_'.join(filename.split('_')[:-1])

# Initialize data structures
units = ["bar", "psi", "kPa", "cmHg", "bar_abs"]
results = {unit: {"data": {}, "gradients": {}} for unit in units}

# Process files
for filename, factors in conversion_factors.items():
    input_path = os.path.join(input_dir, filename)
    if not os.path.exists(input_path):
        print(f"Warning: {input_path} not found.")
        continue
        
    df = pd.read_csv(input_path)
    base_unit = filename.split('_')[-1].replace('.csv', '')
    if base_unit == "knm2":
        base_unit = "kPa"
    elif base_unit == "cmHg":  # Update base unit for Hg Glass
        base_unit = "kPa"
    
    # Store original data
    if base_unit in results:
        results[base_unit]["data"][filename] = df[["Positive", "Negative"]]
    
    # Convert and store in all units
    for unit, factor in factors.items():
        converted = df.copy()
        if unit == "bar_abs":
            converted[["Positive", "Negative"]] = converted[["Positive", "Negative"]] * factor + ATM_PRESSURE_BAR
        else:
            converted[["Positive", "Negative"]] = converted[["Positive", "Negative"]] * factor
        results[unit]["data"][filename] = converted

# Calculate gradients using np.polyfit() - MODIFIED SECTION
for unit in units:
    # Find calibrator data
    calibrator_df = None
    for filename, df in results[unit]["data"].items():
        if "Pressure_Calibrator" in filename:
            calibrator_df = df
            break
    
    if calibrator_df is None:
        continue
    
    # Compare each instrument to calibrator
    for filename, instrument_df in results[unit]["data"].items():
        if "Pressure_Calibrator" in filename:
            continue
            
        instrument_name = clean_filename(filename)
        
        # Calculate gradients and intercepts using polyfit
        x_pos, y_pos = instrument_df["Positive"], calibrator_df["Positive"]
        x_neg, y_neg = instrument_df["Negative"], calibrator_df["Negative"]
        x_combined = np.concatenate([x_pos, x_neg])
        y_combined = np.concatenate([y_pos, y_neg])
        
        (slope_pos, intercept_pos), _ = np.polyfit(x_pos, y_pos, 1, full=True)[:2]
        (slope_neg, intercept_neg), _ = np.polyfit(x_neg, y_neg, 1, full=True)[:2]
        (slope_combined, intercept_combined), _ = np.polyfit(x_combined, y_combined, 1, full=True)[:2]
        
        results[unit]["gradients"][instrument_name] = {
            "Positive Gradient": slope_pos,
            "Positive Intercept": intercept_pos,
            "Negative Gradient": slope_neg,
            "Negative Intercept": intercept_neg,
            "Combined Gradient": slope_combined,
            "Combined Intercept": intercept_combined
        }

# Modified print section to show intercepts
for unit in units:
    print(f"\n{'='*40}\nUnit: {unit.upper()}\n{'='*40}")
    
    pos_data = pd.DataFrame({clean_filename(f): results[unit]["data"][f]["Positive"] 
                           for f in results[unit]["data"]}).round(4)
    neg_data = pd.DataFrame({clean_filename(f): results[unit]["data"][f]["Negative"] 
                           for f in results[unit]["data"]}).round(4)
    
    print("\nPositive Values:")
    print(pos_data)
    print("\nNegative Values:")
    print(neg_data)
    
    if results[unit]["gradients"]:
        print("\nGradient and Intercept Analysis vs Pressure Calibrator:")
        grad_df = pd.DataFrame.from_dict(results[unit]["gradients"], orient='index')
        print(grad_df.round(4))

# Verify gradient consistency (unchanged from original)
print("\n\n" + "="*60)
print("Unit Consistency Validation")
print("="*60)

for instrument in ["Bourden_Gauge_2", "Bourden_Gauge", "Bundenburg_Gauge", "Hg_Glass"]:
    grad_types = ["Positive Gradient", "Negative Gradient", "Combined Gradient"]
    
    for grad_type in grad_types:
        gradients = []
        for unit in units:
            try:
                gradients.append(results[unit]["gradients"][instrument][grad_type])
            except KeyError:
                continue
        
        if len(gradients) > 0:
            base_grad = gradients[0]
            consistent = np.allclose(gradients, base_grad, rtol=0.01)
            
            print(f"{instrument} {grad_type}:")
            print(f"  Units: {len(gradients)} | Mean: {np.mean(gradients):.4f} ± {np.std(gradients):.4f}")
            print(f"  Consistent across units? {'True' if consistent else 'False'}")
            print("-"*50)

print("\nProcessing complete.")