
import numpy as np
import matplotlib.pyplot as plt

# Conversion factors for each unit to bar
psi_to_bar = 0.0689476
kn_m2_to_bar = 0.01
cmHg_to_bar = 0.00133322

# Data in respective units (converted to bar for consistency)
pressurecalibrator = np.array([0, 5.7, 10.4, 16, 21.1, 27.7, 34.2, 40, 46.1, 52.2]) * 0.001  # kPa to bar
bourdongauge = np.array([0, 1, 1.6, 2.4, 3.1, 4, 5, 5.8, 6.6, 7.5]) * psi_to_bar  # psi to bar
bourdongaugetwo = np.array([0, 7, 13, 19, 24, 29, 38, 44, 49, 56]) * kn_m2_to_bar  # kN/m^2 to bar
bundenbergpressuregauge = np.array([0, 0.05, 0.09, 0.15, 0.2, 0.27, 0.34, 0.4, 0.45, 0.52])  # already in bar
hgglassmanometer = np.array([0, 3.1, 4.9, 7, 9, 11.2, 13.8, 16, 18.3, 20.6]) * cmHg_to_bar  # cm Hg to bar

# Negative counterparts in respective units (converted to bar)
pressurecalibrators_neg = np.array([0, -5.6, -12.1, -18, -21.8, -25.4, -29.3, -33.6, -37.6, -41.7]) * 0.001  # kPa to bar
bourdongauges = np.array([0, -0.8, -1.7, -3.2, -4, -5.2, -7.2, -8.3, -9.5, -10.7]) * psi_to_bar  # psi to bar
bourdongaugetwos = np.array([0, -3.5, -11.5, -17.5, -22.5, -25.5, -29.5, -34.5, -38.5, -42.5]) * kn_m2_to_bar  # kN/m^2 to bar
bundenbergpressuregauges = np.array([0, -0.05, -0.11, -0.19, -0.22, -0.25, -0.3, -0.35, -0.39, -0.44])  # already in bar
hgglassmanometers = np.array([0, -1.1, -4.1, -5.8, -7.2, -8.6, -10, -11.7, -13.2, -14.8]) * cmHg_to_bar  # cm Hg to bar


print(pressurecalibrator)
print(bourdongauge)
print(bourdongaugetwo)
print(bundenbergpressuregauge)
print(hgglassmanometer)

print(pressurecalibrators_neg)
print(bourdongauges)
print(bourdongaugetwos)
print(bundenbergpressuregauges)
print(hgglassmanometers)



# Create x values (indices of data points)
x = np.arange(len(pressurecalibrator))

# Function to plot data and fit line, and return the gradient
def plot_with_best_fit(data, label):
    p = np.polyfit(x, data, 1)  # Line of best fit (linear fit)
    y_fit = np.polyval(p, x)  # Best fit values
    gradient = p[0]  # The first coefficient is the gradient (slope)
    plt.scatter(x, data, label=label)
    plt.plot(x, y_fit, linestyle='--', label=f"Best fit ({label})")
    return gradient

# Plot all data sets
plt.figure(figsize=(12, 10))

# Plot for Pressure Calibrator
plt.subplot(2, 2, 1)
gradient_1 = plot_with_best_fit(pressurecalibrator, "Pressure Calibrator (Positive)")
gradient_2 = plot_with_best_fit(pressurecalibrators_neg, "Pressure Calibrators (Negative)")
plt.title('Pressure Calibrator')
plt.xlabel('Index')
plt.ylabel('Pressure (bar)')
plt.axhline(0, color='black',linewidth=1)  # Add horizontal axis
plt.axvline(0, color='black',linewidth=1)  # Add vertical axis
plt.grid(True)
print(f"Gradient for Pressure Calibrator (Positive): {gradient_1}")
print(f"Gradient for Pressure Calibrators (Negative): {gradient_2}")

# Plot for Bourdon Gauge
plt.subplot(2, 2, 2)
gradient_3 = plot_with_best_fit(bourdongauge, "Bourdon Gauge (Positive)")
gradient_4 = plot_with_best_fit(bourdongauges, "Bourdon Gauge (Negative)")
plt.title('Bourdon Gauge')
plt.xlabel('Index')
plt.ylabel('Pressure (bar)')
plt.axhline(0, color='black',linewidth=1)  # Add horizontal axis
plt.axvline(0, color='black',linewidth=1)  # Add vertical axis
plt.grid(True)
print(f"Gradient for Bourdon Gauge (Positive): {gradient_3}")
print(f"Gradient for Bourdon Gauge (Negative): {gradient_4}")

# Plot for Bourdon Gauge Two
plt.subplot(2, 2, 3)
gradient_5 = plot_with_best_fit(bourdongaugetwo, "Bourdon Gauge Two (Positive)")
gradient_6 = plot_with_best_fit(bourdongaugetwos, "Bourdon Gauge Two (Negative)")
plt.title('Bourdon Gauge Two')
plt.xlabel('Index')
plt.ylabel('Pressure (bar)')
plt.axhline(0, color='black',linewidth=1)  # Add horizontal axis
plt.axvline(0, color='black',linewidth=1)  # Add vertical axis
plt.grid(True)
print(f"Gradient for Bourdon Gauge Two (Positive): {gradient_5}")
print(f"Gradient for Bourdon Gauge Two (Negative): {gradient_6}")

# Plot for Bundenberg Pressure Gauge
plt.subplot(2, 2, 4)
gradient_7 = plot_with_best_fit(bundenbergpressuregauge, "Bundenberg Pressure Gauge (Positive)")
gradient_8 = plot_with_best_fit(bundenbergpressuregauges, "Bundenberg Pressure Gauge (Negative)")
plt.title('Bundenberg Pressure Gauge')
plt.xlabel('Index')
plt.ylabel('Pressure (bar)')
plt.axhline(0, color='black',linewidth=1)  # Add horizontal axis
plt.axvline(0, color='black',linewidth=1)  # Add vertical axis
plt.grid(True)
print(f"Gradient for Bundenberg Pressure Gauge (Positive): {gradient_7}")
print(f"Gradient for Bundenberg Pressure Gauge (Negative): {gradient_8}")

# Adjust layout
plt.tight_layout()
plt.show()
