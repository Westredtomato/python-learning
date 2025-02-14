import csv
import requests
from bs4 import BeautifulSoup
import time  # 导入time模块，用于模拟请求间的延迟

def main():
    """
    主函数，负责启动爬取过程，获取网页内容并保存数据
    """
    url = "http://www.hkclzjt.cn/groceries/index"  # 目标网页链接
    save_path = "菜价.csv,utf-8"  # 存储数据的文件路径

    # 请求网页并获取 HTML 内容
    html = askURL(url)

    if html:
        # 提取数据
        datalist = getData(html)
        if datalist:
            # 如果提取到了数据，则保存到 CSV 文件中
            saveData(datalist, save_path)
        else:
            print("未能提取到任何数据")
    else:
        print("网页内容获取失败")

def askURL(url):
    """
    获取指定URL的网页内容
    :param url: 网页链接
    :return: 返回页面的 HTML 内容
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        # 向网页发送 GET 请求，获取网页响应
        response = requests.get(url, headers=headers)

        # 检查响应状态码是否为 200，若不是则抛出异常
        response.raise_for_status()

        # 设置编码方式，防止乱码
        response.encoding = response.apparent_encoding

        # 返回页面的 HTML 内容
        return response.text
    except requests.RequestException as e:
        # 请求失败时，打印错误信息
        print(f"请求网页时发生错误: {e}")
        return None  # 如果请求失败，返回 None

def getData(html):
    """
    从网页 HTML 内容中提取所需数据
    :param html: 网页的 HTML 内容
    :return: 返回一个列表，包含提取的数据
    """
    # 使用 BeautifulSoup 解析 HTML 内容
    soup = BeautifulSoup(html, "html.parser")

    # 找到包含数据的 div 元素
    div = soup.find("div", attrs={"class": "row"})
    if not div:
        print("未找到目标 div 元素")
        return []  # 如果未找到目标 div，返回空列表

    # 在 div 元素内找到 table 标签
    table = div.find("table")
    if not table:
        print("未找到表格")
        return []  # 如果未找到表格，返回空列表

    # 获取表格中的所有行（跳过表头，从第二行开始）
    trs = table.find_all("tr")[1:]

    datalist = []  # 用来存储提取的数据
    for tr in trs:
        # 获取当前行的所有单元格（td标签）
        tds = tr.find_all("td")

        # 如果当前行的单元格数目大于等于3，表示数据完整
        if len(tds) >= 3:
            data = tds[0].text.strip()  # 获取日期
            name = tds[1].text.strip()  # 获取名称
            price = tds[2].text.strip()  # 获取价格
            datalist.append([data, name, price])  # 将数据添加到列表中

    return datalist  # 返回所有提取到的数据

def saveData(datalist, savepath):
    """
    将提取的数据保存到 CSV 文件中
    :param datalist: 要保存的数据列表
    :param savepath: 保存文件的路径
    """
    try:
        # 打开 CSV 文件并准备写入数据
        with open(savepath, mode="w", newline='', encoding="utf-8") as f:
            csv_writer = csv.writer(f)

            # 写入标题行
            csv_writer.writerow(["日期", "名称", "价格"])

            # 写入数据行
            csv_writer.writerows(datalist)

        print(f"数据已保存到 {savepath}")
    except Exception as e:
        # 如果保存文件时出现错误，打印异常信息
        print(f"保存数据时发生错误: {e}")

# 运行程序
if __name__ == "__main__":
    # 调用主函数，启动爬取和保存过程
    main()
    print("爬取完毕")
