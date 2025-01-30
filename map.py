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
df['G_abs'] = df['phot_g_mean_mag'] + 5 * (np.log10(df['parallax'] / 1000) + 5)

# Calculate Color Index (Bp-Rp)
df['Bp-Rp'] = df['phot_bp_mean_mag'] - df['phot_rp_mean_mag']

# Drop rows with NaN values in necessary columns
df = df.dropna(subset=['G_abs', 'Bp-Rp'])

# Classify Stellar Populations
main_sequence = df[(df['G_abs'] > 0) & (df['G_abs'] < 10) & (df['Bp-Rp'] > 0) & (df['Bp-Rp'] < 2)]
red_giants = df[(df['G_abs'] < 0) & (df['Bp-Rp'] > 1.0)]
white_dwarfs = df[(df['G_abs'] > 10) & (df['Bp-Rp'] < 0.5)]

# Plot the Hertzsprung-Russell Diagram with Stellar Populations
plt.figure(figsize=(10, 8))

# Main Sequence
plt.scatter(main_sequence['Bp-Rp'], main_sequence['G_abs'], s=1, c='blue', label='Main Sequence', alpha=0.5)
# Red Giants
plt.scatter(red_giants['Bp-Rp'], red_giants['G_abs'], s=1, c='red', label='Red Giants', alpha=0.5)
# White Dwarfs
plt.scatter(white_dwarfs['Bp-Rp'], white_dwarfs['G_abs'], s=1, c='green', label='White Dwarfs', alpha=0.5)

# Invert y-axis for HR diagram
plt.gca().invert_yaxis()

plt.title('Hertzsprung-Russell Diagram with Stellar Populations')
plt.xlabel('Color Index (Bp - Rp)')
plt.ylabel('Absolute Magnitude (G_abs)')
plt.legend()
plt.grid()
plt.show()
