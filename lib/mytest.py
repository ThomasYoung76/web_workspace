# coding: utf-8
import unittest
from lib.page import *
from lib.snatch import SNATCH
from lib.func import execute_sql

class MyUnitTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        log_write('\n---------------------------------------------------------------------------------------\n'
                  '                                     Test Suite Start                                    \n'
                  '-----------------------------------------------------------------------------------------\n')
        # 重新加载testcase表
        sna = SNATCH()
        sna.reload_testcase()
        log_write(get_current_info() + 'Reload testcase success')
        # 实例化PLMS，登陆网页
        cls.plms = PLMS()
        try:
            WebDriverWait(cls.plms.driver, 10).until(lambda x: x.find_element_by_xpath("//img[@id='background']"))
        except:
            log_write(get_current_info() + 'Trigger 407 Error', 'warn')
            # 规避407错误
            cls.plms.driver.back()
            cls.plms.driver.refresh()
            cls.plms.driver.find_element_by_id('password').send_keys(password)
            sleep(1)
            cls.plms.driver.find_element_by_xpath("//button[@class='btn btn-primary block full-width m-b']").click()
            cls.plms.driver.implicitly_wait(10)

        # # 预置数据处理
        # sql = "select id from testcase"
        # test_dev_list = execute_sql(sql)
        # for dev_id in test_dev_list:
        #     dev_id = dev_id[0]
        #     # 进入所有设备列表界面查找设备是否存在
        #     cls.plms.sj_main_to_device_list(0, '公众用户')
        #     cls.plms.driver.find_element_by_xpath(".//*[@id='breadcrumbs']/ul/li[1]/a")
        #     if cls.plms.sj_list_is_device_exist(device_id=dev_id, is_check=True):
        #         # 设备存在则不用新增该设备
        #         log_write(get_current_info() + 'device exsits. do not need to add the device. device id: %s'% dev_id)
        #         pass
        #     else:
        #         # 设备不存在，则在相应类型的设备中新增该设备
        #         log_write(get_current_info() + 'device not exsits. need to add the device first. device id: %s' % dev_id)
        #         sql = "select type_id from testcase where id = '%s'"% dev_id
        #         dev_type_en = execute_sql(sql)[0][0]
        #         sql = "select classes, type from device_type where type_id = '%s'" % dev_type_en
        #         result = execute_sql(sql)
        #         menu_cn = result[0][0]
        #         dev_type_cn = result[0][1]
        #         sql = "select tag from classification where classes = '%s'" % menu_cn
        #         index = int(execute_sql(sql)[0][0])
        #         cls.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        #         cls.plms.sj_list_function('btn_add')
        #         cls.plms.sj_panel_update_attr(attr_ele_id='pf-_id', new_value=dev_id)
        #         cls.plms.sj_panel_update_attr(attr_ele_id='pf-deviceName', new_value='测试设备' + '_%s'%dev_id)
        #         cls.plms.sj_panel_update_attr(attr_ele_id='pf-deviceDesc', new_value='测试设备描述' + '_%s' % dev_id)

    @classmethod
    def tearDownClass(cls):
        cls.plms.driver.quit()
        log_write(get_current_info()+'Quit Browser with %s' % browser)

        log_write('\n---------------------------------------------------------------------------------------\n'
                  '                                     Test Suite End                                    \n'
                  '-----------------------------------------------------------------------------------------\n')