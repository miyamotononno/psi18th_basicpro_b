from bs4 import BeautifulSoup
import urllib.request as req
from selenium import webdriver
import time

url = "https://www.instagram.com/explore/tags/%E5%8F%8B%E9%81%94/"
link = req.urlopen(url)

browser = webdriver.Chrome('C:\selenium\chromedriver')
browser.get(url)
scroll_count = 0

for i in range(0,10):
   if scroll_count == 0:
      time.sleep(1)
   browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#ブラウザを閉じる

soup = BeautifulSoup(browser.page_source, 'html.parser')
res1 = soup.findAll('img')
for elm in res1:
   print(elm['alt'])
print(len(res1))

browser.close()
