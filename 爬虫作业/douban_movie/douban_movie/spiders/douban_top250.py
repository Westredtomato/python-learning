import scrapy
import csv


class DoubanTop250Spider(scrapy.Spider):
    name = 'douban_top250'
    allowed_domains = ['movie.douban.com']

    # 使用列表生成式构建要爬取的 URL 地址
    start_urls = [
        f'https://movie.douban.com/top250?start={i * 25}&filter=' for i in range(10)
    ]

    count = 1  # 用来计数电影条目的编号

    # 编写 CSV 文件
    def __init__(self, *args, **kwargs):
        super(DoubanTop250Spider, self).__init__(*args, **kwargs)
        self.csv_file = open('douban_movie_top250.csv,utf-8', mode='w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.csv_file)
        self.writer.writerow(['No', 'Title', 'Link', 'Director', 'Score', 'Comment', 'Summary'])  # 写入表头

    def parse(self, response):
        # 获取页面上的所有电影条目
        lis = response.xpath('//*[@id="content"]/div/div[1]/ol/li')

        for li in lis:
            title = self.get_first_text(li.xpath('./div/div[2]/div[1]/a/span[1]/text()'))
            src = self.get_first_text(li.xpath('./div/div[2]/div[1]/a/@href'))
            director = self.get_first_text(li.xpath('./div/div[2]/div[2]/p[1]/text()'))
            score = self.get_first_text(li.xpath('./div/div[2]/div[2]/div/span[2]/text()'))
            comment = self.get_first_text(li.xpath('./div/div[2]/div[2]/div/span[4]/text()'))
            summary = self.get_first_text(li.xpath('./div/div[2]/div[2]/p[2]/span/text()'))

            # 写入数据到 CSV
            self.writer.writerow([self.count, title, src, director, score, comment, summary])
            self.count += 1

    # 辅助函数，用来获取列表的第一个元素，如果为空则返回空字符串
    def get_first_text(self, xpath_result):
        text = xpath_result.get() if xpath_result else ''
        return text.strip() if text else ''

    # 爬虫关闭时调用，用于关闭文件
    def close(self, reason):
        self.csv_file.close()
