# Gaia Hackathon Project 2025

Tori Fowler, Hayden Tedrake, Damian Gold

# README: Astronomical Data Clustering and Hertzsprung-Russell Diagram

## Overview
This project analyzes astronomical data from Gaia, focusing on clustering stellar objects using DBSCAN and visualizing their spatial distributions. Additionally, it generates a Hertzsprung-Russell (HR) diagram to classify stellar populations.

## Requirements
Ensure you have the following Python packages installed:
- `pandas`
- `numpy`
- `scikit-learn`
- `matplotlib`
- `mpl_toolkits`
- `astropy`

Install missing dependencies using:
```bash
pip install pandas numpy scikit-learn matplotlib astropy
```

## Data Files
- `3k_gaia_kin_data.csv`: Contains Gaia astrometric data including RA, Dec, proper motions, and parallax.
- `all_w_rv_kin_3k.fits`: FITS file containing stellar photometric and astrometric data.

## Functionality
### 1. Parallax-Based Distance Calculation
Converts parallax measurements into distances from the Sun in parsecs.

### 2. Data Normalization
Scales astronomical data for clustering using `StandardScaler`.

### 3. DBSCAN Clustering
Identifies stellar clusters based on position and motion data, appending cluster labels to the dataset.

### 4. Coordinate Transformations
- **Cartesian Coordinates (X, Y, Z)**: Converts RA, Dec, and distance into 3D Cartesian coordinates.
- **Galactic Coordinates (l, b)**: Converts RA and Dec into galactocentric longitude and latitude.

### 5. Hertzsprung-Russell Diagram
- Computes absolute magnitudes (`G_abs`) using parallax.
- Computes color indices (`Bp-Rp`).
- Categorizes stars into:
  - Main Sequence
  - Red Giants
  - White Dwarfs
- Visualizes the HR diagram with temperature on the x-axis and absolute magnitude on the y-axis.

## Usage
### Running the Clustering Analysis
Execute the script to:
- Load `3k_gaia_kin_data.csv`
- Compute distances and normalize data
- Apply DBSCAN clustering
- Transform to Cartesian and Galactic coordinates
- Visualize clustered stars in 2D and 3D

```bash
python clustering_script.py
```

### Generating the HR Diagram
Execute the script to:
- Load `all_w_rv_kin_3k.fits`
- Compute absolute magnitudes
- Classify stellar populations
- Plot the HR diagram

```bash
python hr_diagram_script.py
```

## Visualization Outputs
- **2D Galactic Coordinate Plot**: Stars are colored by their DBSCAN cluster.
- **3D Cartesian Plot**: Spatial distribution of clusters.
- **HR Diagram**: Stellar classification based on absolute magnitude and color index.

## Notes
- Ensure the required FITS and CSV files are available in the working directory.
- Modify clustering parameters (`eps`, `min_samples`) to optimize DBSCAN performance.
- In the HR diagram, hotter stars appear on the left (temperature axis is inverted).

## License
This project is open-source and can be modified for research and educational purposes.
