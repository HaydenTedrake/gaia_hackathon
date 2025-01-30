import pandas as pd
from astropy.table import Table

# load the data
# Specify the path to your .fits file
file_path = 'all_w_rv_kin_3k.fits'


tb = Table.read(file_path)
df = tb.to_pandas()


print('done!')




# save the dataframe
df.to_csv('3k_gaia_kin_data.csv', index = False)
