# 1.导入模块
import requests  #网络请求模块
from lxml import etree   #数据解析模块

# 2.向对应的网站发起网络请求

#请求头信息，防止反爬虫操作
#右击网页选择检查，选择网络然后刷新，随便点击一个，在标头找到user_agent，复制
headers = {
    'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
}

#功能函数，用来获取列表的第一个元素，当为空时打出空格
def get_first_text(list):
    try:
        return list[0].strip()  # 后面加strip()为了去除两边的空格
    except:
        return " "

#使用列表生成式表示10个页面的地址
#观察每一页的网址，发现规律，遍历爬取每一页的数据
urls = ['https://movie.douban.com/top250?start={}&filter='.format(str(i*25)) for i in range(10)]
count = 1   #用来计数

#遍历每一页
for url in urls:
    print(url)  #获得25个url地址

    res = requests.get(url=url, headers = headers)   #发起请求
    #print(res.status_code)，可以用这个语句检验请求是否成功，成功为200
    html = etree.HTML(res.text)   #将返回的文本加工为可以解析的html
    lis = html.xpath('//*[@id="content"]/div/div[1]/ol/li')   #获取每个电影的li元素
    #print(len(lis))，可以用这个语句来检验，应该是25，表示每一页有25部电影

# 3.解析需要的数据

    #用定位找到并复制xpath
    for li in lis:
        title = get_first_text(li.xpath('./div/div[2]/div[1]/a/span[1]/text()'))  #电影标题
        #删掉//*[@id="content"]/div/div[1]/ol/li[1]，在前面加点表示当前的位置
        src = get_first_text(li.xpath('./div/div[2]/div[1]/a/@href'))   #电影链接
        #解析超链接，a开头
        #删掉//*[@id="content"]/div/div[1]/ol/li[1],用.替代表示当前位置，在后面加上/@href
        director = get_first_text(li.xpath('./div/div[2]/div[2]/p[1]/text()'))   #导演
        #删，加点，结尾加/text()
        score = get_first_text(li.xpath('./div/div[2]/div[2]/div/span[2]/text()'))   #评分
        comment = get_first_text(li.xpath('./div/div[2]/div[2]/div/span[4]/text()'))   #评价人数
        summary = get_first_text(li.xpath('./div/div[2]/div[2]/p[2]/span/text()'))   #简介
        print(count, title, src, director, score, comment, summary)   #输出
        #标题原本保存在一个列表里，用get_first_text改成字符串
        count += 1


# 4.对数据进行处理（将数据存入数据库或者打印）
#保存到 CSV 文件：
import csv

# 打开一个csv文件进行写入
with open('douban_movie_top250.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['No', 'Title', 'Link', 'Director', 'Score', 'Comment', 'Summary'])  # 写入表头

    for url in urls:
        res = requests.get(url=url, headers=headers)  # 发起请求
        html = etree.HTML(res.text)  # 解析HTML
        lis = html.xpath('//*[@id="content"]/div/div[1]/ol/li')  # 获取电影条目

        for li in lis:
            title = get_first_text(li.xpath('./div/div[2]/div[1]/a/span[1]/text()'))
            src = get_first_text(li.xpath('./div/div[2]/div[1]/a/@href'))
            director = get_first_text(li.xpath('./div/div[2]/div[2]/p[1]/text()'))
            score = get_first_text(li.xpath('./div/div[2]/div[2]/div/span[2]/text()'))
            comment = get_first_text(li.xpath('./div/div[2]/div[2]/div/span[4]/text()'))
            summary = get_first_text(li.xpath('./div/div[2]/div[2]/p[2]/span/text()'))

            # 写入电影数据
            writer.writerow([count, title, src, director, score, comment, summary])
            count += 1
