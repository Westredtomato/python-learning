# Scrapy作业优化版

## 环境配置
1. 安装 Python
本项目使用 Python 编写，确保系统中已经安装 Python 3.6 或更高版本。

2. 安装依赖库
安装 Scrapy、Pandas、Matplotlib 等依赖：

pip install scrapy pandas matplotlib

## 3.执行操作
1. 配置 Scrapy 项目
确保 Scrapy 项目文件夹（douban_spider）结构如下，且每个模块已正确导入。douban_spider.py 文件是爬虫的主体，settings.py 中定义了配置，items.py 定义了存储数据的 Item。

2. 运行爬虫
进入 Scrapy 项目的根目录（包含 scrapy.cfg 的目录），然后通过 Scrapy 命令运行爬虫：

scrapy crawl douban_spider

爬虫会开始抓取豆瓣电影 Top 250 页面，并将每个电影的相关信息保存到 CSV 文件 douban_movie_top250.csv 中。

3. 数据分析
爬虫完成后，可以使用 data_analysis.py 脚本进行数据分析与可视化。此脚本会读取从爬虫中导出的 CSV 文件，计算描述性统计，并生成直方图和箱线图。

运行命令：

python data_analysis.py

## 4. 查看结果

运行完毕后，以下文件将会被生成：

douban_movie_top250.csv：包含爬取的豆瓣Top 250电影信息。
score_histogram.png：电影评分的分布直方图。
score_boxplot.png：电影评分的箱线图。

5. 可视化结果
通过以下命令，您可以查看 score_histogram.png 和 score_boxplot.png 来分析电影评分的分布。