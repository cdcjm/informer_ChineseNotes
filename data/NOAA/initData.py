
'''读取CSV'''
import geopy as geopy
import numpy as np
import pandas as pd
# print(ipath)
ipath='./s/316040103.csv'
df_raw = pd.read_csv(ipath,
                     usecols=['BaseDateTime', 'LON', 'LAT', 'SOG', 'COG', 'Heading'])
df_raw = df_raw[['BaseDateTime', 'LON', 'LAT', 'SOG', 'COG', 'Heading']]
df_raw = df_raw.rename(columns={'BaseDateTime': 'date'})
# df_raw = df_raw.drop_duplicates(subset=['LON'])
# df_raw = df_raw.drop_duplicates(subset=['LAT'])
# 删除有空缺值的行
# df_raw.dropna(axis=0,how='any')
# df_raw.dropna(subset=['SOG', 'COG', 'Heading'], how='any', inplace=True)
# df_raw.drop(df_raw.index[(df_raw['Heading'] == 511.0)], inplace=True)
# df_raw.drop(df_raw.index[(df_raw['SOG'] == 0.0)], inplace=True)
df_raw = df_raw.reset_index(drop=True)

df_raw.to_csv('./s/SHIP.csv', index=False)

last_24_rows = df_raw.tail(24)
last_24_rows.to_excel('../../TrueValue/SHIP.xlsx', index=False, sheet_name='Sheet1')

#
# if len(df_raw) > all_len:
#     '''2。计算出两两数据间时间差值（找出大于1小时的），根据encoder列筛选数据'''
#     '''
#     df_raw.columns: ['date', ...(other features), target feature]
#     '''
#     # cols = list(df_raw.columns);
#     if self.cols:
#         cols = self.cols.copy()
#         cols.remove(self.target)
#     else:
#         cols = list(df_raw.columns)
#         cols.remove(self.target)
#         cols.remove('BaseDateTime')
#     df_raw = df_raw[['BaseDateTime'] + cols + [self.target]]
#     df = df_raw
#     df['BaseDateTime'] = pd.to_datetime(df_raw['BaseDateTime'])
#
#     # 清理异常速度
#     window = 2
#     # df['speed'] = rolling_apply(self.compute_distance, window, df['LON'].values, df['LAT'].values)
#     lat_diff = df["LAT"].rolling(window=2)
#     lon_diff = df["LON"].rolling(window=2)
#     dists = []
#     for lat, lon in zip(lat_diff, lon_diff):
#         if len(lon) == 1:
#             dists.append(np.nan)
#         else:
#             coord1 = (lat.iloc[0], lon.iloc[0])
#             coord2 = (lat.iloc[1], lon.iloc[1])
#             dist = geopy.distance.geodesic(coord1, coord2).km
#             dists.append(dist)
#     df['timeh'] = df_raw['BaseDateTime'].apply(lambda x: x.strftime('%Y-%m-%dT%H:%M:%S')).apply(str2timeh)
#     df["speed"] = dists / df['timeh'].diff()
#     df = df[df['speed'] < 20]
#     del df["speed"]
#     df = df.reset_index(drop=True)
#
#     df["hour"] = df['BaseDateTime'].apply(lambda x: x.hour)
#     df["minute"] = df['BaseDateTime'].apply(lambda x: x.minute)
#     df["minute"] = (df["minute"] / INTER_TIME).astype(int)
#     df["day"] = df['BaseDateTime'].apply(lambda x: x.dayofyear)
#     # 更改间隔hour，day都要改，按照初始值15分钟一个点，一小时4个，一天24*4
#     df["hour"] = df["minute"] + df["hour"] * (60 / INTER_TIME) + df["day"] * 24 * (60 / INTER_TIME)
#     df.drop_duplicates(subset=['hour'], keep='first', inplace=True)
#     df = df.reset_index(drop=True)
#     df['timediffer'] = df["hour"].diff()
#     # df['timediffer'][0] = 3.0
#     # df['timediffer'][-1] = 3.0
#     del df["hour"]
#     del df["day"]
#     del df["minute"]
#     # del df['timediffer']
#     df_raw = df.copy(deep=True)
#     del df_raw['timediffer']
#     df_timeh = df_raw['timeh'].values
#     del df_raw['timeh']
#
#     if self.features == 'M' or self.features == 'MS':
#         cols_data = df_raw.columns[1:]
#         df_data = df_raw[cols_data]
#     elif self.features == 'S':
#         df_data = df_raw[[self.target]]
#
#     part_index_ = df[df['timediffer'] > 2].index.tolist()
#     part_index = []
#
#     '''3。数据归一化、数据拆分'''
#     for i in range(1, len(part_index_)):
#         if (part_index_[i] - part_index_[i - 1]) > all_len + 1:
#             part_index.append([part_index_[i - 1], part_index_[i]])
#     if len(part_index) > 0:
#         df_data = df_data.values
#         df_stamp = df_raw[['BaseDateTime']]
#         data_stamp = time_features(df_stamp, timeenc=self.timeenc, freq=self.freq)
#
#         for i in range(len(part_index)):
#             # start = int(part_index[i][0] + 1)
#             start = part_index[i][0]
#             # if part_index[i]-start>self.seq_len:
#             end = start + all_len + 1
#             while (end < part_index[i][1]):
#                 if len(data_all) == 0:
#                     data_all = [df_data[start:end, :]]
#                     stamp_all = [data_stamp[start:end]]
#                     time_real = [df_timeh[start:end]]
#                 else:
#                     data_all.append(df_data[start:end, :])
#                     stamp_all.append(data_stamp[start:end])
#                     time_real.append(df_timeh[start:end])
#                 '''此处更改间隔'''
#                 start = start + 2
#                 # start = start + all_len
#                 end = start + all_len + 1
#             #     data_all = [df_data[start:part_index[i][1], :]]
#             #     stamp_all = [data_stamp[start:part_index[i][1]]]
#             #     # if self.prob_use == True:
#             #     #     # data_map_all = [df_data[(start - 1):part_index[i][1], :]]
#             #     #     data_map_all = [df_data[start:part_index[i][1], :]]
#             # else:
#             #     data_all.append(df_data[start:part_index[i][1], :])
#             #     stamp_all.append(data_stamp[start:part_index[i][1]])
#             #     # if self.prob_use == True:
#             #     #     # data_map_all.append(df_data[(start - 1):part_index[i][1], :])
#             #     #     data_map_all.append(df_data[start:part_index[i][1], :])
# # self.draw_data(data_all)
# random.shuffle(data_all_x)