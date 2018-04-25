# coding: utf-8
from time import sleep
import traceback
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from lib.data import *
from lib.func import scan_dir
from lib.log import *
import sys


"""
    三江智慧云页面的方法封装
"""

__author__  = 'yangshifu'
# Note: the attributes below are no longer maintained.
__version__ = '2.0'
__date__ = "2017-08-01"


def sj_login(url, username, password, is_login=True, browser='Firefox'):
    """
    登陆页面
    :param url: url地址
    :param username: 用户名
    :param password: 密码
    :param is_login: 是否登陆
    :param browser: 采用的浏览器
    :return: 登陆后的driver
    """
    if browser.lower() == 'firefox' or browser.lower() == 'ff' or browser == u'火狐':
            # profile_dir = "C:\\Users\\shifu.yang\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\tvumvzbj.default"
            # profile_dir = os.environ.get('USERPROFILE') + os.sep + "AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\tvumvzbj.default"
            profile_base_dir = os.environ.get('USERPROFILE') + os.sep + "AppData\\Roaming\\Mozilla\\Firefox\\Profiles"
            for dir_name in os.listdir(profile_base_dir):
                if '.default' in dir_name:
                    profile_dir = os.path.join(profile_base_dir, dir_name)
                    break
                else:
                    profile_dir = None
            profile = webdriver.FirefoxProfile(profile_dir)
            driver = webdriver.Firefox(profile)
    elif browser.lower() == 'chrome'or browser.lower() == 'gc' or browser.lower() == 'googlechrome' or browser == u'谷歌':
        chromeOptions = webdriver.ChromeOptions()
        # 设置默认导出文件的路径
        prefs = {"download.default_directory": os.path.join(SJ_DOCS, 'export')}
        chromeOptions.add_experimental_option("prefs", prefs)
        # chromedriver = "path/to/chromedriver.exe"
        driver = webdriver.Chrome(chrome_options=chromeOptions)
    elif browser.lower() == 'ie' or browser.lower() == 'internetexplorer':
        driver = webdriver.Ie()
    else:
        log_write(get_current_info() + 'No driver found. Only support firefox or IE or Chrome now', 'critical')
        traceback.format_exc()
        raise Exception('No driver found. Only support firefox or IE or Chrome now')
    log_write(get_current_info() + 'Start browser with %s ...' % browser)
    driver.get(url)
    # 输入用户名和密码
    if username:
        user = driver.find_element_by_id('username')
        user.clear()
        user.send_keys(username)
        sleep(0.5)
    if password:
        driver.find_element_by_id('password').send_keys(password)
    if is_login:
        driver.find_element_by_xpath("//button[@class='btn btn-primary block full-width m-b']").click()
        driver.implicitly_wait(30)
    return driver

