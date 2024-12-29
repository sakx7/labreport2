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

# Function to plot stress-strain curve
def plot_stress_strain(strain, stress, label, color, modulus_of_toughness):
    plt.plot(strain, stress, label=f'{label} (MoT = {modulus_of_toughness:.2f} MPa)', color=color)
    plt.fill_between(strain, stress, color=color, alpha=0.3, label='Area under curve')

# Create separate plots for each specimen
specimens = [
    (AR_strain, AR_stress, 'AR', 'blue'),
    (PH_strain, PH_stress, 'PH', 'green'),
    (ST_strain, ST_stress, 'ST', 'red')
]

for strain, stress, label, color in specimens:
    # Calculate modulus of toughness
    modulus_of_toughness = np.trapezoid(stress, strain)  # Use trapezoid instead of trapz
    
    # Plot the stress-strain curve with modulus of toughness
    plt.figure(figsize=(10, 10))
    plot_stress_strain(strain, stress, label, color, modulus_of_toughness)
    
    plt.xlabel(r'Strain $(\varepsilon)$ [dimensionless]', fontsize=30)
    plt.ylabel(r'Stress $(\sigma)$ $[\text{N/}\text{mm}^2]$', fontsize=30)
    plt.title(f'Stress vs Strain for {label} with Modulus of Toughness', fontsize=25)
    
    plt.legend(fontsize=16)
    plt.grid(True)

    x_max = strain.max()
    y_max = stress.max()
    plt.xlim(0, x_max * 1.05)
    plt.ylim(bottom=0, top=y_max * 1.05)

    plt.tight_layout()
    plt.savefig(f'figures/stress_vs_strain_{label}_tough.png', dpi=1000, bbox_inches='tight')
    plt.show()

    # Print the modulus of toughness
    print(f"Modulus of Toughness for {label}: {modulus_of_toughness:.2f} MPa")
