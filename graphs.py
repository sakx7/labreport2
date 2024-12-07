import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

data1 = pd.read_csv('data1.csv')
data2 = pd.read_csv('data2.csv')
data3 = pd.read_csv('data3.csv')

strain1, stress1 = data1['Strain'], data1['Stress']
strain2, stress2 = data2['Strain'], data2['Stress']
strain3, stress3 = data3['Strain'], data3['Stress']

plt.figure(figsize=(10, 10))

plt.plot(strain1, stress1, label='AR', color='red')
plt.plot(strain2, stress2, label='PH', color='blue')
plt.plot(strain3, stress3, label='ST', color='green')
plt.xlabel('(Use for Strain) in mm')
plt.ylabel('(Use for Stress) in N')
plt.title('Differentiation of specimen by cobr')
plt.legend()

plt.gca().xaxis.set_major_locator(MultipleLocator(5))
plt.gca().xaxis.set_minor_locator(MultipleLocator(1))

plt.gca().yaxis.set_major_locator(MultipleLocator(5000))
plt.gca().yaxis.set_minor_locator(MultipleLocator(1000)) 

plt.grid(True, linestyle='--', alpha=0.7)

plt.xlim(0, 20.5)
plt.ylim(bottom=0)
plt.savefig('graph.png',dpi=1000)

plt.show()

