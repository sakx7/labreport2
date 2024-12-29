import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.size'] = 25  # Replace 12 with your desired font size

# Load the data
AR = pd.read_csv('data/AR_stress_strain.csv')
PH = pd.read_csv('data/PH_stress_strain.csv')
ST = pd.read_csv('data/ST_stress_strain.csv')

# Assign the correct variables for Strain and Stress
AR_strain, AR_stress = AR['Strain'], AR['Stress']
PH_strain, PH_stress = PH['Strain'], PH['Stress']
ST_strain, ST_stress = ST['Strain'], ST['Stress']

def plot_stress_strain(strain, stress, label, color):
    plt.plot(strain, stress, label=label, color=color)

def calculate_uts(stress):
    return max(stress)  # UTS is the maximum stress value

# Calculate UTS for each material
uts_AR = calculate_uts(AR_stress)
uts_PH = calculate_uts(PH_stress)
uts_ST = calculate_uts(ST_stress)

# Display UTS values
print(f"UTS for AR: {uts_AR} N/mm²")
print(f"UTS for PH: {uts_PH} N/mm²")
print(f"UTS for ST: {uts_ST} N/mm²")

# Create separate plots for each specimen
specimens = [
    (AR_strain, AR_stress, 'AR', 'blue', uts_AR),
    (PH_strain, PH_stress, 'PH', 'green', uts_PH),
    (ST_strain, ST_stress, 'ST', 'red', uts_ST)
]

for strain, stress, label, color, uts in specimens:
    plt.figure(figsize=(10, 10))
    
    plot_stress_strain(strain, stress, label, color)
    
    text_x = strain[stress.idxmax()] * 0.85  # 5% to the left of the point
    text_y = uts * 0.92  # 2% above the point


    # Highlight UTS
    plt.scatter(strain[stress.idxmax()], uts, color=color, zorder=5)  # Mark the UTS point
    plt.text(text_x, text_y, f'({strain[stress.idxmax()]:.2f}, {uts:.2f})', fontsize=25, color=color)
    
    plt.xlabel(r'Strain $(\varepsilon)$ [dimensionless]', fontsize=30)
    plt.ylabel(r'Stress $(\sigma)$ $[\text{N/}\text{mm}^2]$', fontsize=30)
    plt.title(f'Stress vs Strain for {label} with UTS', fontsize=25)
    
    plt.legend(fontsize=16)
    plt.grid(True)

    x_max = strain.max()
    y_max = stress.max()
    plt.xlim(0, x_max * 1.05)
    plt.ylim(bottom=0, top=y_max * 1.05)

    plt.tight_layout()
    plt.savefig(f'figures/stress_vs_strain_with_uts_{label}.png', dpi=1000, bbox_inches='tight')
    plt.show()
