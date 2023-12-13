import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from datetime import datetime

# 示例数据（请替换为你的实际数据）

data = pd.read_csv("./s/SHIP.csv")

df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# 将日期转换为数值（例如，从开始日期的秒数）
df['timestamp'] = (df['date'] - df['date'].min()).dt.total_seconds()


# 移除重复的timestamp
df = df.drop_duplicates(subset='timestamp')

# 确保数据按照timestamp排序
df = df.sort_values(by='timestamp')
# 创建三次样条插值函数
lat_interp = interp1d(df['timestamp'], df['LAT'], kind='cubic')
lon_interp = interp1d(df['timestamp'], df['LON'], kind='cubic')
sog_interp = interp1d(df['timestamp'], df['SOG'], kind='cubic')
cog_interp = interp1d(df['timestamp'], df['COG'], kind='cubic')
heading_interp = interp1d(df['timestamp'], df['Heading'], kind='cubic')

# 创建新的时间戳以进行插值
# 例如，每1h一个时间点
new_timestamps = np.arange(df['timestamp'].min(), df['timestamp'].max(), 3600)

# 执行插值
new_lat = lat_interp(new_timestamps)
new_lon = lon_interp(new_timestamps)
new_sog = sog_interp(new_timestamps)
new_cog = cog_interp(new_timestamps)
new_heading = heading_interp(new_timestamps)

# 将时间戳转换回日期
new_dates = [df['date'].min() + pd.Timedelta(seconds=ts) for ts in new_timestamps]

# 创建新的DataFrame
interpolated_df = pd.DataFrame({
    'date': new_dates,
    'LAT': new_lat,
    'LON': new_lon,
    'SOG': new_sog,
    'COG': new_cog,
    'Heading': new_heading
})

print(interpolated_df)

# 保存插值后的数据到CSV文件
interpolated_df.to_csv('inSHIP.csv', index=False)
last_24_rows = interpolated_df.tail(24)
last_24_rows.to_excel('../../TrueValue/SHIP.xlsx', index=False, sheet_name='Sheet1')


# 绘图
# 定义一个函数来绘制每个字段的比较
def plot_comparison(original_df, interpolated_df, field, title, color):
    plt.figure(figsize=(10, 4))
    plt.scatter(original_df['date'], original_df[field], color=color, label='Original')
    plt.plot(interpolated_df['date'], interpolated_df[field], color=color, linestyle='dashed', label='Interpolated')
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(field)
    plt.legend()
    plt.gcf().autofmt_xdate()  # 优化日期格式显示
    plt.show()

# 绘制LAT字段的比较
plot_comparison(df, interpolated_df, 'LAT', 'LAT Comparison', 'red')

# 绘制LON字段的比较
plot_comparison(df, interpolated_df, 'LON', 'LON Comparison', 'blue')

# 绘制SOG字段的比较
plot_comparison(df, interpolated_df, 'SOG', 'SOG Comparison', 'green')

# 绘制COG字段的比较
plot_comparison(df, interpolated_df, 'COG', 'COG Comparison', 'purple')

# 绘制Heading字段的比较
plot_comparison(df, interpolated_df, 'Heading', 'Heading Comparison', 'orange')
# 添加图例
plt.legend()

# 设置标题和轴标签
plt.title('Interpolated Ship Trajectory Data')
plt.xlabel('Date')
plt.ylabel('Values')

# 优化日期格式显示
plt.gcf().autofmt_xdate()

# 显示图表
plt.show()