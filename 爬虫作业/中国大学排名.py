############################
#univorder-20121122.py
#
#https://blog.csdn.net/m0_48405781/article/details/106921993

from bs4 import BeautifulSoup  # 网页解析  获取数据
import re  # 正则表达式 进行文字匹配
import urllib.request, urllib.error  # 制定url 获取网页数据
import xlwt



'''
从网页上获取网页内容，并进行异常处理
'''
def askURL(url):
    # 我的初始访问user agent
    head = {  # 模拟浏览器头部信息，向豆瓣服务器发送消息 伪装用的
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36"
    }
    # 用户代理表示告诉豆瓣服务器我们是什么类型的机器--浏览器  本质是告诉浏览器我们可以接受什么水平的文件内容
    request = urllib.request.Request(url, headers=head)  # 携带头部信息访问url
    # 用request对象访问
    html = ""
    try:
        response = urllib.request.urlopen(request)  # 用urlopen传递封装好的request对象
        html = response.read().decode("utf-8")  # read 读取 可以解码 防治乱码
        # print(html)
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)  # 打印错误代码
        if hasattr(e, "reason"):
            print(e.reason)  # 打印错误原因
    return html

'''
http://m.gaosan.com/gaokao/265440.html
通过观察源代码，
可以发现每个大学排名的数据信息被封装在一个<tr></tr>之间的结构中。
这是HTML 语言表示表格中一行的标签，在这行中，每列内容采用<td></td>表示。
以“清华大学”为例，它对应一行信息的HTML 代码如下：
<tr>
<td>2</td><td>清华大学</td><td>98.78</td><td>8★</td><td>世界一流大学</td>
</tr>
'''



# 正则表达式
# 创建超链接正则表达式对象，表示字符串模式，规则
paiming = re.compile(r'<td>(.*)</td><td>.*</td><td>.*</td><td>.*</td><td>.*</td>')
xuexiao = re.compile(r'<td>.*</td><td>(.*)</td><td>.*</td><td>.*</td><td>.*</td>')
defen   = re.compile(r'<td>.*</td><td>.*</td><td>(.*)</td><td>.*</td><td>.*</td>')
xingji  = re.compile(r'<td>.*</td><td>.*</td><td>.*</td><td>(.*)</td><td>.*</td>')
cengci  = re.compile(r'<td>.*</td><td>.*</td><td>.*</td><td>.*</td><td>(.*)</td>')


'''
爬取网页
这个代码中每个td 标签包含大学排名表格的一个列数值，与表头一一对应。
因此，如果要获得其中的数据，需要首先找到<tr></tr>标签，并遍历其中每个<td></td>标签，
获取其值写入程序的数据结构中，这个代码封装成函数表示如下
'''
def getData(html):
#def getData(baseurl):
    datalist = []
    #html = askURL(baseurl)  # 保存获取到的网页源码
    # print(html)
    #【逐一】解析数据  （一个网页就解析一次）
    soup = BeautifulSoup(html, "html.parser")  # soup是解析后的树形结构对象
    for item in soup.find_all('tr'):  # 查找符合要求的字符串形成列表
        # print(item)    #测试查看item全部
        data = []  # 保存一个学校的所有信息
        item = str(item)
        #排名
        paiming1 = re.findall(paiming, item)  # re正则表达式查找指定字符串 0表示只要第一个 前面是标准后面是找的范围
        # print(paiming1)
        if(not paiming1):
            pass
        else:
            print(paiming1[0])
            data.append(paiming1)
        if(paiming1 in data):
            #学校名字
            xuexiao1 = re.findall(xuexiao, item)[0]
            # print(xuexiao1)
            data.append(xuexiao1)
            #得分
            defen1 = re.findall(defen, item)[0]
            # print(defen1)
            data.append(defen1)
            #星级
            xingji1 = re.findall(xingji, item)[0]
            # print(xingji1)
            data.append(xingji1)
            #层次
            cengci1 = re.findall(cengci, item)[0]
            # print(cengci1)
            data.append(cengci1)
            # print('-'*80)
        datalist.append(data)  # 把处理好的一个学校信息放入datalist中
    return datalist




'''
保存数据
得到处理好的数据之后，我们可以将数据保存到excel表中，这时候就需要用到 xlwt库中的方法，
将数据按 '名次', '学校名称', '综合得分', '星级排名', '办学层次'的顺序打印到excel表中，
将此代码封装成函数如下:
'''
def saveData(datalist, savepath):
    book = xlwt.Workbook(encoding="utf-8", style_compression=0)  # 创建workbook对象   样式压缩效果
    sheet = book.add_sheet('中国大学排名', cell_overwrite_ok=True)  # 创建工作表  一个表单  cell覆盖
    for i in range(0, 640):
        print("第%d条" % (i + 1))
        data = datalist[i]
        # print(data)
        for j in range(0, 5):  # 每一行数据保存进去
            sheet.write(i , j, data[j])  # 数据
    book.save(savepath)  # 保存数据表


'''
最终在main()方法中调用这些方法，运行即可：
'''
def main():
    baseurl = "http://m.gaosan.com/gaokao/265440.html"
    # 1爬取网页
    html = askURL(baseurl)
    datalist = getData(html)
    savepath = "中国大学排名2.xls"
    saveData(datalist,savepath)


#主函数
if __name__ == "__main__":  # 当程序执行时
    # #调用函数     程序执行入口
    main()
    # init_db("movietest.db")
    print("爬取完毕！")
