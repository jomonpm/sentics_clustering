
import os
import csv
import pandas as pd
import math



df = pd.read_csv("/home/jomon/Downloads/test_Data(2).csv")

df_filtered = df[df['unique_id'] != 0]
df_filtered.to_csv('filtered_data.csv', index=False)

file_path = 'new_file.csv'

with open(file_path, 'w') as file:
    pass


timestamp_unique = df_filtered['timestamp_id'].unique()
unique_id_unique = df_filtered['unique_id'].unique()

cluster = []
fill_up= []
position_dict= {}

for unique_time in timestamp_unique:
    for index, row in df_filtered[df_filtered['timestamp_id'] == unique_time].iterrows():
        for unique_id in unique_id_unique:
            if df_filtered.loc[index, 'unique_id'] == unique_id:
                position_tuple = (row['x_position'], row['y_position'],unique_time,row["sensor_id"])
                position_dict[index] = position_tuple
        mean_x = sum(position[0] for position in position_dict.values()) / len(position_dict)
        mean_y = sum(position[1] for position in position_dict.values()) / len(position_dict)
                
        if math.sqrt((row['x_position']- mean_x)**2 + (row['y_position']- mean_y)**2) <=2:
            fill_up.append([unique_time, unique_id])
            cluster.append([row['x_position'], row['y_position'], row['sensor_id']])       

new_df = pd.DataFrame({
    'f_timestamp': [row[0] for row in fill_up],
    'f_id': [row[1] for row in fill_up],
    'cluster_data' : [sublist[0] for sublist in cluster]})
new_df.to_csv(file_path, index=False)