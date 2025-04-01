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
# Improved gradient consistency check
print("\n\n" + "="*60)
print("GRADIENT CONSISTENCY REPORT".center(60))
print("="*60)

# Create a summary table
gradient_summary = []

for instrument in ["Bourden_Gauge_2", "Bourden_Gauge", "Bundenburg_Gauge", "Hg_Glass"]:
    grad_types = ["Positive Gradient", "Negative Gradient", "Combined Gradient"]
    
    instrument_data = []
    
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
            std_dev = np.std(gradients)
            
            instrument_data.append({
                "Type": grad_type.replace(" Gradient", ""),
                "Mean": np.mean(gradients),
                "Std Dev": std_dev,
                "Min": np.min(gradients),
                "Max": np.max(gradients),
                "Range": np.ptp(gradients),
                "Consistent": consistent,
                "Units": len(gradients)
            })
    
    gradient_summary.append((instrument, instrument_data))

# Print the improved report
for instrument, data in gradient_summary:
    print(f"\n{instrument.replace('_', ' ').title():<25} {'='*35}")
    print(f"{'Type':<15} {'Mean':>8} {'Std Dev':>8} {'Range':>8} {'Consistent':>12}")
    print("-"*60)
    
    for row in data:
        print(f"{row['Type']:<15} {row['Mean']:>8.4f} {row['Std Dev']:>8.4f} "
              f"{row['Range']:>8.4f} {str(row['Consistent']):>12}")
    
    # Calculate and print overall consistency
    overall_consistent = all(row['Consistent'] for row in data)
    print("-"*60)
    print(f"{'OVERALL':<15} {'':>8} {'':>8} {'':>8} {str(overall_consistent):>12}")
    print(f"Units Tested: {data[0]['Units']} ({', '.join(units)})")

# Add this section after the gradient consistency check
print("\n\n" + "="*60)
print("Intercept Consistency Analysis")
print("="*60)

intercept_types = ["Positive Intercept", "Negative Intercept", "Combined Intercept"]

for instrument in ["Bourden_Gauge_2", "Bourden_Gauge", "Bundenburg_Gauge", "Hg_Glass"]:
    print(f"\n{instrument} Intercept Analysis:")
    
    # Create a dictionary to store all intercept data
    intercept_data = {it: [] for it in intercept_types}
    
    # Collect intercept values across all units
    for unit in units:
        try:
            for it in intercept_types:
                intercept_data[it].append(results[unit]["gradients"][instrument][it])
        except KeyError:
            continue
    
    # Create a DataFrame for beautiful display
    analysis_df = pd.DataFrame(index=intercept_types, 
                              columns=["Mean", "Min", "Max", "Range (Magnitude)"])
    
    # Calculate statistics for each intercept type
    for it in intercept_types:
        if intercept_data[it]:
            vals = np.array(intercept_data[it])
            analysis_df.loc[it, "Mean"] = np.mean(vals)
            analysis_df.loc[it, "Min"] = np.min(vals)
            analysis_df.loc[it, "Max"] = np.max(vals)
            analysis_df.loc[it, "Range (Magnitude)"] = np.max(vals) - np.min(vals)
    
    # Display the results
    print(analysis_df.round(4))
    print("-"*60)

print("\nProcessing complete.")