import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Load the data
AR = pd.read_csv('data/AR_Force_Elongation.csv')
PH = pd.read_csv('data/PH_Force_Elongation.csv')
ST = pd.read_csv('data/ST_Force_Elongation.csv')

# Assign the correct variables for Force and Elongation
elongation1, force1 = AR['Elongation'], AR['Force']
elongation2, force2 = PH['Elongation'], PH['Force']
elongation3, force3 = ST['Elongation'], ST['Force']

# Create the plot
plt.figure(figsize=(10, 10))

# Plot the data for each specimen
plt.plot(elongation1, force1, label='AR', color='blue')
plt.plot(elongation2, force2, label='PH', color='green')
plt.plot(elongation3, force3, label='ST', color='red')

plt.rcParams['text.usetex'] = True

# Set the axis labels and title with increased font size
plt.xlabel(r'Elongation $(\Delta L)$ [mm]', fontsize=14)
plt.ylabel(r'Force $(F)$ [N]', fontsize=14)
plt.title(r'Force vs Change in Length for Different Specimens', fontsize=16)

# Add a legend
plt.legend(fontsize=16)  # Adjust the fontsize as needed

# Enable the grid with custom styling
plt.grid(True, linestyle='--', alpha=0.7)

# Set the limits for the axes
plt.xlim(0, 20.5)
plt.ylim(bottom=0)

plt.tight_layout()
# Save the figure
plt.savefig('figures/force_vs_elongation.png', dpi=1000, bbox_inches='tight')
# Display the plot
plt.show()
