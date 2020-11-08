import time
import datetime
import os
import traceback
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select

class clock_in:
    def __init__(self, dic, chrome_driver_path, op=1):
        self.dic = dic
        self.dirver_path = chrome_driver_path
        self.op = op
        self.log = ''

    def start(self):
        browser = self.browser_start(self.dirver_path, op=self.op)
        self.login(browser,self.dic)
        return self.log

    def login(self, browser, dic):
        #输入账号密码
        acc_input = browser.find_element_by_xpath('//*[@id="username"]')
        acc_input.clear()
        acc_input.send_keys(dic['username'])
        acc_input = browser.find_element_by_xpath('//*[@id="password"]')
        acc_input.clear()
        acc_input.send_keys(dic['passwd'])

        #点击登录
        browser.find_element_by_xpath('//*[@id="login-submit"]').click()
        print(dic['username']+' log in...')
        self.log += dic['username']+' log in...\t'
        time.sleep(3)

        #点击研究生打卡
        browser.find_element_by_xpath('//*[@id="cont_one_1"]/li[3]/a/dl/dd').click()
        time.sleep(2)

        #点击我要办理
        browser.find_element_by_xpath('//*[@id="service_guide"]/div/div/input[3]').click()
        print('进入打卡页面...')
        self.log += '进入打卡页面...\t'
        time.sleep(8)

        handles = browser.window_handles
        browser.switch_to_window(handles[1])

        #输入专业
        zy = browser.find_element_by_xpath('/html/body/div[4]/form/div/div[2]/div[3]/div/div[1]/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr[3]/td[2]/div/input')
        zy.clear()
        zy.send_keys(dic['zy'])

        #选择年级
        Select(browser.find_element_by_xpath(
            "/html/body/div[4]/form/div/div[2]/div[3]/div/div[1]/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr[3]/td[4]/font/div/select")).select_by_value(
            dic['nj'])
        #选择校区
        Select(browser.find_element_by_xpath(
            "/html/body/div[4]/form/div/div[2]/div[3]/div/div[1]/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr[4]/td[4]/font/div/select")).select_by_value(
            dic['xq'])

        #选择公寓
        Select(browser.find_element_by_xpath(
            "/html/body/div[4]/form/div/div[2]/div[3]/div/div[1]/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr[5]/td[2]/div/select")).select_by_value(
            dic['gy'])

        #填写寝室号
        qsh = browser.find_element_by_xpath('/html/body/div[4]/form/div/div[2]/div[3]/div/div[1]/div[2]/table/tbody/tr[2]/td/div/table/tbody/tr[6]/td[2]/div/input')
        qsh.clear()
        qsh.send_keys(dic['qsh'])

        #点击硕士
        browser.find_element_by_xpath('//*[@id="V1_CTRL44"]').click()
        print('填写基本信息...')
        self.log += '填写基本信息...\t'
        curr_time = datetime.datetime.now()
        hour = int(curr_time.hour)

        '''
        #判断打卡时间
        if hour == 7:
            # 7：00-8：00 体温状态
            browser.find_element_by_xpath('').click()
        elif hour == 11:
            #11：00-12：00 体温状态
            browser.find_element_by_xpath('//*[@id="V1_CTRL19"]').click()
        elif hour == 17:
            # 17：00-18：00 体温状态
            browser.find_element_by_xpath('//*[@id="V1_CTRL23"]').click()
        '''

        if hour > 5 and hour < 12:
            browser.find_element_by_xpath('//*[@id="V1_CTRL28"]').click()
        elif hour > 8 and hour < 11:
            pass
        print('打卡时间 '+curr_time.strftime('%Y-%m-%d %H:%M:%S')+'...')
        self.log += '打卡时间 '+curr_time.strftime('%Y-%m-%d %H:%M:%S')+'...\t'

        #提交
        browser.find_element_by_xpath('/html/body/div[4]/form/div/div[1]/div[2]/ul/li[1]').click()
        time.sleep(3)
        #确认
        browser.find_element_by_xpath('/html/body/div[6]/div/div[2]/button[1]').click()
        print('提交确认...')
        self.log += '提交确认...\t'
        time.sleep(3)
        if '办理成功' in browser.page_source:
            print('办理成功 !')
            self.log += '办理成功 !'
        browser.quit()

    def browser_start(self, path, op):
        chrome_driver_path = path
        os.environ["webdriver.ie.driver"] = chrome_driver_path
        if op == 0:
            #隐式使用浏览器
            option = webdriver.ChromeOptions()
            option.add_argument('headless')
            browser = webdriver.Chrome(options=option)
        elif op == 1:
            #显式使用浏览器
            browser = webdriver.Chrome()
        browser.get("https://ehall.jlu.edu.cn/jlu_portal/")
        time.sleep(3)
        return browser

#微信提醒打卡成功或失败
def notification(status, urlPush):
    textPush = status
    urlPush = 'https://sc.ftqq.com/'+SCKEY+'.send'
    dataPush = {'text':textPush}
    requests.post(urlPush, data=dataPush, verify=False)

if __name__ == "__main__":
    dic = dict()
    #****************************需要个人填写的部分*************************
    #'12':南苑8公寓 '10':'南苑6公寓'
    dic['lx'] = {'username': 're18', 'passwd': 'xxx', 'qsh': 'xxx', 'gy': '10', 'zy': u"计算机应用技术", 'xq': '1','nj': '9'}
    dic['zhy'] = {'username':'zj18','passwd':'xxx','qsh':'xxx','gy':'12','zy':u"计算机应用技术",'xq':'1','nj':'9'}
    chrome_driver_path = "C:\Program Files (x86)\Google\Chrome\Application" #chrome driver 位置 不同主机可能不同
    SCKEY = "..."
    #是否显示调用浏览器：1：显式，0：隐式
    op = 1
    # ****************************需要个人填写的部分*************************

    for person in dic:
        clock = clock_in(dic[person], chrome_driver_path, op)
        try:
            text = clock.start()
            notification(text,SCKEY)
        except Exception as e:
            traceback.print_exc()
            notification(clock.log+'\n打卡失败  错误提示：'+traceback.format_exc(),SCKEY)
