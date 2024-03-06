from selenium import webdriver  # 拟人爬取数据模块
from bs4 import BeautifulSoup  # 基于selenium模块获取到的数据解析工具
from tqdm import tqdm  # 进度条模块
from selenium.webdriver.common.by import By  # 控制浏览器模拟鼠标动作模块
from selenium.webdriver.edge.service import Service  # selenium模块启动edge浏览器服务
import time  # 时间模块
import re  # 正则表达式模块
from selenium.webdriver.common.action_chains import ActionChains
import csv  # csv模块


def getCommentsAndWrite(href):
    edgedriver = Service('msedgedriver.exe')  # 调用edge浏览器驱动程序
    edgedriver.start()  # 打开浏览器
    browers = webdriver.Remote(edgedriver.service_url)
    file = open('网易云音乐评论1.csv', mode='w', encoding='utf-8')

    browers.get(href)
    time.sleep(2)
    # 数据解析
    page_source = browers.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    # 查找iframe元素
    iframe = browers.find_element(By.NAME, 'contentFrame')
    # 切换到iframe中
    browers.switch_to.frame(iframe)
    givenButton = browers.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div/div[2]/div/div[2]/div[3]/div/a[9]')
    for i in tqdm(range(0, 3392), desc="点击进度", colour='green'):
        givenButton.click()
        time.sleep(1)
    time.sleep(10)
    # 获取完当页评论后，点击下一页，使用while循环，直到没有下一页
    while True:
        time.sleep(3)
        # 数据选择丨数据预处理
        # 整个评论区域
        # 用selector定位到评论区域
        div0 = browers.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div/div[2]/div/div[2]/div[2]')
        div0BS = BeautifulSoup(div0.get_attribute('innerHTML'), 'html.parser')
        div1 = div0BS.find_all('div', attrs={'class': 'itm'})
        # 当页评论
        for item in div1:
            div2 = item.find('div', attrs={'class': 'cnt f-brk'}).get_text()
            # 将div2的内容从第一个冒号开始截取
            div2 = div2.split('：')[1]
            # 将div2中的&nbsp;替换为空格
            div2 = div2.replace('&nbsp;', ' ')
            # 将div2的内容写入csv文件
            file.write(div2 + '\n')
        # 使用By模块定位链接文字“下一页”
        nextPage = browers.find_element(By.LINK_TEXT, '下一页')
        ActionChains(browers).move_to_element(nextPage).click().perform()
        # 判断是否有下一页，如果没有下一页，跳出循环
        next_button_class = browers.find_element(By.LINK_TEXT, '下一页').get_attribute('class')
        if re.match(r'zbtn\s+znxt.+.+js-disabled', next_button_class):
            break
        else:
            continue
    file.close()


def dataProcessing():
    # 读取评论
    commentsFile = open("O:\\北京石油化工学院\\2023春\\文本分析与大数据可视化\\data\\ChengDu.csv", mode="r",
                        encoding="UTF8")
    commentsList = commentsFile.readlines()
    commentsFile.close()

    resultFile = open("O:\\北京石油化工学院\\2023春\\文本分析与大数据可视化\\data\\ChengDu（Pro）.csv", mode="w",
                      encoding="UTF8")

    for comments in tqdm(commentsList, desc="数据清洗进度", colour="green"):
        # 空行处理
        if comments == "\n":
            pass
        # 正常评论处理
        else:
            # 过滤 方括号表情
            brackets_pattern = re.compile(r'\[.*?]')  # 匹配方括号及其中的内容
            comments = brackets_pattern.sub('', comments)
            # 匹配中文字符，取出中文（过滤emoji表情）
            pattern = re.compile(r'[^\u4e00-\u9fa5]')  # 匹配所有非中文字符
            comments = pattern.sub('', comments)
            if comments == "":
                pass
            else:
                resultFile.write(comments + "\n")


def concatCSV():
    # 打开第一个CSV文件并读取其中的所有数据
    with open('data/ChengDu1.csv', 'r', encoding="UTF8") as file1:
        csv_reader = csv.reader(file1)
        data1 = list(csv_reader)

    # 打开第二个CSV文件并读取其中的所有数据，并进行倒序操作
    with open('data/ChengDu2.csv', 'r', encoding="UTF8") as file2:
        csv_reader = csv.reader(file2)
        data2 = list(csv_reader)[::-1]

    # 将第二个CSV文件的数据倒序添加到第一个CSV文件的数据之后
    data = data1 + data2

    # 将新的数据写入一个新的CSV文件，或将其覆盖现有的第一个CSV文件
    with open('data/ChengDu.csv', 'w', newline='', encoding="UTF8") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerows(data)


def main():
    startTime = time.time()  # 记录数据采集开始时间
    print("数据采集开始——————————")
    getCommentsAndWrite('https://music.163.com/#/song?id=436514312')
    endTime = time.time()  # 记录数据采集结束时间
    print("数据采集结束——————————")
    print("数据采集总耗时：{:.2f}秒".format(endTime - startTime))
    startTime = time.time()  # 记录数据清洗开始时间
    print("数据清洗开始——————————")
    dataProcessing()
    endTime = time.time()  # 记录数据清洗结束时间
    print("数据清洗结束——————————")
    print("数据清洗总耗时：{:.2f}秒".format(endTime - startTime))
    startTime = time.time()  # 记录数据合并开始时间
    print("数据合并开始——————————")
    concatCSV()
    endTime = time.time()  # 记录数据合并结束时间
    print("数据合并结束——————————")
    print("数据合并总耗时：{:.2f}秒".format(endTime - startTime))


if __name__ == '__main__':
    main()
