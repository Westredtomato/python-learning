import requests  # 用于发送HTTP请求的库
from lxml import etree  # 用于解析HTML或XML文档的库
import csv  # 用于读写CSV文件的库

# 定义请求头信息，模拟浏览器访问，避免被网站识别为爬虫
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
}

# 功能函数，用来安全地获取列表的第一个元素，当列表为空时返回空格
def get_first_text(list):
    try:
        # 如果列表不为空，则取第一个元素并去除首尾空白字符；否则返回空格
        return list[0].strip() if list else " "
    except Exception as e:
        # 捕获并打印任何可能发生的异常，确保程序不会因单个数据点错误而崩溃
        print(f"Error processing text: {e}")
        return " "

# 获取单页电影数据的函数
def fetch_page_data(url):
    try:
        # 发送GET请求获取页面内容
        res = requests.get(url=url, headers=headers)
        # 检查请求是否成功，如果不是200状态码则抛出异常
        res.raise_for_status()
        # 使用lxml解析HTML文本
        html = etree.HTML(res.text)
        # 使用XPath定位到所有电影条目（<li>标签）
        lis = html.xpath('//*[@id="content"]/div/div[1]/ol/li')
        return lis
    except requests.RequestException as e:
        # 捕获网络请求中的任何异常，并打印错误信息
        print(f"Failed to fetch data from {url}: {e}")
        return []  # 返回空列表表示没有抓取到数据

# 主函数，负责协调整个爬取和保存过程
def main():
    # 生成包含10个分页链接的列表，每个链接指向Top250榜单的不同页面
    urls = ['https://movie.douban.com/top250?start={}&filter='.format(str(i*25)) for i in range(10)]
    all_movies = []  # 用于存储所有电影的数据
    count = 1  # 用于给每部电影编号

    # 遍历每个分页链接，抓取并解析页面内容
    for url in urls:
        print(f"Fetching data from {url}...")  # 打印当前正在处理的URL
        lis = fetch_page_data(url)  # 调用函数获取单页数据
        for li in lis:
            # 使用XPath提取电影的标题、链接、导演、评分、评价人数和简介
            title = get_first_text(li.xpath('./div/div[2]/div[1]/a/span[1]/text()'))
            src = get_first_text(li.xpath('./div/div[2]/div[1]/a/@href'))
            director = get_first_text(li.xpath('./div/div[2]/div[2]/p[1]/text()')).replace('\n', '').replace(' ', '')
            score = get_first_text(li.xpath('./div/div[2]/div[2]/div/span[2]/text()'))
            comment = get_first_text(li.xpath('./div/div[2]/div[2]/div/span[4]/text()'))
            summary = get_first_text(li.xpath('./div/div[2]/div[2]/p[2]/span/text()'))

            # 将提取的数据添加到all_movies列表中
            all_movies.append([count, title, src, director, score, comment, summary])
            count += 1  # 更新电影编号

    # 打开一个CSV文件进行写入，使用'w'模式创建新文件，如果文件已存在则覆盖
    with open('plus_douban_movie_top250.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)  # 创建CSV写入器对象
        # 写入表头，定义CSV文件的列名
        writer.writerow(['No', 'Title', 'Link', 'Director', 'Score', 'Comment', 'Summary'])
        # 批量写入所有电影的数据
        writer.writerows(all_movies)

# 确保main函数只在脚本直接运行时调用，而不是作为模块导入时
if __name__ == "__main__":
    main()
