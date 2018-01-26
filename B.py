# coding:utf-8
import codecs
import csv

import time
import xlwt
import requests
import re
from bs4 import BeautifulSoup
from urllib import parse


def crawl(url):
    html = requests.get(url)
    # print(html.text)
    urls = set()
    soup = BeautifulSoup(html.text, "lxml")
    # print(soup.prettify())
    target = soup.find_all('a', attrs={"href": re.compile(r'^./201')})
    # print(target)
    print(len(target))
    urls.add(parse.urljoin(url,target[0]['href']))
    # for link in target:
    #     # print(parse.urljoin(url, link['href']))
    #     urls.add(parse.urljoin(url, link['href']))
    downloader(urls)


def downloader(urls):
    datas = []

    user_agent = 'Mozilla/6.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    for url in urls:
        # print(url)
        data = {}
        data['url'] = url
        html = requests.get(url, headers)

        # print(html)
        soup = BeautifulSoup(html.text, "lxml")
        title = soup.select('title')[0].get_text()
        data['title'] = title
        # print(type(title))
        # print(title)
        pubtime = soup.select('.pubtime')[0].string.split("：")[1]
        data['pubtime'] = pubtime

        # print( type(pubtime))
        # print(soup.select('pubtime')[0].string.split("：")[1])
        # print(type(pubtime))

        # view = soup.select('#view')
        # print(view)

        content = soup.select('.content')[0].get_text()
        data['content'] = content
        # print(type(content))
        datas.append(data)
    print("*")
    # writeIntoExcel(datas)
    output(datas)
    # writeIntoCsv(datas)
    # testXlwt(datas)


def output(datas):
    fout = codecs.open('a.html', 'w', encoding='utf-8')
    fout.write("<html><head><meta charset='utf-8'/></head><body><table>")
    for data in datas:
        fout.write("<tr>")
        # print(data["url"])
        fout.write("<td>%s</td>" % data['url'])
        fout.write("<td>%s</td>" % data['title'])
        fout.write("<td>%s</td>" % data['pubtime'])
        fout.write("<td>%s</td>" % data["content"])
        fout.write("</tr>")

    fout.write("</table></body></html>")
    fout.close()


def writeIntoExcel(datas):
    myfile = xlwt.Workbook()
    sheet = myfile.add_sheet("sheet1", cell_overwrite_ok=True)
    row = len(datas)
    col = len(datas[0])
    for i in range(0, row):
        for j in range(0, col):
            sheet.write(i, j, datas[i].get(j))
            # print(i)
    myfile.save("filename.xls")

#将list中的内容写入一个新的file文件
def testXlwt(list = []):
    book = xlwt.Workbook() #创建一个Excel
    sheet1 = book.add_sheet('hello') #在其中创建一个名为hello的sheet
    i = 0 #行序号
    for app in list : #遍历list每一行
        j = 0 #列序号
        for x in app : #遍历该行中的每个内容（也就是每一列的）
            sheet1.write(i, j, x) #在新sheet中的第i行第j列写入读取到的x值
            j = j+1 #列号递增
        i = i+1 #行号递增
    # sheet1.write(0,0,'cloudox') #往sheet里第一行第一列写一个数据
    # sheet1.write(1,0,'ox') #往sheet里第二行第一列写一个数据
    book.save("filename.xls") #创建保存文件

def writeIntoCsv(datas):
    writer = csv.writer("a.csv", 'wb')
    writer.writerow(['url', 'title', 'pubtime', 'content'])
    list = []
    for data in datas:
        s = tuple(list(data.values()))
        list.add(s)
    writer.writerows(list)


if __name__ == '__main__':
    start = time.time()
    crawl('http://www.gdofa.gov.cn/ywjx/yw/')
    end = time.time()
    print(end-start)