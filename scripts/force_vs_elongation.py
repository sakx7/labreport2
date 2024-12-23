import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Load the data
AR = pd.read_csv('data/data1.csv')
PH = pd.read_csv('data/data2.csv')
ST = pd.read_csv('data/data3.csv')

# Assign the correct variables for Force and Elongation
elongation1, force1 = AR['Elongation'], AR['Force']
elongation2, force2 = PH['Elongation'], PH['Force']
elongation3, force3 = ST['Elongation'], ST['Force']

# Create the plot
plt.figure(figsize=(10, 10))

# Plot the data for each specimen
plt.plot(elongation1, force1, label='AR', color='red')
plt.plot(elongation2, force2, label='PH', color='blue')
plt.plot(elongation3, force3, label='ST', color='green')

# Set the axis labels
plt.xlabel('(Use for Strain) in mm')
plt.ylabel('(Use for Stress) in N')
plt.title('Differentiation of specimen by cobr')

# Add a legend
plt.legend()

# Set major and minor tick intervals for x and y axes
plt.gca().xaxis.set_major_locator(MultipleLocator(5))
plt.gca().xaxis.set_minor_locator(MultipleLocator(1))

plt.gca().yaxis.set_major_locator(MultipleLocator(5000))
plt.gca().yaxis.set_minor_locator(MultipleLocator(1000))

# Enable the grid with custom styling
plt.grid(True, linestyle='--', alpha=0.7)

# Set the limits for the axes
plt.xlim(0, 20.5)
plt.ylim(bottom=0)

# Save the figure
plt.savefig('figures/force_vs_elongation.png', dpi=1000)

# Display the plot
plt.show()
