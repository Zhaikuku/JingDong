# coding: utf-8
import traceback
from logs import Log
from MsSql import ToMsSql, ToCsv
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from scrapy import Selector
import time
import re
import os






class TianMao():

    def __int__(self, account, password, objname, login_url, max_page):
        self._account = account
        self._password = password
        self._login_url = login_url
        self._ObjName = objname
        self.MaxNumberPage = max_page

    def Login_Search_GongSiMingCheng(self):
        profile = webdriver.FirefoxOptions()
        # 伪装模式
        # user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
        # profile.add_argument('--user-agent={}'.format(user_agent))
        # 设置无头模式
        profile.add_argument('-headless')
        #  about:config webdriver = false 关闭 webdriver 检测机制
        profile.set_preference("dom.webdriver.enabled", False)
        browser = webdriver.Firefox(executable_path=r"{}\driver\geckodriver.exe".format(os.path.abspath('.'), Options=profile))

        browser.get(self._login_url)
        time.sleep(5)
        browser.refresh()
        time.sleep(5)
        iframe = browser.find_element_by_xpath('//*[@id="J_loginIframe"]')
        browser.switch_to.frame(iframe)
        browser.find_element_by_name("fm-login-id").clear()
        browser.find_element_by_name("fm-login-id").send_keys(self._account)
        time.sleep(4)
        browser.find_element_by_name("fm-login-password").clear()
        browser.find_element_by_name("fm-login-password").send_keys(self._password)
        time.sleep(2)
        browser.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/form/div[4]/button').click()
        time.sleep(10)
        browser.get(self._ObjName)
        return browser

    def Get_Max_DiV(self, bor_div):
        # 获取 div 最大块数
        time.sleep(10)
        MaxDiv = list()
        html = bor_div.page_source
        selector = Selector(text=html)
        for item in selector.xpath('//html//div[contains(@class,"view grid-nosku ")]'):
            for maxpage in item.re('(class="product  "?)'):
                MaxDiv.append(str(maxpage.replace('class="', '').replace('">', '')))
        maxdiv = len(MaxDiv) + 1
        del MaxDiv
        return int(maxdiv)

    def Start_Crawl(self):
        log = Log('测试')
        option = Options()
        option.add_argument('--headless')
        browser = self.Login_Search_GongSiMingCheng()
        start_click = 0
        for _ in range(1, 34):
            start_click += 1
            if start_click > 1:
                browser.find_element_by_class_name('ui-page-next').click()
            time.sleep(5)
            # 模拟鼠标滚轮滑动至底部
            browser.execute_script("window.scrollTo(0,-document.body.scrollHeight)")
            browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            browser.execute_script('Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});')
            time.sleep(6)
            HtmlResource = browser.page_source
            time.sleep(6)
            maxdiv = self.Get_Max_DiV(browser)
            selector = Selector(text=HtmlResource)
            for _ in range(1, maxdiv):
                log.info("第 {} 次迭代元素".format(_))
                YaoPinList = list()
                for item in selector.xpath("/html/body/div[1]/div/div[3]/div/div[7]/div[{}]//p[contains(@class,'productPrice') or contains(@class,'productTitle') or contains(@class,'productStatus')]".format(_)):
                    for jiage in item.re('<em title="\d+\.\d+"?'):
                        YaoPinList.append(jiage.replace('<em title="', '').replace('"', ''))

                    for pinming in item.re('target="_blank" title=".*\"?'):
                        YaoPinList.append(re.search('[^arget="_blank" title="].*\"?', pinming).group())

                    for xiaoling in item.re('<em>.*</em>?'):
                        YaoPinList.append(xiaoling.replace('<em>', '').replace('</em>', ''))
                try:
                    ToCsv(YaoPinList, '测试')
                    log.info("Error迭代的元素个数为：{}".format(len(YaoPinList))) if len(YaoPinList) != 3 else log.info(
                        "本次迭代的元素个数为：{}".format(len(YaoPinList)))
                except Exception as e:
                    log.info(e.args)
                    log.info(traceback.format_exc())
                    print("异常信息请观察日志！！！")
                    YaoPinList.clear()

                    continue
                finally:
                    YaoPinList.clear()


if __name__ == "__main__":

  tianmao =  TianMao()
  tianmao._login_url = 'https://login.tmall.com/?spm=a1z10.3-b-s.a2226mz.2.319f738a6roLl7&redirectURL=https%3A%2F%2Fhnmsdyf.tmall.com%2Fsearch.htm%3Ftbpm%3D1%26scene%3Dtaobao_shop'
  tianmao._ObjName = 'https://list.tmall.com/search_product.htm?q=%BA%D3%C4%CF%C3%F1%C9%FA%B4%F3%D2%A9%B7%BF&type=p&spm=a1z10.3-b-s.a2227oh.d100&xl=%BA%D3%C4%CF%C3%F1%C9%FA_1&from=.shop.pc_1_suggest'
  # TianMao._ObjName = 'https://hnmsdyf.tmall.com/search.htm?scene=taobao_shop'
  tianmao._account = ''
  tianmao._password = ''
  tianmao.Start_Crawl()



