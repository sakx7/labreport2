import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.size'] = 25  # Adjust font size

# Load the data
AR = pd.read_csv('data/AR_stress_strain.csv')
PH = pd.read_csv('data/PH_stress_strain.csv')
ST = pd.read_csv('data/ST_stress_strain.csv')

# Assign the correct variables for Strain and Stress
AR_strain, AR_stress = AR['Strain'], AR['Stress']
PH_strain, PH_stress = PH['Strain'], PH['Stress']
ST_strain, ST_stress = ST['Strain'], ST['Stress']

def plot_stress_strain_with_ultstrain(strain, stress, label, color):
    # Plot stress-strain curve
    plt.plot(strain, stress, label=label, color=color)
    
    # Find ultimate strain (strain at fracture)
    ultimate_strain = strain[stress > 0].iloc[-1]  # Last non-zero stress point
    ultimate_stress = stress[stress > 0].iloc[-1]  # Corresponding stress
    print(ultimate_strain)

    # Highlight the ultimate strain point
    plt.scatter(ultimate_strain, ultimate_stress, color=color, s=100, label=f'Fracture ({label})')
    
    # Adjust annotation position relative to the ultimate point
    text_x = ultimate_strain * 0.75  # 5% to the left of the point
    text_y = ultimate_stress * 1.02  # 2% above the point
    
    plt.text(text_x, text_y,
             f'({ultimate_strain:.2f}, {ultimate_stress:.2f})',
             fontsize=20, color=color)

# Create separate plots for each specimen
specimens = [
    (AR_strain, AR_stress, 'AR', 'blue'),
    (PH_strain, PH_stress, 'PH', 'green'),
    (ST_strain, ST_stress, 'ST', 'red')
]

for strain, stress, label, color in specimens:
    plt.figure(figsize=(10, 10))
    
    plot_stress_strain_with_ultstrain(strain, stress, label, color)
    
    plt.xlabel(r'Strain $(\varepsilon)$ [dimensionless]', fontsize=30)
    plt.ylabel(r'Stress $(\sigma)$ $[\text{N/}\text{mm}^2]$', fontsize=30)
    plt.title(f'Stress vs Strain for {label} with Fracture Strain', fontsize=25)
    
    plt.legend(fontsize=16)
    plt.grid(True)

    x_max = strain.max()
    y_max = stress.max()
    plt.xlim(0, x_max * 1.05)
    plt.ylim(bottom=0, top=y_max * 1.05)

    plt.tight_layout()
    plt.savefig(f'figures/stress_vs_strain_with_ultstrain_{label}.png', dpi=1000, bbox_inches='tight')
    plt.show()