class PLMS(object):
    """
    实例化该类时登陆三江智慧云
    sj_main_    :   主页
    sj_list_    :   设备列表
    sj_panel_    :   设备编辑面板
    sj_func_    :   其他功能类方法
    """
    def __init__(self):
        """登陆网页"""
        self.driver = sj_login(url, username, password, browser=browser)
        cur_url = self.driver.current_url
        if cur_url in main_page:
            log_write(get_current_info() + 'Login PLMS success', 'info')
        else:
            log_write(get_current_info() + 'Login PLMS fail', 'critical')
            self.driver.quit()
            log_write(get_current_info() + 'Quit browser', 'warn')
            self.driver = sj_login(url, username, password, browser=browser)
            log_write(get_current_info() + 'Login PLMS again', 'warn')

    # 回到主页
    def sj_func_back_main_page(self):
        """
        回到主页
        :return: None
        """
        try:
            sleep(1)
            self.driver.find_element_by_xpath("//small[contains(.,'%s')]"%u'三江智慧云PLMS').click()
            self.driver.implicitly_wait(30)
            log_write(get_current_info() + 'Return back main page success')
            return None
        except:
            msg = 'Return back main page fail, try return back again. '
            log_write(get_current_info() + msg, 'warn')
        sleep(1)
        self.driver.refresh() # 刷新下网页再return back
        try:
            self.driver.find_element_by_xpath("//small[contains(.,'%s')]" % u'三江智慧云PLMS').click()
            log_write(get_current_info() + 'Return back main page success')
        except:
            msg = 'Return back main page fail'
            log_write(get_current_info() + msg, 'Error')
            traceback.format_exc()
            raise Exception(msg)

    # 刷新页面
    def sj_func_refresh(self):
        """
        刷新页面
        :return: None
        """
        self.driver.refresh()
        sleep(1)
        self.driver.implicitly_wait(10)
        log_write(get_current_info() + 'Refresh page', 'info')

    # 注销
    def sj_func_logout(self):
        """
        注销账号
        :return: None
        """
        try:
            self.driver.find_element_by_id('loginName').click()
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id('logout')).click()
            self.driver.find_element_by_xpath("//h3[contains(.,'%s')]" % u'登录三江智慧云PLMS').is_displayed()
            log_write(get_current_info() + get_current_info() + 'Logout success')
        except:
            log_write(get_current_info() + 'Logout fail', 'error')

    # 检查提示是否存在
    def sj_func_is_tips_display(self, content):
        """
        检查提示内容是否存在
        :param content: 错误或其他友情提示
        :return: bool值
        """
        try:
            self.driver.find_element_by_xpath("//*[contains(.,'%s')]" % content).is_displayed()
            log_write('Check tips exists success. tips is: %s' % content)
            return True
        except:
            log_write('Not found tips', 'warn')
            return False

    # 检查元素是否可用
    def sj_func_is_element_enable(self, ele_id):
        """
        检查元素是否可用
        :param ele_id: 元素id
        :return: bool值
        """
        try:
            self.driver.find_element_by_id(ele_id)
            log_write(get_current_info() + 'Check elements is enabled success. element: %s' % ele_id)
            return True
        except:
            log_write(get_current_info() + 'Not found element. element: %s' % ele_id, 'warn')
            return False

    # 点击菜单栏，进入设备列表界面
    def sj_main_to_device_list(self, index, sub_menu, dev_type=None):
        """
        点击菜单栏，进入相应界面
        :param index: int主菜单栏的索引值，从0开始，0~5
        :param sub_menu: 子菜单栏的中文菜单名
        :param dev_type: 第三层菜单的设备类型
        :return: None
        """
        try:
            # 根据索引值点击菜单栏
            menu_list = self.driver.find_element_by_id('slide_nav_list').find_elements_by_class_name("menu-text")
            menu_list[index].click()
            sleep(1)
            # 点击子菜单如“设备管理”
            ele_menu2 = self.driver.find_element_by_xpath("//a[contains(.,'%s')]" % sub_menu)
            ele_menu2.click()
            sleep(0.5)
            # index==0是用户设备，没有第三层菜单，跳过
            if dev_type:
                WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath("//ul//ul//ul//*[contains(.,'%s')]"%dev_type)).click()
                sleep(0.3)
                self.driver.implicitly_wait(10)
            log_write(get_current_info() + "Enter device list success, device list: [%s, '%s', '%s']" % (index, sub_menu, dev_type))
            return True
        except:
            msg = "Enter device list fail, device list: [%s, '%s', '%s']" % (index, sub_menu, dev_type)
            log_write(get_current_info() + msg, 'error')
            traceback.format_exc()
            raise Exception(msg)

    # 进入设备编辑面板
    def sj_main_to_device_panel(self, device_id, index, sub_menu, dev_type=''):
        """
        从主页进入设备编辑面板页
        :param device_id: 设备ID
        :param index: 主菜单栏的索引值，从0开始，0~5
        :param sub_menu: 子菜单栏的中文菜单名
        :param dev_type: 第三层菜单的设备类型
        :return: None
        """
        try:
            # 进入设备界面
            self.sj_main_to_device_list(index, sub_menu, dev_type)
            # 查找用户
            sleep(0.5)
            search = self.driver.find_element_by_id('keywordSearchBox')
            search.send_keys(device_id)
            search.send_keys(Keys.ENTER)
            WebDriverWait(self.driver, 10).until(
                lambda x: x.find_element_by_id('edit_' + device_id).find_element_by_class_name("btn-group")).click()
            sleep(0.5)
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id('name'))
            log_write(get_current_info() + 'Enter device panel success. device is: %s' % device_id)
        except:
            log_write(get_current_info() + 'Enter device panel fail. device is: %s' % device_id, 'error')

    # 查找设备
    def sj_list_is_device_exist(self, device_id, device_menu='', is_check=True):
        """
        在设备列表界面查找设备，is_check为True时检查设备的存在性，is_check为False时，跳过检查
        :param device_id: 设备ID
        :device_menu: 点击设备菜单栏元素的id，默认为空，已关注设备、未关注设备、设备属主、公众用户 分别为：observed、unobserved、authorized、deviceType_title
        :is_check: 为True时检查设备是否存在
        :return: bool值. 存在返回True，不存在返回False， 跳过检查也返回True
        """
        if device_menu:
            self.driver.find_element_by_id('%s' % device_menu).click()
        sleep(2)
        search = self.driver.find_element_by_id('keywordSearchBox')
        search.clear()
        search.send_keys(device_id)
        search.send_keys(Keys.ENTER)
        sleep(1)
        flag_check = False
        if is_check:
            dev_element = self.driver.find_elements_by_xpath("//tbody[@id='list_body']/tr")
            if len(dev_element) < 1:
                return flag_check
            device_list = []
            for i in range(1, len(dev_element) + 1):
                element = self.driver.find_element_by_xpath("//tbody[@id='list_body']/tr[%d]/td[2]" % i)
                device_list.append(element.text)
            if device_id in device_list:
                flag_check = True
        else:
            flag_check = True
        if flag_check:
            log_write(get_current_info() + "Search the device success. device id: %s" % device_id)
        else:
            log_write(get_current_info() + "Not found the device. device id: %s" % device_id, 'warn')
        return flag_check

    # 每隔2秒查找一次设备，直到设备被找到
    def sj_list_until_device_exist(self, device_id):
        """
        每隔2秒查找一次设备，直到设备被找到，查询10次仍未找到至返回False
        :param device_id:
        :return: bool值
        """
        count = 0
        while count < 10:
            if self.sj_list_is_device_exist(device_id):
                log_write(get_current_info() + 'Search device exist success. device id: %s' % device_id)
                return True
            sleep(2)
            count += 1
        traceback.format_exc()
        log_write(get_current_info() + 'Not found the device. device id: %s' % device_id, 'warn')
        return False

    # 搜索
    def sj_list_search(self, keyword):
        """
        在设备列表页，通过关键字过滤出符合条件的设备
        :param keyword: 关键字
        :return: None
        """
        try:
            search = self.driver.find_element_by_id('keywordSearchBox')
            search.clear()
            search.send_keys(keyword)
            search.send_keys(Keys.ENTER)
            sleep(1)
            log_write(get_current_info() + 'Search the keyword success. keyword: %s' % keyword)
        except:
            msg = 'Search the keyword fail. keyword: %s' % keyword
            log_write(get_current_info() + msg, 'Error')
            traceback.format_exc()
            raise Exception(msg)


    # 复制设备
    def sj_list_copy_device(self, device_id, is_save=True):
        """
        复制用户设备
        :param device_id: 原设备ID
        :is_save: 是否保存
        :return: 返回新设备ID
        """
        try:
            if not self.sj_list_is_device_exist(device_id, is_check=True):
                raise Exception('Device not found')
            self.driver.find_element_by_xpath(".//tbody[@id='list_body']/tr[1]/td[1]/input").click()
            self.driver.find_element_by_id('btn_copy').click()
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id('name')).is_displayed()
            new_device_id = self.driver.find_element_by_id('pf-_id').text
            if is_save:
                self.driver.find_element_by_id('save').click()
                sleep(3)
            log_write(get_current_info() + 'Copy device success. new device key: %s' % new_device_id)
        except:
            log_write(get_current_info() + 'Copy device fail', 'Error')
            traceback.format_exc()
            raise Exception('Copy device fail')
        return new_device_id

    # 删除设备 - 搜索到该设备然后删除
    def sj_list_del_device(self, device_id):
        """
        删除用户设备
        :param device_id: 设备ID
        :return:
        """
        if not self.sj_list_is_device_exist(device_id, is_check=True):
            traceback.format_exc()
            log_write(get_current_info() + "Not found device when delete device. device id: %s" % device_id, 'warn')
            raise Exception('Device not found')
        self.driver.find_element_by_xpath(".//tbody[@id='list_body']/tr[1]/td[1]/input").click()
        self.driver.find_element_by_id('btn_del').click()
        WebDriverWait(self.driver, 10).until(
            lambda x: x.find_element_by_xpath("//button[contains(.,'%s')]" % u'确定')).click()
        sleep(1)
        log_write(get_current_info() + "delete device success. device id: %s" % device_id)

    # 删除设备 - 直接从设备列表中删除（不需要等待设备同步，直接删除，效率快）
    def sj_list_del_device_upgrade(self, device_key, count=1, is_last_page=True, flag_device_id=None):
        """
        从最后一页最后一项往前逐条记录遍历设备ID并删除，遇到flag_device_id则停止,用于删除测试时新增设备
        :param device_key: 模糊匹配设备ID（可用于批量删除，尽可能最大匹配，防止误删）
        :param count: 待删除的设备数，精确删除设备时为1
        :param is_last_page: 是否只在最后一页进行遍历
        :param flag_device_id: 设备ID标识，遍历到该标识则退出整个遍历过程，设置该设备值防止误删
        :return: bool值
        """
        checked_count = 0   # 选中的设备数
        sleep(0.1)
        ele_last_page = self.driver.find_element_by_xpath("//ul[@id='pagination']/li[5]/a")
        raw_page_count = ele_last_page.get_attribute('data-page') # 页数
        # 点击最后一页，从最后一页往前遍历
        ele_last_page.click()
        sleep(1.5)
        # 循环点击下一页，遍历所有设备记录
        for i in range(int(raw_page_count)):
            dev_elements = self.driver.find_elements_by_xpath("//tbody[@id='list_body']/tr")
            # 从一页中最后一条记录开始往前遍历
            for row in range(0, len(dev_elements)):
                # 获取设备ID的元素
                element = self.driver.find_element_by_xpath("//tbody[@id='list_body']/tr[%d]/td[2]" % (len(dev_elements)-row))
                element_id = element.text
                # 该设备id中包含device_key，勾选中
                if device_key in element_id:
                    checked_count += 1
                    check_box = self.driver.find_element_by_xpath(".//tbody[@id='list_body']/tr[%d]/td[1]/input"% (len(dev_elements)-row))
                    check_box.click()
                    sleep(0.5)
                     # 如果选中的设备数小于或等于预期数量则删除，防止删除原始数据
                    if checked_count <= count :
                        self.driver.find_element_by_id('btn_del').click()
                        WebDriverWait(self.driver, 10).until(
                            lambda x: x.find_element_by_xpath("//button[contains(.,'%s')]" % u'确定')).click()
                        sleep(0.5)
                    else:
                        return False
                if flag_device_id:
                    if flag_device_id == element_id:
                        log_write(get_current_info() + 'Delete device with device key success. device key: %s' % device_key)
                        return True

            # 如果当前是第一页则退出
            pre_page = self.driver.find_element_by_xpath("//ul[@id='pagination']/li[2]/a").get_attribute('data-page')
            if pre_page == 0:
                break

            # is_last_page为True时只查找最后最后一页，即此时退出，否则前往上一页
            if is_last_page:
                break
            else:
                # is_last_page为false时，继续向前页遍历所有记录
                # 如果最后一页内容全被删除，则总页数会自动减少
                page_count = self.driver.find_element_by_xpath("//ul[@id='pagination']/li[5]/a").get_attribute('data-page')
                if int(page_count) == int(raw_page_count):
                    # 如果没有减少，则点击上一页
                    self.driver.find_element_by_xpath("//ul[@id='pagination']/li[2]/a").click()
                    self.driver.implicitly_wait(10)
                    sleep(1)
                else:
                    # 页数自动减少了的话自动回到上一页
                    sleep(1)
        # 整个遍历结束后,已经删除的设备checked_count应该等于count
        if checked_count != count:
            log_write(get_current_info() + 'Delete device with device key fail. device key: %s' % device_key, 'Error')
            return False
        log_write(get_current_info() + 'Delete device with device key success. device key: %s' % device_key)
        return True

    #添加设备界面，各选项信息
    def sj_basic_dev_info(self,d_name,d_describe,d_owner,d_encrypt,d_key,d_value,is_save=True):
        '''
        添加设备时，各个选项信息
        d_name：设备名称
        d_decribe：设备描述
        d_owner：属主
        d_encrypt：加密方式
        d_key：扩展信息中key值
        d_value：扩展信息中value值
        '''
        if d_name:
            device_name=self.driver.find_element_by_id("pf-deviceName")
            device_name.click()
            inputinfo=self.driver.find_element_by_xpath("//input[@class='form-control input-sm']")
            inputinfo.clear()
            inputinfo.send_keys(d_name)
            sleep(1)
        if d_describe:
            device_describe=self.driver.find_element_by_id("pf-deviceDesc")
            device_describe.click()
            self.driver.find_element_by_xpath("//input[@class='form-control input-sm']").clear()
            self.driver.find_element_by_xpath("//input[@class='form-control input-sm']").send_keys(d_describe)
            sleep(1)
        if d_owner:
            device_owner=self.driver.find_element_by_id("pf-ownerDevice_id")
            device_owner.click()
            self.driver.find_element_by_xpath("//input[@class='form-control input-sm']").clear()
            self.driver.find_element_by_xpath("//input[@class='form-control input-sm']").send_keys(d_owner)
            sleep(1)
        if d_encrypt:
            device_encrypt=self.driver.find_element_by_id("pf-encrypt")
            device_encrypt.click()
            Select(self.driver.find_element_by_xpath("//select[@class='form-control input-sm']")).select_by_value(d_encrypt)
        if d_key:
            Expandkey=self.driver.find_element_by_xpath("//input[@placeholder='请输入key...']")
            Expandkey.click()
            sleep(1)
            Expandkey.send_keys(d_key)
        if d_value:
            Expandvalue=self.driver.find_element_by_xpath("//input[@placeholder='请输入value...']")
            Expandvalue.click()
            sleep(1)
            Expandvalue.send_keys(d_value)
            sleep(1)
        if is_save:
            self.driver.find_element_by_id("save").click()

    # 添加设备
    def sj_list_add_device(self, device_name, is_save=True):
        """
        添加用户设备后，如果保存则，回到原界面，如果不保存，则界面不跳转
        :param device_name: 新设备名
        :is_save:保存则，返回原界面，不保存则留在新用户界面
        :return: 新设备ID
        """
        self.driver.find_element_by_id('btn_add').click()
        self.driver.implicitly_wait(10)
        try:
            self.driver.find_element_by_xpath("//button[@class='btn btn-primary' and text()='确定']").click()
        except:
            WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id('name')).is_displayed()
            new_device_id = self.driver.find_element_by_id('pf-_id').text
            self.driver.find_element_by_id('pf-deviceName').click()
            sleep(0.5)
            element_name = self.driver.find_element_by_xpath("//input[@class='form-control input-sm']")
            element_name.send_keys(device_name)
            element_name.send_keys(Keys.ENTER)
            if is_save:
                self.driver.find_element_by_id('save').click()
                sleep(2)
            log_write(get_current_info() + 'Add new device success. new device id: %s' % new_device_id)
            return new_device_id

    # 勾选设备
    def sj_list_select_device(self, index=1):
        """
        设备列表界面勾选设备，默认勾选第一个设备
        :param index: 设备位置，index为1表示设备列表页第一个设备，index为-1表示倒数第一个设备，index=0,选中所有设备，默认勾选当前页第一个设备
        :return: None
        """
        # index 为正值，表示从上往下数的第index个设备
        if index > 0:
            self.driver.find_element_by_xpath(".//tbody[@id='list_body']/tr[%d]/td[1]/input" % index).click()
        # index 为0，选中当页所有设备
        elif index == 0:
            sleep(0.5)
            self.driver.find_element_by_xpath(".//*[@id='page_content']/div[1]/div[2]/div/div/table/thead/tr/th[1]/label/span").click()
        # index 为负值时，从下往上数的第-index个设备
        else:
            dev_elements = self.driver.find_elements_by_xpath("//tbody[@id='list_body']/tr")
            count = len(dev_elements)
            self.driver.find_element_by_xpath(".//tbody[@id='list_body']/tr[%d]/td[1]/input" % (count+index+1)).click()
        log_write(get_current_info() + 'Select device success')

    # 编辑设备
    def sj_list_edit_device(self, index=-1):
        """
        设备列表界面编辑设备，默认编辑最后一个设备，进入设备面板页
        :param index: 设备位置，index为1表示设备列表页第一个设备，index为-1表示倒数第一个设备,默认编辑当前页最后一个设备
        :return: None
        """
        if index > 0:
            self.driver.find_element_by_xpath("//tbody[@id='list_body']/tr[%d]/td[7]/div/a" % index).click()
        elif index == 0:
            pass    # index取值为0无效
        # index 为负值时，从下往上数的第-index个设备
        else:
            dev_elements = self.driver.find_elements_by_xpath("//tbody[@id='list_body']/tr")
            count = len(dev_elements)
            self.driver.find_element_by_xpath("//tbody[@id='list_body']/tr[%d]/td[7]/div/a" % (count + index + 1)).click()
        log_write(get_current_info() + 'edit device success')

    # 页面操作
    def sj_list_pagenation(self, page_id, is_click=True):
        """
        获取页码值，is_click为True时可点击page_id代表的元素
        :param page_id: 取值1、2、3、4、5分别代表点击第一页/上一页/当前页/下一页/最后一页
        :param is_click: 是否点击
        :param get_data_page: 是否获取该page_id的data-page属性，即页码值
        :return: 返回页码值，如page_id=5，获取最后一页的页码值
        """
        ele_page = self.driver.find_element_by_xpath("//ul[@id='pagination']/li[%d]/a" % page_id)
        if page_id != 3:
            page_num =ele_page.get_attribute('data-page')
        else:
            # 当前页的页码值为上一页的页码加1
            page_num = self.driver.find_element_by_xpath("//ul[@id='pagination']/li[2]/a").get_attribute('data-page') + 1
        log_write(get_current_info() + 'Get page number success. page number is: %d' % int(page_num))
        if is_click:
            ele_page.click()
            log_write(get_current_info() + 'Click page element success. page number is: %s' % int(page_num))
            sleep(0.8)
        return int(page_num)

    # 导入
    def sj_list_import_device(self, dev_type=None, dev_name=None, virtual_dev=None, \
                              dev_owner=None,upload_file=None,file_path=None,is_confirm=True):
        """
        导入设备界面封装
        :param dev_type:选择设备类型
        :param dev_name:输入设备名称
        :param dev_batch:输入设备批次
        :param virtual_dev:虚拟设备分组
        :param dev_owner:添加设备属主
        :param upload_file:上传excel文件
        :param is_confirm: 确定还是取消
        :return:None
        """
        if dev_type:
            selector = Select(self.driver.find_element_by_id('importDevTypes'))
            selector.select_by_value(dev_type)
            sleep(0.2)
        if dev_name:
            self.driver.find_element_by_id('deviceName').send_keys(dev_name)
        # if dev_batch:
        #     self.driver.find_element_by_id('deviceBatch').send_keys(dev_batch)
        if virtual_dev:
            selector = Select(self.driver.find_element_by_id('virtualDevice'))
            selector.select_by_value(virtual_dev)
            sleep(0.2)
        if dev_owner:
            self.driver.find_element_by_id('deviceOwner').send_keys(dev_owner)
        if upload_file:
            self.driver.find_element_by_id('importFile').click()
            sleep(0.8)
            self.driver.find_element_by_name('file-input').send_keys(upload_file)
            sleep(0.5)
            self.driver.find_element_by_xpath("//form[@id='myform']/div[2]/button[1]").click()
            sleep(0.5)
        if is_confirm:
            self.driver.find_element_by_id('import_submit').click()
        log_write(get_current_info() + "Import file. condition is: dev_type=%s. dev_name=%s. virtual_dev=%s. dev_owner=%s. upload_file=%s, is_confirm=%s"
                % (dev_type, dev_name, virtual_dev, dev_owner, upload_file, is_confirm))

    # 批量导出设备
    def sj_list_export_device(self, dev_type=None, batch_num=None, exp_count=None, exp_is_excel=True, is_confirm=True, sleep_time=3):
        """
        导出设备界面封装
        :param dev_type: 设备类型（非中文类型名）
        :param dev_type: 设备类型（非中文类型名）
        :param exp_count: 导出个数
        :param exp_is_excel: 导出方式
        :param is_confirm: 是否确定导出
        :param sleep_time: 等待导出完成，默认3秒，检查错误导出的提示需设置sleep_time为0跳过等待
        :return:None
        """
        self.driver.find_element_by_id('btn_exp').click()
        sleep(1)
        if dev_type:
            sel_type = Select(self.driver.find_element_by_id('exportDevTypes'))
            sel_type.select_by_value(dev_type)
            sleep(0.1)
        if batch_num:
            self.driver.find_element_by_id('exportDevBatch').send_keys(batch_num)
            sleep(0.1)
        if exp_count:
            self.driver.find_element_by_id('numberOfExpDev').send_keys(exp_count)
            sleep(0.1)
        if exp_is_excel:
            self.driver.find_element_by_id('exportExcel').click()
        else:
            self.driver.find_element_by_id('exportTxt').click()
        if is_confirm:
            self.driver.find_element_by_id('export_submit').click()
        else:
            self.driver.find_element_by_id('export_cancel').click()
        if sleep_time:
            sleep(sleep_time)
        else:
            pass
        log_write(get_current_info() + 'Export file. condition is：dev_type=%s, batch_num=%s, exp_count=%s, exp_is_excel=%s, '
                  'is_confirm=%s, sleep_time=%s'% (dev_type, batch_num, exp_count, exp_is_excel, is_confirm, sleep_time))

    #批量导出设备地址
    def sj_list_export_devaddr(self, dev_type=None, batch_num=None, exp_count=None, exp_is_pdf=True, is_confirm=True, sleep_time=3):
        """
        导出设备界面封装
        :param dev_type: 设备类型（非中文类型名）
        :param batch_num: 设备批次
        :param exp_count: 导出个数
        :param exp_is_pdf: 导出方式
        :param is_confirm: 是否确定导出
        :param sleep_time: 等待导出完成，默认3秒，检查错误导出的提示需设置sleep_time为0跳过等待
        :return:None
        """
        self.driver.find_element_by_id('add_exp').click()
        sleep(1)
        if dev_type:
            sel_type = Select(self.driver.find_element_by_id('exportAddDevTypes'))
            sel_type.select_by_value(dev_type)
            sleep(0.1)
        if batch_num:
            self.driver.find_element_by_id('exportAddDevBatch').send_keys(batch_num)
            sleep(0.1)
        if exp_count:
            self.driver.find_element_by_id('numberOfAddExpDev').send_keys(exp_count)
            sleep(0.1)
        if exp_is_pdf:
            self.driver.find_element_by_id('exportAddressPdf').click()
        else:
            self.driver.find_element_by_id('exportAddressTxt').click()
        if is_confirm:
            self.driver.find_element_by_id('export_add_submit').click()
        else:
            self.driver.find_element_by_id('export_add_cancel').click()
        if sleep_time:
            sleep(sleep_time)
        else:
            pass
        log_write(get_current_info() + 'Export file. condition is：dev_type=%s, batch_num=%s, exp_count=%s, exp_is_pdf=%s, '
                  'is_confirm=%s, sleep_time=%s'% (dev_type, batch_num, exp_count, exp_is_pdf, is_confirm, sleep_time))

    # 批量生成
    def sj_list_gen_device(self, total_count=None, dev_type=None, dev_name=None, dev_owner=None, is_confirm =True):
        """
        批量生成设备
        :param total_count:生成个数
        :param dev_type:设备类型
        :param dev_name:设备名称
        :param dev_owner:设备属主
        :param is_confirm: 是否确定
        :return: None
        """
        self.driver.find_element_by_id('batchGen').click()
        self.driver.implicitly_wait(10)
        sleep(0.5)
        if total_count:
            self.driver.find_element_by_id('totalNum').send_keys(total_count)
            sleep(0.1)
        if dev_type:
            sel_type = Select(self.driver.find_element_by_id('devType'))
            sel_type.select_by_value(dev_type)
            sleep(0.1)
        if dev_name:
            self.driver.find_element_by_id('devName').send_keys(dev_name)
            sleep(0.1)
        if dev_owner:
            self.driver.find_element_by_id('devOwner').send_keys(dev_owner)
            sleep(0.1)
        if is_confirm:
            self.driver.find_element_by_id('batchGen_submit').click()
        else:
            self.driver.find_element_by_id('batchGen_cancel').click()
        self.driver.implicitly_wait(10)
        log_write(get_current_info() + 'Gen batch device. condition is:total_count=%s, dev_type=%s, dev_name=%s, '
                  'dev_owner=%s, is_confirm=%s' % (total_count, dev_type, dev_name, dev_owner, is_confirm))

    def sj_list_function(self, function_id):
        """
        点击进入设备列表左下方的功能项
        :param function_id: 功能元素id，如导入为'btn_imp'，导出为'btn_exp'，批量生成为'batchGen'
        :return: None
        """
        self.driver.find_element_by_id(function_id).click()
        sleep(0.5)
        self.driver.implicitly_wait(10)
        log_write(get_current_info() + 'Click element. element id: %s' % function_id)

    # 遍历设备列表中内容
    def sj_list_scan_device(self, is_all_page=False):
        """
        遍历设备列表中当前页的内容，is_all_page为True时，遍历所有页的内容
        :param is_all_page: 是否遍历所有页的内容
        :return: 设备列表的二维数组
        """
        dev_list = []
        page_count = self.driver.find_element_by_xpath("//ul[@id='pagination']/li[5]/a").get_attribute('data-page')
        # 循环点击下一页，遍历所有设备记录
        for i in range(int(page_count)):
            dev_elements = self.driver.find_elements_by_xpath("//tbody[@id='list_body']/tr")
            for row in range(1, len(dev_elements) + 1):
                sub_dev_list = []
                for col in range(2, 7):
                    element = self.driver.find_element_by_xpath("//tbody[@id='list_body']/tr[%d]/td[%d]" % (row, col))
                    sub_dev_list.append(element.text)
                dev_list.append(sub_dev_list)
            if is_all_page:
                self.driver.find_element_by_xpath("//ul[@id='pagination']/li[4]/a").click()
                self.driver.implicitly_wait(10)
                sleep(1)
            else:
                break
        log_write(get_current_info() + 'Scan device list. is all page: %s')
        return dev_list

    # 遍历页面表格数据
    def sj_list_scan_page(self, start, stop, is_all_page=False):
        """
        遍历设备列表中当前页的某些列的内容，is_all_page为True时，遍历所有页的内容。
        :param is_all_page: 是否遍历所有页的内容
        :param start: 初始列
        :param stop: 结束列，该列不扫描
        :return: 获取多列时，返回设备列表的二维数组[(...),(...),(...)]，获取单列时返回列表[...]
        """
        dev_list = []
        sleep(3)
        page_count = self.driver.find_element_by_xpath("//ul[@id='pagination']/li[5]/a").get_attribute('data-page')
        # 循环点击下一页，遍历所有设备记录
        for i in range(int(page_count)):
            dev_elements = self.driver.find_elements_by_xpath("//tbody[@id='list_body']/tr")
            for row in range(1, len(dev_elements) + 1):
                sub_dev_list = []
                for col in range(start, stop):
                    element = self.driver.find_element_by_xpath("//tbody[@id='list_body']/tr[%d]/td[%d]" % (row, col))
                    element = str(element.text)   # element原本为unicode类型，转换成str类型
                    sub_dev_list.append(element)
                dev_list.append(tuple(sub_dev_list))
            if is_all_page:
                self.driver.find_element_by_xpath("//ul[@id='pagination']/li[4]/a").click()
                self.driver.implicitly_wait(10)
                sleep(1)
            else:
                break
        # 如果只获取一列数据，返回结果为列表形式
        dev_list_single = []
        if len(dev_list[0]) == 1:
            for text in dev_list:
                dev_list_single.append(text[0])
            log_write(get_current_info() + 'Scan page. return only one column data')
            return dev_list_single
        log_write(get_current_info() + 'Scan page. return several column data. start: %s. stop: %s. is all page: %s' % (start, stop, is_all_page))
        return dev_list

    # 修改属主  // + + + + + + + + + + +  deserted  + + + + + + + + + + +
    def sj_panel_mod_owner(self, value):
        """
        修改属主
        :param value: 属主ID值
        :return: None
        """
        # 修改属主
        owner = self.driver.find_element_by_id('pf-ownerDevice_id')
        raw_value = owner.text
        owner.click()
        val_owner = self.driver.find_element_by_xpath("//input[@class='form-control input-sm']")
        val_owner.clear()
        if raw_value != value:
            val_owner.send_keys(value)
        else:
            raise ValueError('owner is not exist')
        val_owner.send_keys(Keys.ENTER)
        # 保存
        self.driver.find_element_by_id('save').click()
        self.driver.implicitly_wait(30)
        # 检查更新记录验证修改成功
        self.driver.refresh()
        self.driver.find_element_by_id("changelog").click()
        record = self.driver.find_elements_by_xpath("//tbody[@id='profile-changelist']/tr[1]/td")
        assert record[0].text == username
        assert record[2].text == u'属主'
        if raw_value != value:
            assert record[4].text == value

    # 关注设备、取消关注、移交属主
    def sj_panel_manage_user(self, device_id, device_menu, new_owner_id=''):
        """
        用户编辑面板开始，对设备列表中中的device_id设备进行操作，实现关注设备、取消设备、移交设备的功能
        :param device_id:
        :param device_menu: 取值为'observed'、'unobserved'、'authorized'
        :return: None
        """
        self.driver.find_element_by_id('%s' % device_menu).click()
        sleep(0.5)
        # 点击关注列表，取消关注第一个设备 搜索设备筛选目前存在问题，已规避处理
        if device_menu == 'observed':
            dev_element = self.driver.find_elements_by_xpath("//tbody[@id='list_body']/tr")
            for index in range(1, len(dev_element)+1):
                if self.driver.find_element_by_xpath("//tbody[@id='list_body']/tr[%d]/td[2]"%index).text == device_id:
                    # 选中设备 -> 取消关注
                    self.driver.find_element_by_xpath("//tbody[@id='list_body']/tr[%d]/td[1]/input"% index).click()
                    self.driver.find_element_by_id('btn_unobserve').click()
                    sleep(0.5)
                    break
        if device_menu == 'unobserved':
            self.sj_list_is_device_exist(device_id, device_menu, is_check=False)
            # 选中设备并关注
            self.driver.find_element_by_xpath("//tbody[@id='list_body']/tr[1]/td[1]/input").click()
            self.driver.find_element_by_id('btn_observe').click()
            sleep(0.5)
        if device_menu == 'authorized':
            self.sj_list_is_device_exist(device_id, device_menu, is_check=False)
            self.driver.find_element_by_xpath("//tbody[@id='list_body']/tr[1]/td[1]/input").click()
            self.driver.find_element_by_id('btn_devolveOwner').click()
            if new_owner_id:
                sleep(1)
                WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id('newOwnerId')).send_keys(new_owner_id)
                self.driver.find_element_by_id('devolveOwner_submit').click()
            # 取消移交属主
            else:
                sleep(1)
                WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id('newOwnerId'))
                self.driver.find_element_by_id('devolveOwner_cancel').click()

    # 编辑新增设备的设备属性  // + + + + + + + + + + +  deserted  + + + + + + + + + + +
    def sj_panel_modify_device(self, index, value):
        """
        在新增设备界面修改设备属性值后保存。
        :param index: 属性列的索引值，如ID的索引为4，
        :value: 属性值
        :return: None
        """
        self.driver.find_element_by_xpath("//tbody[@id='profile-fields']/tr[quarter]/td[2]"%index).click()
        attr_ele = self.driver.find_element_by_class_name('form-control input-sm')
        attr_ele.clear()
        attr_ele.send_keys(value)
        attr_ele.send_keys(Keys.ENTER)
        self.driver.find_element_by_id('save').click()

    # 获取设备属性值
    def sj_panel_get_attr(self, attr_ele_id):
        """
        获取设备属性值并返回
        :param attr_ele_id: 属性元素id， 如属主id为："pf-ownerDevice_id"
        :return: 属性值
        """
        attr_value = self.driver.find_element_by_id(attr_ele_id).text
        log_write(get_current_info() + 'Get attribute of device success. attribute id: %s. attribute value: %s.'% (attr_ele_id, attr_value))
        return attr_value

    # 修改设备属性并保存
    def sj_panel_update_attr(self, attr_ele_id, new_value, is_sure=False, is_save=True):
        """
        在设备编辑面板界面，修改设备属性的值
        :param attr_ele_id: 设备属性的值对应的元素id， 如属主：'pf-ownerDevice_id'
        :param new_value: 设备属性的值
        :param is_sure:处理弹出框，True确定，False取消
        :param is_save:是否保存
        :return: None
        """
        ele_secret = self.driver.find_element_by_id(attr_ele_id)
        ele_secret.click()
        sleep(1)

        # 修改安装地址弹出地图，是否确定
        if attr_ele_id == 'pf-installAddress':
            self.driver.implicitly_wait(10)
            ele_addr = self.driver.find_element_by_id('geoSearch')
            ele_addr.click()
            ele_addr.clear()
            ele_addr.send_keys(new_value)
            if is_sure:
                self.driver.find_element_by_id('geoModify_submit').click()
            else:
                self.driver.find_element_by_id('geoModify_cancel').click()
            self.driver.implicitly_wait(10)
            return None

        # 修改加密方式--取值有：'false'（不加密）,"aes-128-ecb"
        if attr_ele_id == 'pf-encrypt':
            sel = self.driver.find_element_by_tag_name("select")
            Select(sel).select_by_value(new_value)
            if is_save:
                self.driver.find_element_by_id('save').click()
            self.driver.implicitly_wait(10)
            return None
        ele_input = self.driver.find_element_by_xpath("//input[@class='form-control input-sm']")
        ele_input.clear()
        ele_input.send_keys(new_value)
        ele_input.send_keys(Keys.ENTER)
        # 修改设备密钥时弹出是否确定加密
        if attr_ele_id == 'pf-deviceSecret' and new_value:
            self.driver.implicitly_wait(10)
            sleep(1)
            #提示框信息（偶尔不弹出提示框）
            content=u'您设置的密钥需要加密吗？'
            if self.sj_func_is_tips_display(content):
                if is_sure:
                    self.driver.find_element_by_xpath("//button[contains(text(),'确定')]").click()
                    sleep(1)
                else:
                    self.driver.find_element_by_xpath("//button[@class='btn' and contains(text(),'取消')]").click()
        # 保存
        if is_save:
            ele_save = self.driver.find_element_by_id('save')
            ele_save.click()
        self.driver.implicitly_wait(10)
        log_write(get_current_info() + 'Update device attribute value. attribute id: %s, attibute new value: %s, is save: %s' %(attr_ele_id, new_value, is_save))

    # 从设备面板页面回到当前类型的设备列表
    def sj_panel_back_device_list(self):
        """
        从设备面板页面回到当前类型的设备列表
        :return: None
        """
        WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_id('deviceType_title')).click()
        sleep(0.5)

    # 更新记录
    def sj_panel_change_log(self):
        """
        获取最新一条更新记录
        :return: 列表，最新一条更新记录
        """
        self.driver.find_element_by_id("changelog").click()
        sleep(0.1)
        record = []
        elements = self.driver.find_elements_by_xpath("//tbody[@id='profile-changelist']/tr[1]/td")
        for element in elements:
            record.append(element.text)
        log_write(get_current_info() + 'Get newest change log success. change log is: %s'% record)
        return record

    # 特殊设备（如子系统管理--智慧消防下的设备）进入它的功能
    def sj_panel_function(self, id):
        """
        点击ID元素
        应用：
        1.智慧消防---社区消防站下的设备，在设备的编辑面板页，进入到设备的功能页，如地图，分组，关注等
        2.在设备的功能页，点击移出分组，加入分组，取消关注，关注
        :param id: 功能元素id，如地图分组id为'map'，已加入分组设备为'related'
        :return:None
        """
        self.driver.find_element_by_id(id).click()
        sleep(1)
        log_write(get_current_info() + 'Click element')

    # # 上传图像
    # def sj_panel_upload_icon(self, icon_file, is_submit=True):
    #     """
    #     上传设备图像
    #     :param icon_file:图片文件
    #     :return:None
    #     """
    #     icon_ele = self.driver.find_element_by_id('avatar')
    #     sleep(1)
    #     icon_ele.click()
    #     sleep(1)
    #     self.driver.implicitly_wait(10)
    #     self.driver.find_element_by_name('file-input').send_keys(icon_file)
    #     sleep(1)
    #     if is_submit:
    #         self.driver.find_element_by_xpath("//button[contains(.,'%s')]"% u'提交')
    #         sleep(1)
    #     else:
    #         self.driver.find_element_by_xpath("//button[contains(.,'%s')]" % u'取消')
    #         sleep(1)
    #     return icon_ele

if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get(url)
    print(driver.title)
    print(driver.page_source)
    driver.quit()
