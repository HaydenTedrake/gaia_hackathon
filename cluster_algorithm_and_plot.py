import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


from astropy import units as u
import astropy.coordinates as coord
from astropy.coordinates import SkyCoord

##############################################
#             HELPER FUNCTIONS               #
##############################################

def parallax_to_distance(parallax_array: list):
    """
    Computes the distance an object is from the Sun based on its parallax.

    Arguments:
        parallax_array, list
            A list (or NumPy array) of parallaxes in milliarcsecs

    Return:
        list
            A list of the distances computed from each parallax
            in the parallax_array in parsecs
    """
    distance_array = 1.0 / (parallax_array)
    return distance_array

def scale_data(dataframe):
    """
    Returns a scaled 2-D array of a dataframe by applying a normalizing
    scaler to each column of the dataframe.

    Arguments:
        dataframe, Pandas Array
            A dataframe containing astronomical data.
    Return:
        scaled_data, pandas arary
            A dataframe meeting the above specification.
    """
    scaler = StandardScaler()
    return scaler.fit_transform(dataframe)

def cluster_data(df, scaled_dataframe, eps, min_samples):
    """
    Performs a DBSCAN algorithm on a scaled dataframe, modifying

    Arguments:
        df, dataframe
            An original (astronomical) dataframe to which to append
            information about cluster identity.
        scaled_dataframe, 2-D array
            An array with scaled data of the df dataframe that
            will be used to calculate clusters.
        eps, float
            The maximum Euclidean distance from which observations
            can be from each other while still being in the same
            cluster.
        min_samples, int
            The minimum number of obversations that can be conted
            as a cluster.

    Return:
        tuple
            A tuple of the number of clusters found and the number
            of noise points found, in that order.
    """
    dbscan_object = DBSCAN(eps = eps, min_samples = min_samples)
    cluster_labels = dbscan_object.fit(scaled_dataframe).labels_
    df['cluster'] = cluster_labels

    n_noise = list(cluster_labels).count(-1)
    n_clusters = len(set(cluster_labels)) - (1 if n_noise > 0 else 0)

    return (n_clusters, n_noise)

def generate_skycoord(astro_df):
    """
    Returns an AstroPy SkyCoord object for reference when converting
    between coordinates based on an astronomical dataframe.

    Arguments:
        astro_df, Pandas dataframe
            An astronomical dataframe of astronomical entries,
            including columns on astronomical distance, RA, and dec.

    Returns:
        SkyCoord object,
            A SkyCoord object containing coordinates in all
            relevant astronomical coordinate systems for points
            in the given dataframe.
    """
    coordinate_object = SkyCoord(
        ra = np.array(astro_df['ra']) * u.degree,
        dec = np.array(astro_df['dec']) * u.degree,
        distance = np.array(astro_df['distance']) / u.mas
    )
    return coordinate_object

def generate_cartesian(astro_df):
    """
    Modifies an astronomical dataframe by calculating the
    Cartesian coordinates (x, y, and z) and adding
    this information as additional columns.

    Arguments:
        astro_df, Pandas dataframe
            An astronomical dataframe of astronomical entries,
            including columns on astronomical distance, RA, and dec.

    Returns:
        None
    """
    # create coordinate object
    coords = generate_skycoord(astro_df).cartesian
    # add Cartesian coordinates
    astro_df['x'] = coords.x.value  # x-coordinate in kpc
    astro_df['y'] = coords.y.value  # y-coordinate in kpc
    astro_df['z'] = coords.z.value  # z-coordinate in kpc

    return None

def generate_galactocentric(astro_df):
    """
    Modifies an astronomical dataframe by calculating the
    galactocentric coordinates (longitude and latitude) and adding
    this information as additional columns.

    Arguments:
        astro_df, Pandas dataframe
            An astronomical dataframe of astronomical entries,
            including columns on astronomical distance, RA, and dec.

    Returns:
        None
    """
    # create coordinate object
    galactic_coords = generate_skycoord(astro_df).galactic
    # add galactocentric coordinates
    sampled_df['galactic_l'] = galactic_coords.l.degree  # Galactic longitude in degrees
    sampled_df['galactic_b'] = galactic_coords.b.degree  # Galactic latitude in degrees

    return None



if __name__ == '__main__':
    # define columns to keep
    columns_to_keep = ['ra', 'dec', 'pmra', 'pmdec', 'parallax']
    # read the sampled gaia data, ridding of NaN values
    sampled_df = pd.read_csv('3k_gaia_kin_data.csv', usecols = columns_to_keep).dropna()

    # calculate distances based on parallax
    sampled_df['distance'] = parallax_to_distance(sampled_df['parallax'])

    # clean the data, then scale the data
    del sampled_df['parallax'] # don't use parallax to cluster gorups
    scaled_data = scale_data(sampled_df)

    n_clusters, n_noise = cluster_data(sampled_df, scaled_data, 0.1, 5)
    print(f'Number of clusters found: {n_clusters}')
    print(f'Number of noise points found: {n_noise}')

    # add coordinate transforms to other systems for plotting
    generate_cartesian(sampled_df)
    generate_galactocentric(sampled_df)

    # ============= 2-D PLOT ==========================
    # plot galactocentric coordinates and clusters
    plt.figure(figsize=(10, 8))
    plt.scatter(sampled_df['galactic_l'], sampled_df['galactic_b'],\
                 c=sampled_df['cluster'], cmap='viridis', s=10)
    plt.colorbar(label='Cluster')
    plt.xlabel('Galactic longitude')
    plt.ylabel('Galactic latitude')
    plt.title('Star Clusters Identified by DBSCAN')
    plt.show()

    # ============= 3-D PLOT ==========================
    # calculate marker size (highlight the clusters)
    marker_sizes = np.array([1 if label == -1 else 20 for label in sampled_df['cluster']])

    # plot the cartesian coordinates and clusters
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    # Scatter plot:
    scatter = ax.scatter(
        sampled_df['x'],  # x coordinate (x-axis)
        sampled_df['y'],  # y coordinate (y-axis)
        sampled_df['z'],    # z coordinate (z-axis)
        c=sampled_df['cluster'],   # Color by cluster
        cmap='viridis',            # Color map
        s=marker_sizes,            # Marker size
        alpha=0.8                  # Transparency
    )
    # set axes
    ax.set_xlabel('X Coordinate', fontsize=12)
    ax.set_ylabel('Y Coordinate', fontsize=12)
    ax.set_zlabel('Z Coordinate', fontsize=12)
    ax.set_title('3D Distribution of Stars Colored by Cluster', fontsize=14)

    # Add a color bar to show the cluster mapping
    cbar = plt.colorbar(scatter, ax=ax, pad=0.1)
    cbar.set_label('Cluster', fontsize=12)

    # Show the plot
    plt.show()
