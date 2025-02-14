## README
# 作业二：利用scrapy框架爬取豆瓣top250电影信息

### 1. 运行环境配置

操作系统：适用于 Windows、Linux 和 macOS。

安装 Python：本项目需要 Python 3.6 及以上版本。

安装 Scrapy：在命令行中运行以下命令来安装 Scrapy：

pip install scrapy

### 2. 项目文件说明

douban_top250.py：Scrapy 爬虫脚本，负责抓取豆瓣电影 Top 250 页面的数据（电影名、导演、评分、评论数、简介等信息）。

settings.py：Scrapy 配置文件，用于设置如 User-Agent、下载延时等配置，以便避开反爬虫机制。

douban_movie_top250.csv：最终存储抓取数据的 CSV 文件。

### 3. 启动爬虫

完成上述配置后，可以按照以下步骤启动爬虫：

在终端中进入项目根目录（包含 scrapy.cfg 文件的目录）。

运行以下命令启动爬虫：

scrapy crawl douban_top250

爬虫启动后，Scrapy 会抓取豆瓣电影 Top 250 页面的数据，数据会存储在 douban_movie_top250.csv 文件中。

如果关联excel软件时出现乱码，可以把后缀.csv改成.csv,utf-8，这样就可以在pycharm中打开查看爬取的电影信息

### 4. 查看输出结果

爬虫运行时，电影的数据将会保存在 douban_movie_top250.csv 文件中。文件的格式如下：

No,Title,Link,Director,Score,Comment,Summary
1,电影名称,http://movie.douban.com/xxx,导演名称,9.5,20000,简介信息
2,电影名称,http://movie.douban.com/xxx,导演名称,9.3,15000,简介信息
...