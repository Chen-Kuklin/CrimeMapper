import geopandas as gpd
import pandas as pd
import time
# task 0
# Read the CSV file
df = gpd.read_file('statisticalareas_2020_demography.gdb')
df_crime = pd.read_csv('filter.csv')
# Join the statistical areas map file to crime data
df_final_join = df.merge(df_crime, left_on='YISHUV_STAT11', right_on='StatArea')
# ////////////////////////////////////////////////////////////
# task1 
# ///////////////////////////////////////////////////////
# Group the rows by the yishuv_stat11 and StatisticCrimeGroup columns
# and calculate the sum of the TikimSum column
df_sum = df_final_join.groupby(['YISHUV_STAT11', 'StatisticCrimeGroup'])['TikimSum'].sum().reset_index()
# Rename the column with the sum of TikimSum to tikim_sum
df_sum = df_sum.rename(columns={'TikimSum': 'tikim_sum'})
# ////////////////////////////////////////////////////////////
# task2 
# ///////////////////////////////////////////////////////
#  maximum value of 'tikim_sum' for each 'yishuv_stat11'
miss_namegroup = df_sum.groupby('YISHUV_STAT11')['tikim_sum'].max().reset_index()
# Rename the 'tikim_sum' column to 'tikim_max'
miss_namegroup = miss_namegroup.rename(columns={'tikim_sum': 'tikim_max'})
# Join the 'miss_namegroup' and 'sum_tikim' dataframes
max_tikim=pd.merge(miss_namegroup, df_sum, left_on= ['YISHUV_STAT11', 'tikim_max'],right_on= ['YISHUV_STAT11', 'tikim_sum'], how = 'left')
# Join the 'max_tikim' and 'df' dataframes
to_geojason = df.merge(max_tikim, left_on='YISHUV_STAT11', right_on='YISHUV_STAT11')
# setting the geometry column of the dataframe to be used as the geospatial data
gdf = to_geojason.set_geometry('geometry')
# changing the coordinate reference system of the dataframe
gdf_crs84 = gdf.to_crs(epsg=4326)
# saving the dataframe as a geojson file
gdf_crs84.to_file("enaliza1_geopendes_11.geojson", driver='GeoJSON')







