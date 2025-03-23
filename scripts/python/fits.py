import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Define paths
data_dir = "data/same_units"
output_dir = "figures"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Identify files
files = sorted([f for f in os.listdir(data_dir) if f.endswith("_bar.csv")])

# Identify the calibrator file
calibrator_file = "Pressure_Calibrator_bar.csv"
if calibrator_file not in files:
    raise FileNotFoundError(f"{calibrator_file} not found in {data_dir}")

# Read calibrator data
calibrator_df = pd.read_csv(os.path.join(data_dir, calibrator_file))

# Check for required columns
if "Positive" not in calibrator_df.columns or "Negative" not in calibrator_df.columns:
    raise ValueError(f"{calibrator_file} does not have expected 'Positive' and 'Negative' columns.")

# Function to fit and plot best-fit lines
def plot_best_fit(x, y, label,file, color, linestyle="--", alpha=0.6):
    coeffs = np.polyfit(x, y, 1)  # Linear fit (y = mx + c)
    poly_eq = np.poly1d(coeffs)
    plt.plot(x, poly_eq(x), linestyle=linestyle, color=color, label=f"{label} (Fit)", alpha=alpha)
    print(f"{file},{label}, best-fit equation: y = {coeffs[0]:.4f}x + {coeffs[1]:.4f}")

# Loop through all instruments
for file in files:
    if file == calibrator_file:
        continue  # Skip the calibrator itself

    instrument_df = pd.read_csv(os.path.join(data_dir, file))

    # Check if required columns exist
    if "Positive" not in instrument_df.columns or "Negative" not in instrument_df.columns:
        print(f"Skipping {file}: Missing 'Positive' or 'Negative' columns.")
        continue

    # Extract values
    x_pos, y_pos = instrument_df["Positive"], calibrator_df["Positive"]
    x_neg, y_neg = instrument_df["Negative"], calibrator_df["Negative"]

    # Combined data
    x_combined = np.concatenate([x_pos, x_neg])
    y_combined = np.concatenate([y_pos, y_neg])

    # Plot 1: Negative data with best-fit line (adjusted axes)
    plt.figure(figsize=(8, 6))
    plt.scatter(x_neg, y_neg, color="blue", label="Negative", alpha=0.7)
    plot_best_fit(x_neg, y_neg, "Negative",file, "blue")

    # Adjust axes for negative plot
    ax = plt.gca()
    ax.xaxis.tick_top()  # Move x-axis to the top
    ax.yaxis.tick_right()  # Move y-axis to the right
    ax.xaxis.set_label_position('top')  # Move x-axis label to the top
    ax.yaxis.set_label_position('right')  # Move y-axis label to the right

    plt.xlabel(file.replace("_bar.csv", "").replace("_", " ") + " (bar)")
    plt.ylabel("Pressure Calibrator (bar)")
    plt.title(f"Calibration: {file.replace('_bar.csv', '')} (Negative) vs Calibrator")
    plt.legend(loc='lower left')  # Adjust legend position
    plt.grid(True)
    output_path_neg = os.path.join(output_dir, file.replace("_bar.csv", "_negative_calibration.png"))
    plt.savefig(output_path_neg, dpi=300)
    plt.show()
    plt.close()
    #print(f"Saved plot: {output_path_neg}")

    # Plot 2: Positive data with best-fit line (unchanged)
    plt.figure(figsize=(8, 6))
    plt.scatter(x_pos, y_pos, color="red", label="Positive", alpha=0.7)
    plot_best_fit(x_pos, y_pos, "Positive",file, "red")
    plt.xlabel(file.replace("_bar.csv", "").replace("_", " ") + " (bar)")
    plt.ylabel("Pressure Calibrator (bar)")
    plt.title(f"Calibration: {file.replace('_bar.csv', '')} (Positive) vs Calibrator")
    plt.legend()
    plt.grid(True)
    output_path_pos = os.path.join(output_dir, file.replace("_bar.csv", "_positive_calibration.png"))
    plt.savefig(output_path_pos, dpi=300)
    plt.show()
    plt.close()
    #print(f"Saved plot: {output_path_pos}")

    # Plot 3: Combined data with distinct dot colors and a single best-fit line (centered axes)
    plt.figure(figsize=(8, 6))
    ax = plt.gca()

    # Move spines to the center
    ax.spines['left'].set_position('zero')  # Move left spine to zero
    ax.spines['bottom'].set_position('zero')  # Move bottom spine to zero
    ax.spines['right'].set_color('none')  # Remove right spine
    ax.spines['top'].set_color('none')  # Remove top spine

    # Plot data points
    plt.scatter(x_pos, y_pos, color="blue", label="Positive", alpha=0.7)  # Positive points in blue
    plt.scatter(x_neg, y_neg, color="red", label="Negative", alpha=0.7)  # Negative points in red
    plot_best_fit(x_combined, y_combined, "Combined",file, "black", linestyle="-")  # Combined best-fit in black with solid line

    # Add arrows to indicate the direction of the axes
    ax.plot((1), (0), ls="", marker=">", ms=10, color="k", transform=ax.get_yaxis_transform(), clip_on=False)
    ax.plot((0), (1), ls="", marker="^", ms=10, color="k", transform=ax.get_xaxis_transform(), clip_on=False)

    # Labels and title
    plt.xlabel(file.replace("_bar.csv", "").replace("_", " ") + " (bar)")
    plt.ylabel("Pressure Calibrator (bar)")
    plt.title(f"Calibration: {file.replace('_bar.csv', '')} (Combined) vs Calibrator")
    plt.legend()
    plt.grid(True)
    output_path_combined = os.path.join(output_dir, file.replace("_bar.csv", "_combined_calibration.png"))
    plt.savefig(output_path_combined, dpi=300)
    plt.show()
    plt.close()
    #print(f"Saved plot: {output_path_combined}")
    print(f"------------------------")
    
print("All plots generated and saved in 'figures/'")    