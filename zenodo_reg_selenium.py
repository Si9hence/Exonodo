# 导入 webdriver
from selenium import webdriver
import time
import pickle
# 要想调用键盘按键操作需要引入keys 包
from selenium.webdriver.common.keys import Keys

from pynput.keyboard import Key, Controller
import json

def save_cookie(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)

def load_cookie(driver, path):
    with open(path, 'rb') as cookiesfile:
        cookies = pickle.load(cookiesfile)
        for cookie in cookies:
            driver.add_cookie(cookie)
    return driver

def keyboard_simulation(action, keywords):
    keyboard = Controller()
    dict_hotkey = {"ctrl+enter":[Key.enter, Key.ctrl], "ctrl+n":[Key.alt,"n"]}
    if action == "type":
        keyboard.type(keywords)
    elif action == "hotkey":
        for item in dict_hotkey[keywords]:
            keyboard.press(item)
            time.sleep(0.1)
        for item in dict_hotkey[keywords]:
            keyboard.release(item)
    time.sleep(0.1)

 
with open('sample\info.json', 'rb') as f:
    info = json.load(f)
# 调用环境变量指定的PhantomJS 浏览器创建浏览器对象
driver = webdriver.Chrome()
driver.maximize_window()
# driver = webdriver.PhantomJS()
driver.get("https://zenodo.org/")
load_cookie(driver, 'ck.json')
driver.refresh()
driver.get("https://zenodo.org/deposit/5150278")


for itm in info['files']:
    file_name = "C:\\Users\\Yulin\\OneDrive\\UCL\\Course\\Project\\Jonathan\\Code\\sample\\" + itm
    driver.find_element_by_xpath(r'//*[@id="invenio-records"]/invenio-files-uploader/invenio-records/invenio-files-list/div[1]/div[1]/div/div[2]/span/button[2]').click()
    time.sleep(0.5)
    keyboard_simulation(action='hotkey', keywords="ctrl+n")
    time.sleep(0.5)
    keyboard_simulation(action='type', keywords=file_name)
    time.sleep(0.5)
    keyboard_simulation(action='hotkey', keywords="ctrl+enter")

# fill authors
for idx, itm in enumerate(info['authors']):
    xpath =[r"""//*[@ng-model="model['creators']['""" + str(idx) + r"""']['name']"]""",
    r"""//*[@ng-model="model['creators']['""" + str(idx) + r"""']['affiliation']"]""",
    r"""//*[@ng-model="model['creators']['""" + str(idx) + r"""']['orcid']"]"""]

    driver.find_element_by_xpath(xpath[0]).send_keys(itm['name'])
    driver.find_element_by_xpath(xpath[1]).send_keys(itm['affiliation'])
    driver.find_element_by_xpath(xpath[2]).send_keys(itm['orcid'])
    if idx != len(info['authors'])-1:
        driver.find_element_by_xpath(r'//*[@id="invenio-records"]/invenio-files-uploader/invenio-records/invenio-records-form/form/bootstrap-decorator[3]/fieldset/div/div[2]/sf-decorator[5]/div/div/div/a').click()

time.sleep(1)

driver.find_element_by_xpath(r'//*[@id="title"]').send_keys(info['title'])

xpath = r"""//*[@id="cke_1_contents"]/iframe"""
iframe = driver.find_element_by_xpath(xpath)
driver.switch_to.frame(iframe)
xpath = r'/html/body'
driver.find_element_by_xpath(xpath).send_keys(info['description'])
driver.switch_to.default_content()

xpath = r'''//*[@id="invenio-records"]/invenio-files-uploader/invenio-records/invenio-records-form/form/bootstrap-decorator[3]/fieldset/div/div[2]/sf-decorator[3]/div/div/input'''
driver.find_element_by_xpath(xpath).send_keys(info['publication_date'])

for idx, itm in enumerate(info['keywords']):
    xpath = r"""//*[@ng-model="model['keywords']['""" + str(idx) + "']\"]"
    driver.find_element_by_xpath(xpath).send_keys(itm)
    if idx != len(info['keywords'])-1:
        driver.find_element_by_xpath(r'//*[@id="invenio-records"]/invenio-files-uploader/invenio-records/invenio-records-form/form/bootstrap-decorator[3]/fieldset/div/div[2]/sf-decorator[9]/div/div/div/a').click()

time.sleep(1)
xpath = r"""//*[@id="invenio-records"]/invenio-files-uploader/invenio-records/invenio-records-form/form/bootstrap-decorator[2]/fieldset/div/div[2]/sf-decorator[1]/div/ul/li[4]/label/span"""
driver.find_element_by_xpath(xpath).click()

xpath = r"""//*[@id="invenio-records"]/invenio-files-uploader/invenio-records/invenio-records-form/form/bootstrap-decorator[8]/fieldset/div/div[1]"""
driver.find_element_by_xpath(xpath).click()
for idx, itm in enumerate(info['references']):
    xpath = r"""//*[@ng-model="model['references']['""" + str(idx) + "']\"]"
    driver.find_element_by_xpath(xpath).send_keys(itm)
    if idx != len(info['references'])-1:
        driver.find_element_by_xpath(r'//*[@id="invenio-records"]/invenio-files-uploader/invenio-records/invenio-records-form/form/bootstrap-decorator[8]/fieldset/div/div[2]/sf-decorator/div/div/div/a').click()


input()
# save_cookie(driver,"ck.json")




