# coding: utf-8
import traceback
from MsSql import ToMsSql, ToCsv_JingDong
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from scrapy import Selector
import time
import re
import os
from logs import Log


class YaoJingCai():

    def __int__(self, account, password, objname, login_url, max_page, gongsiid):

        """
        类属性
        :param account: 药京采账号
        :param password:  药京采密码
        :param objname:  目标店铺名称
        :param login_url:  web 登录界面 url
        :param max_page:  目标店铺的最大页数， Get_Max_Number_Page() 方法会覆盖 此属性
        :param gongsiid:  公司名称对应的 id 号  可在数据库中  [192.168.0.84].[BI_2].[dbo].[DaiFenxi_GongSi] 查看
        :return:
        """
        self._account = account
        self._password = password
        self._login_url = login_url
        self._ObjName = objname
        self.MaxNumberPage = max_page
        self.GongSiId = gongsiid

    def Login_Search_GongSiMingCheng(self):

        """
        登录药京采账号 并 浏览器对象。
        :return: 返回一个浏览器对象
        """
        browser = webdriver.Firefox(executable_path=r"{}\driver\geckodriver.exe".format(os.path.abspath('.')))
        browser.get(self._login_url)
        time.sleep(3)
        browser.refresh()
        time.sleep(5)
        iframe = browser.find_element_by_xpath('/html/body/div[2]/div/div/div/iframe')
        browser.switch_to.frame(iframe)
        browser.find_element_by_name("loginname").clear()
        browser.find_element_by_name("loginname").send_keys(self._account)
        time.sleep(2)
        browser.find_element_by_name("nloginpwd").clear()
        browser.find_element_by_name("nloginpwd").send_keys(self._password)
        time.sleep(2)
        browser.find_element_by_id('paipaiLoginSubmit').click()
        time.sleep(10)
        # 无法获取 input 属性并写入 未知原因
        browser.get('https://yao.jd.com/shop/index/{}'.format(self._ObjName))
        # self.Get_Max_Number_Page(browser)

        return browser

    def Get_Max_Number_Page(self, bor_page):
        """

        :param bor_page:  浏览器对象
        :return: 返回店铺最大页数
        """
        time.sleep(5)
        MaxPage = list()
        html = bor_page.page_source
        selector = Selector(text=html)
        # 获取店铺最大页数

        for item in selector.xpath("//html//div[contains(@class,'el-pagination')]"):
            for maxpage in item.re('(>[0-9]{1,3}<)'):
                MaxPage.append(int(maxpage.replace('>', '').replace('<', '')))

        self.MaxNumberPage = max(MaxPage) + 1
        del MaxPage

    def Get_Max_DiV(self, bor_div):
        """

        :param bor_div: 浏览器对象
        :return: 返回 html div 最大块数
        """
        # 获取 div 最大块数
        time.sleep(5)
        MaxDiv = list()
        html = bor_div.page_source
        selector = Selector(text=html)
        for item in selector.xpath('//html//div[contains(@class,"pr fl mb15 mr15 product-wrap")]'):
            for maxpage in item.re('(index="\w+">?)'):
                MaxDiv.append(int(maxpage.replace('index="', '').replace('">', '')))
        maxdiv = max(MaxDiv) + 2
        del MaxDiv
        return maxdiv


    def Start_Crawl(self):
        """
        爬虫从这里开始。
        log 对象 记录爬出输出信息和异常信息
        :return:
        """
        log = Log(self._ObjName)
        option = Options()
        option.add_argument('--headless')
        browser = self.Login_Search_GongSiMingCheng()
        js = "window.scrollTo(0,-document.body.scrollHeight)"
        for page in range(1, 2):
            log.info("第 {} 次迭代页数".format(page))
            # 模拟鼠标滚轮滑动
            browser.execute_script(js)
            time.sleep(6)
            HtmlResource = browser.page_source
            selector = Selector(text=HtmlResource)
            maxdiv = self.Get_Max_DiV(browser)
            for _ in range(1, maxdiv):
                log.info("第 {} 次迭代元素".format(_))
                YaoPinName = list()
                for item in selector.xpath("/html/body/div[1]/div/div[3]/div[2]/div[1]/div[3]/div/div[3]/div/div[2]/div/div[{}]//span[contains(@class,'line-list') or contains(@class,'f15 text-bold') or contains(@class,'f19') or contains(@class,'f14 color-title')]".format(_)):
                    [YaoPinName.append(str(re.search('[^title="].*\"', name).group().replace('" class="f15 text-bold"', ''))) for name in item.re('(title=".*class="f15 text-bold">)')]
                    [YaoPinName.append(str(liang.replace('月销', '').strip())) for liang in item.re('(月销.*\s)')]
                    [YaoPinName.append(str(jia.replace('<', '').replace('>', ''))) for jia in item.re('(>\d{1,}\.\d{1,}<)')]
                    [YaoPinName.append(str(re.search('[^class="f14 color\-title">][\u4E00-\u9FA5]{0,}\w+.*\)?', chang).group().replace('<', ''))) for chang in item.re('(class="f14 color-title".*>.*<)')]

                print(YaoPinName)
                try:
                    # ToCsv_JingDong(YaoPinName, self._ObjName)
                    log.info("Error迭代的元素个数为：{}".format(len(YaoPinName))) if len(YaoPinName) != 4 else log.info("本次迭代的元素个数为：{}".format(len(YaoPinName)))
                    ToMsSql(YaoPinName, self.GongSiId)
                except Exception as e:
                    log.info(e.args)
                    log.info(traceback.format_exc())
                    print("异常信息请观察日志！！！")
                    YaoPinName.clear()
                    continue
                finally:
                    YaoPinName.clear()
        browser.quit()

if __name__ == "__main__":
    k = YaoJingCai()
    k._login_url = "https://yao.jd.com/loginPage/detail?channel=yao&ReturnUrl=https%3A%2F%2Fyao.jd.com%2Forder%2Flist"
    k._account = '郑州福郎中'
    k._password = 'zzflz666'
    k._ObjName = '10277792'
    k.GongSiId = 4
    k.Start_Crawl()

    aa = {'洛阳明康': [10066271, 2], '必康百川': [10082659, 3], '德尔康': [10250371, 1], '佐今明': [10277792, 4]}



