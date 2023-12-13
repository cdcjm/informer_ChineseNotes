import os
import time
from datetime import datetime
from multiprocessing import Pool
import pandas as pd
import glob
import zipfile
from pathlib import Path


def unzip_files(folder_path):
    """
    解压缩指定文件夹下的所有ZIP文件。

    :param folder_path: 包含ZIP文件的文件夹的路径。
    """
    zip_files = glob.glob(f"{folder_path}/*.zip")
    for zip_file in zip_files:
        print(zip_file)
        tmp = zip_file.replace(".zip", ".csv")
        if os.path.exists(zip_file.replace(".zip", ".csv")):
            continue
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(folder_path)
            print('unzip',folder_path)


def process_file(file_path):
    output_folder = Path('../NOAA/nnnew_ship_csv_files')
    output_folder.mkdir(exist_ok=True)
    chunksize = 10000000  # 根据内存限制调整r


    start_time = time.time()  # 获取当前时间
    for chunk in pd.read_csv(file_path, chunksize=chunksize):
        end_time = time.time()
        print(f"过去了{end_time - start_time}秒")  # 打印循环次数和当前时间
        grouped = chunk.groupby('MMSI')

        print('toShip',file_path)
        for mmsi, group in grouped:
            output_file = output_folder / f"{mmsi}.csv"
            if not output_file.exists():
                group.to_csv(output_file, index=False)
            else:
                group.to_csv(output_file, mode='a', header=False, index=False)


if __name__ == '__main__':
    # 示例用法
    # folder_path = './'  # 设置包含ZIP和CSV文件的文件夹路径
    # unzip_files(folder_path)



    folder_path = './'  # 设置包含CSV文件的文件夹路径


    file_paths = glob.glob(f"{folder_path}/*.csv")
    pool = Pool(processes=16)  # 可以调整进程数量以匹配你的CPU
    pool.map(process_file, file_paths)
    pool.close()
    pool.join()



