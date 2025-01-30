import pandas as pd
from astropy.table import Table
import matplotlib.pyplot as plt
import numpy as np

# Load the data
file_path = 'all_w_rv_kin_3k.fits'

# Read the FITS file into an Astropy Table and convert to a Pandas DataFrame
tb = Table.read(file_path)
df = tb.to_pandas()

# Ensure relevant columns are numeric
df['parallax'] = pd.to_numeric(df['parallax'], errors='coerce')  # Ensure parallax is numeric
df['phot_g_mean_mag'] = pd.to_numeric(df['phot_g_mean_mag'], errors='coerce')  # Gaia G-band mean magnitude
df['phot_bp_mean_mag'] = pd.to_numeric(df['phot_bp_mean_mag'], errors='coerce')
df['phot_rp_mean_mag'] = pd.to_numeric(df['phot_rp_mean_mag'], errors='coerce')

# Filter out rows with invalid or negative parallax
df = df[df['parallax'] > 0]

# Calculate Absolute Magnitude (G_abs) using G_mag and parallax
# G_abs = G_mag + 5 * (log10(parallax) - 1)
df['G_abs'] = df['phot_g_mean_mag'] + 5 * (np.log10(df['parallax'] / 1000) + 5)

# Calculate Color Index (Bp-Rp)
df['Bp-Rp'] = df['phot_bp_mean_mag'] - df['phot_rp_mean_mag']

# Drop rows with NaN values in necessary columns
df = df.dropna(subset=['G_abs', 'Bp-Rp'])

# Create the Hertzsprung-Russell (Color-Magnitude) Diagram
plt.figure(figsize=(10, 8))
plt.scatter(df['Bp-Rp'], df['G_abs'], s=1, c='blue', alpha=0.5)
plt.gca().invert_yaxis()  # Invert y-axis for HR diagram
plt.title('Hertzsprung-Russell Diagram (Color-Magnitude Diagram)')
plt.xlabel('Color Index (Bp - Rp)')
plt.ylabel('Absolute Magnitude (G_abs)')
plt.grid()
plt.show()
