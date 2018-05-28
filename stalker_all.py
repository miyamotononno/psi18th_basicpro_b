import time
start = time.time()
from bs4 import BeautifulSoup
import urllib.request as req
import urllib.parse as par
from selenium import webdriver

def instagram_all(N):   #N = 目標習得数
      url = "https://www.instagram.com/explore/"
      link = req.urlopen(url)
      browser = webdriver.Chrome('C:\selenium\Chromedriver')   #ChromeDriverをダウンロードして、Chromedriver.exeの存在場所をパスで示す
      browser.get(url)
      
      instagram = []
      count = -1
      for scroll_count in range(1,N):
            time.sleep(2)
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if scroll_count %3 == 0:
                  soup = BeautifulSoup(browser.page_source, 'html.parser')
                  res = soup.findAll('img')
                  for elm in res:
                        instagram.append(elm)
                  print(len(set(instagram)))
                  if count == len(set(instagram)):
                        break
                  if len(set(instagram)) > N:
                        break
                  count = len(set(instagram))

      print('習得件数',len(set(instagram)))
      print('習得時間',time.time() - start)
      print('習得件数（重複含む)',len(instagram))
      print('重複度',(len(instagram)-len(set(instagram)))/len(instagram))

      instagram = list(set(instagram))

      elements = []

      import re

      file = open('instagram.dat','w',encoding='UTF-8',errors = 'replace')
      for i in instagram:
            j = str(i)
            elements.append(j[10:j.find('" class=')])
            file.write(j[10:j.find('" class=')] + '; ')

      file.close()
      browser.close() #ブラウザを閉じる
      return elements

instagram_all(860)