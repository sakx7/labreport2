import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

plt.rcParams['font.size'] = 25  # Replace 12 with your desired font size

# Load the data
AR = pd.read_csv('data/AR_stress_strain.csv')
PH = pd.read_csv('data/PH_stress_strain.csv')
ST = pd.read_csv('data/ST_stress_strain.csv')

# Assign the correct variables for Strain and Stress
AR_strain, AR_stress = AR['Strain'], AR['Stress']
PH_strain, PH_stress = PH['Strain'], PH['Stress']
ST_strain, ST_stress = ST['Strain'], ST['Stress']

# Function to calculate Young's modulus
def calculate_youngs_modulus(strain, stress, start_fraction, stop_fraction=None):
    start_index = int(start_fraction * len(strain))
    if stop_fraction is not None:
        stop_index = int(stop_fraction * len(strain))
    else:
        stop_index = len(strain)

    start_index = max(start_index, 0)
    stop_index = min(stop_index, len(strain))

    strain_linear = strain[start_index:stop_index]
    stress_linear = stress[start_index:stop_index]

    slope, intercept, r_value, p_value, std_err = linregress(strain_linear, stress_linear)
    return slope

# Calculate Young's modulus for each specimen
E_AR = calculate_youngs_modulus(AR_strain, AR_stress, 0.1, 0.4)   # Start after first 10%, stop after 40%
E_PH = calculate_youngs_modulus(PH_strain, PH_stress, 0.1, 0.4)   # Start after first 10%, stop after 40%
E_ST = calculate_youngs_modulus(ST_strain, ST_stress, 0.0, 0.1)   # Start from 0%, stop at 10%

# Function to plot stress vs strain with Young's modulus lines
def plot_stress_strain_with_fit(strain, stress, E, label, color, skip_fraction):
    plt.plot(strain, stress, label=label, color=color)

    # Calculate starting index for skipping
    start_index = int(skip_fraction * len(strain))

    # Create fitted line for Young's modulus
    strain_fit = np.linspace(0, max(strain), 100)

    if label == 'ST':
        # For ST: Fit line starts from zero
        stress_fit = E * strain_fit
    else:
        # For AR and PH: Fit line starts from a shifted strain value
        stress_fit = E * (strain_fit - strain[start_index]) + stress[start_index]

    plt.plot(strain_fit, stress_fit, color=color, linestyle='--', label=f'{label} Fit')

# Create separate plots for each specimen
specimens = [
    (AR_strain, AR_stress, E_AR, 'AR', 'blue', 0.1),
    (PH_strain, PH_stress, E_PH, 'PH', 'green', 0.1),
    (ST_strain, ST_stress, E_ST, 'ST', 'red', 0.02)
]

for strain, stress, E, label, color, skip_fraction in specimens:
    plt.figure(figsize=(10, 10))
    plot_stress_strain_with_fit(strain, stress, E, label, color, skip_fraction)

    # Set the axis labels and title
    plt.xlabel(r'Strain $(\varepsilon)$ [dimensionless]', fontsize=30)
    plt.ylabel(r'Stress $(\sigma)$ $[\text{N/}\text{mm}^2]$', fontsize=30)
    plt.title(f'Stress vs Strain for {label} with Young\'s Modulus', fontsize=25)

    print(f"Young's Modulus for {label}: {E} N/mm^2")

    # Add a legend and grid
    plt.legend(fontsize=16)
    plt.grid(True)

    # Set limits for the axes with padding
    x_max = max(strain)
    y_max = max(stress)
    plt.xlim(0, x_max * 1.05)
    plt.ylim(bottom=0, top=y_max * 1.05)

    # Save the figure and display it
    plt.tight_layout()
    plt.savefig(f'figures/stress_vs_strain_with_fit_{label}.png', dpi=1000,bbox_inches='tight')
    plt.show()
