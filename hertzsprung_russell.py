import pandas as pd
from astropy.table import Table
import matplotlib.pyplot as plt
import numpy as np

def color_to_temp(bp_rp):
    """Convert Bp-Rp color index to effective temperature (Kelvin)."""
    return 4600 * (1 / (0.92 * bp_rp + 1.7) + 1 / (0.92 * bp_rp + 0.62))

# Load the data
file_path = 'all_w_rv_kin_3k.fits'
tb = Table.read(file_path)
df = tb.to_pandas()

# Ensure relevant columns are numeric
df['parallax'] = pd.to_numeric(df['parallax'], errors='coerce')
df['phot_g_mean_mag'] = pd.to_numeric(df['phot_g_mean_mag'], errors='coerce')
df['phot_bp_mean_mag'] = pd.to_numeric(df['phot_bp_mean_mag'], errors='coerce')
df['phot_rp_mean_mag'] = pd.to_numeric(df['phot_rp_mean_mag'], errors='coerce')

# Filter out rows with invalid or negative parallax
df = df[df['parallax'] > 0]

# Calculate Absolute Magnitude (G_abs)
df['G_abs'] = df['phot_g_mean_mag'] - 5 * (np.log10(df['parallax'] / 1000) + 5)

# Calculate Color Index (Bp-Rp)
df['Bp-Rp'] = df['phot_bp_mean_mag'] - df['phot_rp_mean_mag']

# Drop rows with NaN values in necessary columns
df = df.dropna(subset=['G_abs', 'Bp-Rp'])

# Calculate Effective Temperature
df['T_eff'] = df['Bp-Rp'].apply(color_to_temp)

# Drop rows with NaN or invalid temperature values
df = df[df['T_eff'] > 0]

# Identify Stellar Populations
main_sequence = df[(df['T_eff'] > 3000) & (df['G_abs'] > 2) & (df['G_abs'] < 10)]
red_giants = df[(df['T_eff'] < 5000) & (df['G_abs'] < 2)]
white_dwarfs = df[(df['T_eff'] > 6000) & (df['G_abs'] > 10)]

# Stars that don't fall into any category
unclassified = df[~df.index.isin(main_sequence.index) & 
                  ~df.index.isin(red_giants.index) & 
                  ~df.index.isin(white_dwarfs.index)]

# Plot the Hertzsprung-Russell Diagram with Stellar Populations
plt.figure(figsize=(10, 8))

# Main Sequence
plt.scatter(main_sequence['T_eff'], main_sequence['G_abs'], s=1, c='blue', label='Main Sequence', alpha=0.5)
# Red Giants
plt.scatter(red_giants['T_eff'], red_giants['G_abs'], s=1, c='red', label='Red Giants', alpha=0.5)
# White Dwarfs
plt.scatter(white_dwarfs['T_eff'], white_dwarfs['G_abs'], s=1, c='green', label='White Dwarfs', alpha=0.5)
# Unclassified stars
plt.scatter(unclassified['T_eff'], unclassified['G_abs'], s=1, c='black', label='Unclassified', alpha=0.5)

# Invert the x-axis (hotter stars on the left)
plt.gca().invert_xaxis()

# Invert y-axis for HR diagram
plt.gca().invert_yaxis()

plt.title('Hertzsprung-Russell Diagram with Stellar Populations')
plt.xlabel('Effective Temperature (K)')
plt.ylabel('Absolute Magnitude (G_abs)')
plt.legend()
plt.grid()
plt.show()
