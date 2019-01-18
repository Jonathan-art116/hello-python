import requests
from bs4 import BeautifulSoup
import os

def getHtmlurl(url):         #获取网址
    try:
       r=requests.get(url)
       r.raise_for_status()
       r.encoding=r.apparent_encoding
       return r.text
    except:
        return ""

def getpic(html): #获取图片地址并下载
    soup =BeautifulSoup(html,'html.parser')
    all_img=soup.find('ul',class_='pli').find_all('img')
    for img in all_img:
       src=img['src']
       img_url=src
       print (img_url)
       root='D:/pic/'
       path = root + img_url.split('/')[-1]
       try:                              #创建或判断路径图片是否存在并下载
           if not os.path.exists(root):
               os.mkdir(root)
           if not os.path.exists(path):
               r = requests.get(img_url)
               with open(path, 'wb') as f:
                   f.write(r.content)
                   f.close()
                   print("文件保存成功")
           else:
               print("文件已存在")
       except:
           print("爬取失败")



def main():
    url='http://www.ivsky.com/bizhi/yourname_v39947/'
    html=(getHtmlurl(url))

    print(getpic(html))
main()
