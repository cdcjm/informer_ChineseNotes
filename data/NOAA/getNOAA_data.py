import requests
from bs4 import BeautifulSoup
import os

# 目标网站 URL
url = 'https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2021/index.html'

# 发送请求并获取网页内容
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 为保存文件创建一个目录
directory = 'downloaded_zips'
if not os.path.exists(directory):
    os.makedirs(directory)

# 提取并下载所有 ZIP 文件
for link in soup.find_all('a'):
    href = link.get('href')
    if href and href.endswith('.zip'):
        download_url = url + '/' + href
        print(f"Downloading {href}...")
        zip_response = requests.get(download_url)
        with open(os.path.join(directory, href), 'wb') as file:
            file.write(zip_response.content)
print("下载完成")
