
# coding: utf-8
import traceback
from MsSql import ToMsSql
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from scrapy import Selector
import time
import re
import os
import logging
import pandas

class YaoJingCai:

    def __int__(self, name, password, excelname, loginUrl, url, PageNumber):
        self._name = name
        self._password = password
        self._excelName = excelname
        self._login = loginUrl
        self._url = url
        self._PageNumber = PageNumber

    def Login(self):
        browser = webdriver.Firefox(executable_path=r"{}\driver\geckodriver.exe".format(os.path.abspath('.')))
        browser.get(self._login)
        time.sleep(3)
        browser.refresh()
        time.sleep(5)
        iframe = browser.find_element_by_xpath('/html/body/div[2]/div/div/div/iframe')
        browser.switch_to.frame(iframe)
        browser.find_element_by_name("loginname").clear()
        browser.find_element_by_name("loginname").send_keys(self._name)
        time.sleep(2)
        browser.find_element_by_name("nloginpwd").clear()
        browser.find_element_by_name("nloginpwd").send_keys(self._password)
        time.sleep(2)
        browser.find_element_by_id('paipaiLoginSubmit').click()
        time.sleep(10)
        return browser

    @staticmethod
    def ToCsv(YaoPinName:list):
        datafrname = pandas.DataFrame(
            {
            'Info': [y for y in YaoPinName]
        })
        datafrname.to_csv("{}DerKang.csv".format(os.path.join(os.path.expanduser("~"), 'Desktop') + '\\'), header=False, mode='a')
    def Log(self):
        logger = logging.getLogger(self._excelName)
        logger.setLevel(level=logging.INFO)
        handler = logging.FileHandler(r"logs\log.txt")
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def StartCrawl(self):
        log = self.Log()
        option = Options()
        option.add_argument('--headless')
        browser = self.Login()
        for i in range(71, int(self._PageNumber) + 1):
            log.info("第 {} 次迭代页数".format(i))
            MaxPage = []
            browser.get(self._url.format(i))
            time.sleep(15)
            html = browser.page_source
            selector = Selector(text=html)
            # 取得 div 最大块数
            for item in selector.xpath('//html//div[contains(@class,"clearfix mr-15")]'):
                for i in item.re('(index="\w+">?)'):
                   MaxPage.append(int(i.replace('index="', '').replace('">', '')))
                    ## 开始迭代元素
            for a in range(1, max(MaxPage) + 2):
                log.info("第 {} 次迭代元素".format(a))
                YaoPinName = list()
                for item in selector.xpath("/html/body/div/div/div[3]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[{}]//span[contains(@class,'line-list') or contains(@class,'f15 text-bold') or contains(@class,'f19') or contains(@class,'f14 color-title')]".format(a)):
                    [YaoPinName.append(str(re.search('[^title="].*\"', name).group().replace('" class="f15 text-bold"', ''))) for name in item.re('(title=".*class="f15 text-bold">)')]
                    [YaoPinName.append(str(liang.replace('月销', '').strip())) for liang in item.re('(月销.*\s)')]
                    [YaoPinName.append(str(jia.replace('<', '').replace('>', ''))) for jia in item.re('(>\d{1,}\.\d{1,}<)')]
                    [YaoPinName.append(str(re.search('[^class="f14 color\-title">][\u4E00-\u9FA5]{0,}\w+.*\)?', chang).group().replace('<', ''))) for chang in item.re('(class="f14 color-title".*>.*<)')]

                try:
                    self.ToCsv(YaoPinName)
                    log.info("Error迭代的元素个数为：{}".format(len(YaoPinName))) if len(YaoPinName) != 4 else log.info("本次迭代的元素个数为：{}".format(len(YaoPinName)))
                    ToMsSql(YaoPinName)
                except Exception  as e:
                    log.info(e.args)
                    log.info(traceback.format_exc())
                    print("异常信息请观察日志！！！")
                    # del YaoPinName
                    YaoPinName.clear()
                    continue
                finally:
                    #del YaoPinName
                    YaoPinName.clear()

        browser.quit()
if __name__ == "__main__":
  GongSiName = YaoJingCai()
  GongSiName._name = '郑州福郎中'
  GongSiName._password = 'zzflz666'
  GongSiName._excelName = 'DerKang'
  GongSiName._PageNumber = 314
  GongSiName._login = "https://yao.jd.com/loginPage/detail?channel=yao&ReturnUrl=https%3A%2F%2Fyao.jd.com%2Forder%2Flist"

  GongSiName._url = 'https://yao.jd.com/search/home?currentPage={}&pageSize=20&key=%E5%BF%85%E5%BA%B7%E7%99%BE%E5%B7%9D%E5%8C%BB%E8%8D%AF%EF%BC%88%E6%B2%B3%E5%8D%97%EF%BC%89%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&minPrice=&maxPrice=&hasStock=false&sort=3&batchId=&searchType=1&actId=&venderId=&filtTypeJson=&hasDrug=all&hasRelation=false&hasJdSelf=false&hasArea=true'

  GongSiName.StartCrawl()

# 洛阳明康药业有限公司
# MingKang_url = 'https://yao.jd.com/search/home?currentPage={}&pageSize=20&key=%E6%B4%9B%E9%98%B3%E6%98%8E%E5%BA%B7%E8%8D%AF%E4%B8%9A%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&minPrice=&maxPrice=&hasStock=false&sort=3&batchId=&searchType=1&actId=&venderId=&filtTypeJson=&hasDrug=all&hasRelation=false&hasJdSelf=false&hasArea=true'
# 必康百川医药（河南）有限公司
# BIKang = 'https://yao.jd.com/search/home?currentPage={}&pageSize=20&key=%E5%BF%85%E5%BA%B7%E7%99%BE%E5%B7%9D%E5%8C%BB%E8%8D%AF%EF%BC%88%E6%B2%B3%E5%8D%97%EF%BC%89%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8&minPrice=&maxPrice=&hasStock=false&sort=3&batchId=&searchType=1&actId=&venderId=&filtTypeJson=&hasDrug=all&hasRelation=false&hasJdSelf=false&hasArea=true'
# 德尔康
# DerKang._url = "https://yao.jd.com/search/home?currentPage={}&pageSize=20&key=&minPrice=&maxPrice=&hasStock=false&sort=3&batchId=&searchType=1&actId=&venderId=&filtTypeJson=%5B%7B%22type%22%3A1,%22name%22%3A%22%E4%B8%80%E7%BA%A7%E5%88%86%E7%B1%BB%22,%22values%22%3A%5B%7B%22id%22%3A13720,%22name%22%3A%22%E8%8D%AF%E6%88%BF%E7%BB%8F%E8%90%A5%22%7D%5D%7D,%7B%22type%22%3A2,%22name%22%3A%22%E5%BA%97%E9%93%BA%22,%22values%22%3A%5B%7B%22id%22%3A10112040,%22name%22%3A%22%E6%B2%B3%E5%8D%97%E5%BE%B7%E5%B0%94%E5%BA%B7%E8%8D%AF%E4%B8%9A%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8%22%7D%5D%7D%5D&hasDrug=all&hasRelation=false&hasJdSelf=false&hasArea=true"