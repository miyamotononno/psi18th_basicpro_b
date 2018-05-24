from bs4 import BeautifulSoup
import urllib.request as req
from selenium import webdriver

url = "https://www.instagram.com/explore/tags/%E5%8F%8B%E9%81%94/"
link = req.urlopen(url)
# us_data = req.urlopen(url)
# print(us_data.read().decode('utf-8'))

soup = BeautifulSoup(link, "html.parser")

# 任意のデータを抽出
res1 = soup.find("body")
res2 = res1.find("span")
print(res1)


