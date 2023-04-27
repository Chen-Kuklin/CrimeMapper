import geopandas as gpd
import pandas as pd
import time
# Read the GeoJSON file
police_stations = gpd.read_file('PoliceStationBoundaries.geojson')
# Read the CSV file
df_crime = pd.read_csv('filter.csv')
# Read the gdb formet
gdb_2020=gpd.read_file('statisticalareas_2020_demography.gdb')
# join 2020 whith crime
df_final_join = gdb_2020.merge(df_crime, left_on='YISHUV_STAT11', right_on='StatArea')
# creates a GeoDataFrame from the "police_stations" dataframe and sets the column 'geometry' as the geometry column
gdf_police_stations = gpd.GeoDataFrame(police_stations, geometry='geometry')
# reates a new column in the gdb_2020 dataframe named 'centroid_column' and sets it equal to the centroid of each feature in the gdb_2020 dataframe
gdb_2020['centroid_column'] = gdb_2020.centroid
# sets the 'centroid_column' as the geometry column for the gdb_2020 dataframe
gdb_2020 = gdb_2020.set_geometry('centroid_column')
# re-projects the gdf_police_stations dataframe to the coordinate reference system of the gdb_2020 dataframe
df_crs = gdf_police_stations.crs
gdb_2020_crs = gdb_2020.crs
df_reprojected = gdf_police_stations.to_crs(gdb_2020_crs)
# joins the two dataframes
police_for_stt=gpd.sjoin(df_reprojected,gdb_2020,how='left',op="contains") 
# join  whith crime
result= df_crime.merge(police_for_stt, left_on='StatArea', right_on='YISHUV_STAT11')
# task1
# ///////////////////////////////////////////////////////
# Group the rows by the yishuv_stat11 and StatisticCrimeGroup columns
# and calculate the sum of the TikimSum column
df_sum = result.groupby(['tahananame', 'StatisticCrimeGroup'])['TikimSum'].sum().reset_index()
#  # Rename the column with the sum of TikimSum to tikim_sum
df_sum = df_sum.rename(columns={'TikimSum': 'tikim_sum'})
start_time=time.time()
# task2 
# ///////////////////////////////////////////////////////
miss_namegroup = df_sum.groupby('tahananame')['tikim_sum'].max().reset_index()
# Rename the 'tikim_sum' column to 'tikim_max'
miss_namegroup = miss_namegroup.rename(columns={'tikim_sum': 'tikim_max'})
# Join the 'miss_namegroup' and 'sum_tikim' dataframes using geopandas.merge()
max_tikim=pd.merge(miss_namegroup, df_sum, left_on= ['tahananame', 'tikim_max'],right_on= ['tahananame', 'tikim_sum'], how = 'left')
# joins the two dataframes
to_geojason = gdf_police_stations.merge(max_tikim, left_on='tahananame', right_on='tahananame')
# export to geojason file
to_geojason.to_file("analiza2_geopwndes.geojson", driver='GeoJSON')
# print("------% s-----" %(time.time() - start_time) )












