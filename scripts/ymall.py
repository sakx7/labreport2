import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
from scipy.stats import linregress

# Load the data
AR = pd.read_csv('data/AR_stress_strain.csv')
PH = pd.read_csv('data/PH_stress_strain.csv')
ST = pd.read_csv('data/ST_stress_strain.csv')

# Assign the correct variables for Force and Elongation
AR_strain, AR_stress = AR['Strain'], AR['Stress']
PH_strain, PH_stress = PH['Strain'], PH['Stress']
ST_strain, ST_stress = ST['Strain'], ST['Stress']

# Function to calculate Young's modulus
def calculate_youngs_modulus(strain, stress, start_fraction, stop_fraction=None):
    # Calculate start index based on start_fraction
    start_index = int(start_fraction * len(strain))
    # Calculate stop index based on stop_fraction or use the length of the strain if None
    if stop_fraction is not None:
        stop_index = int(stop_fraction * len(strain))
    else:
        stop_index = len(strain)
    # Ensure indices are within bounds
    start_index = max(start_index, 0)
    stop_index = min(stop_index, len(strain))
    strain_linear = strain[start_index:stop_index]
    stress_linear = stress[start_index:stop_index]
    # Perform linear regression
    slope, intercept, r_value, p_value, std_err = linregress(strain_linear, stress_linear)
    return slope

# Calculate Young's modulus for each specimen
E_AR = calculate_youngs_modulus(AR_strain, AR_stress, 0.1, 0.4)   # Start after first 10%, stop after 40%
E_PH = calculate_youngs_modulus(PH_strain, PH_stress,0.1,0.4) # start slope calc after first 10% of the stop after 40%
E_ST = calculate_youngs_modulus(ST_strain, ST_stress, 0,0.1)  # Start from 0% of data 10% of data, stop at end

# Create the plot for Stress vs Strain with Young's modulus lines
plt.figure(figsize=(10, 10))

# Calculate and plot Young's modulus lines (linear fits)

skip_fraction_AR = 0.1  # 10%
skip_fraction_PH = 0.1   # 10%
skip_fraction_ST = 0.02   # 2%

# Calculate starting index for skipping
start_index_AR = int(skip_fraction_AR * len(AR_strain))
start_index_PH = int(skip_fraction_PH * len(PH_strain))
start_index_ST = int(skip_fraction_ST * len(ST_strain))


# Plot the data for each specimen

# For AR: Fit line starting from a shifted strain value
strain_fit_AR = np.linspace(0, max(AR_strain), 100)
stress_fit_AR = E_AR * (strain_fit_AR - AR_strain[start_index_AR]) + AR_stress[start_index_AR]  # Shifted by skipped amount
plt.plot(AR_strain, AR_stress, label='AR', color='blue')
plt.plot(strain_fit_AR, stress_fit_AR, color='blue', linestyle='--', label=f'AR Fit: E={E_AR:.2f} N/mm²')

# For PH: Fit line starting from a shifted strain value
strain_fit_PH = np.linspace(0, max(PH_strain), 100)
stress_fit_PH = E_PH * (strain_fit_PH - PH_strain[start_index_PH]) + PH_stress[start_index_PH]  # Shifted by skipped amount
plt.plot(PH_strain, PH_stress, label='PH', color='green')
plt.plot(strain_fit_PH, stress_fit_PH, color='green', linestyle='--', label=f'PH Fit: E={E_PH:.2f} N/mm²')

strain_fit_ST = np.linspace(0, max(ST_strain), 100)
stress_fit_ST = E_ST * strain_fit_ST
plt.plot(ST_strain, ST_stress, label='ST', color='red')
plt.plot(strain_fit_ST, stress_fit_ST, color='red', linestyle='--', label=f'ST Fit: E={E_ST:.2f} N/mm²')

# Set the axis labels and title
plt.xlabel(r'Strain $(\varepsilon)$ [dimensionless]', fontsize=14)
plt.ylabel(r'Stress $(\sigma)$ $[\text{N/}\text{mm}^2]$', fontsize=14)
plt.title('Stress vs Strain for Different Specimens with Young\'s Modulus', fontsize=16)

# Add a legend and grid
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)

# Set limits for the axes with padding
x_max = max(max(AR_strain), max(PH_strain), max(ST_strain))
y_max = max(max(AR_stress), max(PH_stress), max(ST_stress))
plt.xlim(0, x_max * 1.05)  
plt.ylim(bottom=0, top=y_max * 1.05)  

# Save the figure and display it
plt.tight_layout()
plt.savefig('figures/stress_vs_strain_with_fits.png', dpi=1000, bbox_inches='tight')
plt.show()
