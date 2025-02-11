import scrapy
import csv
from ..items import NewDoubanMovieItem  # 导入新定义的 Item 类

class DoubanSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['movie.douban.com']

    # 设置爬取的每页 URL
    start_urls = [f'https://movie.douban.com/top250?start={i * 25}&filter=' for i in range(10)]

    def __init__(self, *args, **kwargs):
        super(DoubanSpider, self).__init__(*args, **kwargs)
        self.count = 1  # 从 1 开始计数
        # 打开 CSV 文件进行写入
        self.csv_file = open('douban_movie_top250.csv,utf-8', mode='w', newline='', encoding='utf-8')
        self.writer = csv.writer(self.csv_file)
        # 写入表头
        self.writer.writerow(['No', 'Title', 'Link', 'Director', 'Score', 'Comment', 'Summary'])

    def parse(self, response):
        # 获取页面上的所有电影条目
        lis = response.xpath('//*[@id="content"]/div/div[1]/ol/li')

        for li in lis:
            item = NewDoubanMovieItem()  # 创建新的 Item 实例

            # 提取电影信息
            item['no'] = self.count
            item['title'] = self.get_first_text(li.xpath('./div/div[2]/div[1]/a/span[1]/text()'))
            item['link'] = self.get_first_text(li.xpath('./div/div[2]/div[1]/a/@href'))
            item['director'] = self.get_first_text(li.xpath('./div/div[2]/div[2]/p[1]/text()'))
            item['score'] = self.get_first_text(li.xpath('./div/div[2]/div[2]/div/span[2]/text()'))
            item['comment'] = self.get_first_text(li.xpath('./div/div[2]/div[2]/div/span[4]/text()'))
            item['summary'] = self.get_first_text(li.xpath('./div/div[2]/div[2]/p[2]/span/text()'))

            # 写入数据到 CSV
            self.writer.writerow([
                item['no'], item['title'], item['link'], item['director'],
                item['score'], item['comment'], item['summary']
            ])

            self.count += 1  # 计数器自增

        # 如果有下一页，继续爬取
        next_page = response.xpath('//span[@class="next"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def get_first_text(self, xpath_result):
        # 获取 xpath 查询的第一个文本内容
        text = xpath_result.get() if xpath_result else ''
        return text.strip() if text else ''

    def close(self, reason):
        # 爬虫结束时关闭文件
        self.csv_file.close()
