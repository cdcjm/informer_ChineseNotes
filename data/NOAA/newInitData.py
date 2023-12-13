import geopy as geopy
import numpy as np
import pandas as pd

ipath='./267188530.csv'
df_raw = pd.read_csv(ipath,
                     usecols=['BaseDateTime', 'LON', 'LAT', 'SOG', 'COG', 'Heading'])
df_raw = df_raw[['BaseDateTime', 'LON', 'LAT', 'SOG', 'COG', 'Heading']]
df_raw = df_raw.rename(columns={'BaseDateTime': 'date'})

invalid_rows = []
for idx, row in df_raw.iterrows():
    try:
        pd.to_datetime(row['date'])
    except ValueError:
        # print(f"Error at row {idx}: {row['date']}")
        invalid_rows.append(idx)
df_raw.drop(invalid_rows, inplace=True)

df_raw = df_raw.drop_duplicates(subset=['date'])

df_raw['date'] = pd.to_datetime(df_raw['date'])
df_raw.set_index('date', inplace=True)

df_raw.index = pd.to_datetime(df_raw.index)
numeric_cols = ['LON', 'LAT', 'SOG', 'COG', 'Heading']
for col in numeric_cols:
    df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce')
# 使用重采样进行每小时的均匀采样，并使用平均值填充字段数据
resample_dict = {'LON': 'mean', 'LAT': 'mean', 'SOG': 'mean', 'COG': 'mean', 'Heading': 'mean'}
hourly_resampled_data = df_raw.resample('H').agg(resample_dict)

# 打印均匀采样后的数据
print(hourly_resampled_data)
