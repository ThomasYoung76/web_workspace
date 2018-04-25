# coding: utf-8
from lib import *
from lib.result import *
import unittest
import random

"""
    实现参数化测试，对测试用例中的参数按功能进行过滤，测试所有设备类型页面拥有的功能
"""


class Device(MyUnitTest):
    """以设备类型为粒度覆盖相应功能的测试"""

    def setUp(self):
        """回到主页"""
        sleep(3)
        log_write(
            get_current_info() + '\n\n---------------------------------  Test Start  ---------------------------------\n')
        self.plms.sj_func_back_main_page()

    def tearDown(self):
        log_write(
            get_current_info() + '\n\n---------------------------------  Test End  ---------------------------------\n')


    @parameterized.expand(input=filter_param('post'))
    @screenshot
    def test_device_copy_01(self, index, menu_en, dev_type_en, device_id):
        """复制设备，直接保存，如果设备中的扩展信息已经存在，则保存失败；如直接保存成功，则删除设备"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        # 复制设备
        new_device_id = self.plms.sj_list_copy_device(device_id)
        # 判断保存成功与否
        if self.plms.sj_func_is_element_enable('changelog'):
            # 回到搜索页面
            print("保存成功")
            self.plms.sj_panel_back_device_list()
            # 检查该设备存在并删除
            self.assertTrue(self.plms.sj_list_del_device_upgrade(new_device_id, count=1, flag_device_id=device_id))
       #判断其扩展信息是否有冲突，冲突则保存失败并给出提示
        else:
            self.plms.driver.find_element_by_id("save").click()
            self.assertTrue(self.plms.driver.find_element_by_class_name('alert-success'))


    #bug,修改ID为已存在的值时，保存未提示失败
    @parameterized.expand(input=filter_param('post'))
    @screenshot
    def test_device_copy_02(self, index, menu_en, dev_type_en, device_id):
        """复制设备，修改设备id为已存在的id，保存失败"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        self.plms.sj_list_copy_device(device_id, is_save=False)
        new_value = device_id
        self.plms.sj_panel_update_attr('pf-_id', new_value)
        #检查扩展字段是否冲突
        if self.plms.sj_func_is_tips_display('扩展字段'):
            pass
        #检查ID是否冲突
        elif self.plms.sj_func_is_tips_display('您输入的ID已存在，请修改后重新保存!'):
            pass


    @parameterized.expand(input=filter_param('post'))
    @screenshot
    def test_device_copy_03(self, index, menu_en, dev_type_en, device_id):
        """复制设备，修改id为未存在的id值"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        new_device_id = self.plms.sj_list_copy_device(device_id, is_save=False)
        new_value = 'YTUI' + device_id
        sleep(2)
        self.plms.sj_panel_update_attr('pf-_id', new_value)
        #保持成功会有'更新记录'，以此判断
        if self.plms.sj_func_is_element_enable('changelog'):
            # 回到搜索页面
            self.plms.sj_panel_back_device_list()
            # 检查该设备存在并删除
            self.assertTrue(self.plms.sj_list_del_device_upgrade(new_value, count=1, flag_device_id=device_id))
        #判断其扩展信息是否有冲突，冲突则保存失败并给出提示
        else:
            self.plms.driver.find_element_by_id("save").click()
            self.assertTrue(self.plms.driver.find_element_by_class_name('alert-success'))


    @parameterized.expand(input=filter_param('post'))
    @screenshot
    def test_device_copy_04(self, index, menu_en, dev_type_en, device_id):
        """复制设备，修改设备名称为空，无法保存"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        self.plms.sj_list_copy_device(device_id, is_save=False)
        self.plms.sj_panel_update_attr('pf-deviceName', '', is_save=False)
        # 检查保存按钮不可用
        self.assertTrue(self.plms.sj_func_is_element_enable('save'))

    @parameterized.expand(input=filter_param('post'))
    @screenshot
    def test_device_copy_05(self, index, menu_en, dev_type_en, device_id):
        """复制设备，修改设备名称，保存成功"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        new_device_id = self.plms.sj_list_copy_device(device_id, is_save=False)
        new_device_name = u'这是一台 复制的设备' + dev_type_cn
        self.plms.sj_panel_update_attr('pf-deviceName', new_device_name)
        if self.plms.sj_func_is_element_enable('changelog'):
            # 检查设备名称正确
            device_name = self.plms.sj_panel_get_attr('pf-deviceName')
            self.assertEqual(device_name, new_device_name)
            # 回到搜索页面
            self.plms.sj_panel_back_device_list()
            # 检查该设备存在并删除
            self.assertTrue(self.plms.sj_list_del_device_upgrade(new_device_id, count=1, flag_device_id=device_id))
            #判断其扩展信息是否有冲突，冲突则保存失败并给出提示
        else:
            self.plms.driver.find_element_by_id("save").click()
            self.assertTrue(self.plms.driver.find_element_by_class_name('alert-success'))

    @parameterized.expand(input=filter_param('post'))
    @screenshot
    def test_device_copy_06(self, index, menu_en, dev_type_en, device_id):
        """复制设备，修改设备描述，保存成功"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        new_device_id = self.plms.sj_list_copy_device(device_id, is_save=False)
        new_device_desc = u'这是一台 复制设备' + dev_type_cn + u'的描述信息'
        self.plms.sj_panel_update_attr('pf-deviceDesc', new_device_desc)
        if self.plms.sj_func_is_element_enable('changelog'):
            # 检查设备描述正确
            device_desc = self.plms.sj_panel_get_attr('pf-deviceDesc')
            self.assertEqual(device_desc, new_device_desc)
            # 回到搜索页面
            self.plms.sj_panel_back_device_list()
            # 检查该设备存在并删除
            self.assertTrue(self.plms.sj_list_del_device_upgrade(new_device_id, count=1, flag_device_id=device_id))
        else:
            self.plms.driver.find_element_by_id("save").click()
            self.assertTrue(self.plms.driver.find_element_by_class_name('alert-success'))

    @parameterized.expand(input=filter_param('post'))
    @screenshot
    def test_device_copy_07(self, index, menu_en, dev_type_en, device_id):
        """复制设备，修改设备描述信息为空，保存成功"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        new_device_id = self.plms.sj_list_copy_device(device_id, is_save=False)
        new_device_desc = ''
        self.plms.sj_panel_update_attr('pf-deviceDesc', new_device_desc)
        if self.plms.sj_func_is_element_enable('changelog'):
            # 检查设备描述正确
            device_desc = self.plms.sj_panel_get_attr('pf-deviceDesc')
            self.assertEqual(device_desc, 'Empty')
            # 回到搜索页面
            self.plms.sj_panel_back_device_list()
            # 检查该设备存在并删除
            self.assertTrue(self.plms.sj_list_del_device_upgrade(new_device_id, count=1, flag_device_id=device_id))
        else:
            self.plms.driver.find_element_by_id("save").click()
            self.assertTrue(self.plms.driver.find_element_by_class_name('alert-success'))

    @parameterized.expand(input=filter_param('post'))
    @screenshot
    def test_device_copy_08(self, index, menu_en, dev_type_en, device_id):
        """复制设备，修改属主为不存在的用户，保存失败  //# bug：保存成功后，有错误信息框弹出"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        new_device_id = self.plms.sj_list_copy_device(device_id, is_save=False)
        owner = '110' + device_id
        sleep(3)
        self.plms.sj_panel_update_attr('pf-ownerDevice_id', owner)
        if self.assertTrue(self.plms.sj_func_is_tips_display('扩展字段')):
            pass
        elif self.assertTrue(self.plms.sj_func_is_tips_display('属主不存在')):
            pass
        else:
            print(False)
        # 搜索新设备，检查该设备存在
        self.plms.sj_func_back_main_page()
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        # 如果该设备存在则删除该设备
        self.plms.sj_list_del_device_upgrade(new_device_id, count=1, flag_device_id=device_id)


    @parameterized.expand(input=filter_param('post'))
    @screenshot
    def test_device_copy_09(self, index, menu_en, dev_type_en, device_id):
        """
        复制设备，修改属主为存在的用户
        属主：为用户，如公众用户、集团用户、监控中心用户
        """
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        sleep(3)
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        new_device_id = self.plms.sj_list_copy_device(device_id, is_save=False)
        owner = user_device_id1
        self.plms.sj_panel_update_attr('pf-ownerDevice_id', owner)
        sleep(2)
        if self.plms.sj_func_is_element_enable('changelog'):
            try:
                # 检查属主修改正确
                device_desc = self.plms.sj_panel_get_attr('pf-ownerDevice_id')
                self.assertEqual(device_desc, owner)
                # 回到搜索页面，检查该设备存在
                self.plms.sj_panel_back_device_list()
                sleep(5)
                self.assertTrue(self.plms.sj_list_until_device_exist(new_device_id))
                # 检查属主已关注该设备
                self.plms.sj_main_to_device_panel(owner, index=0, sub_menu=u'公众用户')
                self.assertTrue(self.plms.sj_list_is_device_exist(new_device_id, 'authorized'))
            finally:
                # 回到主页，重新进入
                self.plms.sj_func_back_main_page()
                self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
                # 删除该设备
                self.plms.sj_list_del_device_upgrade(new_device_id, count=1, flag_device_id=device_id)
            #判断扩展信息是否有冲突
        else:
            self.plms.driver.find_element_by_id("save").click()
            self.assertTrue(self.plms.driver.find_element_by_class_name('alert-success'))


    @parameterized.expand(input=filter_param('post'))
    @screenshot
    def test_device_add_02(self, index, menu_en, dev_type_en, device_id):
        """添加设备，修改ID，名称，描述信息"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        new_device_name = u'这又是一台添加的' + dev_type_cn
        new_device_desc = new_device_name + u'的描述信息'
        new_device_id = '123abc' + device_id
        self.plms.sj_list_add_device(new_device_name, is_save=False)
        self.plms.sj_panel_update_attr('pf-_id', new_device_id, is_save=False)
        self.plms.sj_panel_update_attr('pf-deviceDesc', new_device_desc, is_save=True)
        try:
            # 检查设备名称正确
            device_name = self.plms.sj_panel_get_attr('pf-deviceName')
            device_id = self.plms.sj_panel_get_attr('pf-_id')
            device_desc = self.plms.sj_panel_get_attr('pf-deviceDesc')
            self.assertEqual(device_name, new_device_name)
            self.assertEqual(device_id, new_device_id)
            self.assertEqual(device_desc, new_device_desc)
        finally:
            # 回到搜索页面
            self.plms.sj_panel_back_device_list()
            # 检查该设备存在并删除
            self.assertTrue(self.plms.sj_list_del_device_upgrade(new_device_id, count=1, flag_device_id=device_id))


    @parameterized.expand(input=filter_param('post'))
    @screenshot
    def test_device_add_03(self, index, menu_en, dev_type_en, device_id):
        """添加设备，修改属主不存在，失败  //bug：未提示'属主不存在' """
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        sleep(3)
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        new_device_name = u'这又是一台添加的' + dev_type_cn
        device_owner = ''
        new_device_id = self.plms.sj_list_add_device(new_device_name, is_save=False)
        self.plms.sj_panel_update_attr('pf-ownerDevice_id', device_owner, is_save=True)
        try:
            content = u'属主不存在'
            self.assertTrue(self.plms.sj_func_is_tips_display(content))
        except AssertionError as msg:
            # 回到搜索页面
            self.plms.sj_panel_back_device_list()
            # 如果该设备存在则删除该设备
            self.plms.sj_list_del_device_upgrade(new_device_id, count=1, is_last_page=True,flag_device_id=device_id)
            raise AssertionError

    @parameterized.expand(input=filter_param('export'))
    @screenshot
    def test_device_export_01(self, index, menu_en, dev_type_en, device_id):
        """导出单个设备的txt格式//bug:暂时不支持勾选设备后直接导出"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        self.plms.sj_list_is_device_exist(device_id, is_check=False)
        self.plms.sj_list_select_device()
        # 导出
        self.plms.sj_list_export_device(exp_is_excel=False)    #网站暂时未实行
        # 检查导出的数据
        export_file = scan_dir(SJ_DOCS, 'txt')
        device_list = get_txt_data(export_file)
        self.assertTrue(device_id in device_list[0])
        self.assertTrue(self.plms.sj_list_export_device(exp_is_excel=False))

    @parameterized.expand(input=filter_param('export'))
    @screenshot
    def test_device_export_02(self, index, menu_en, dev_type_en, device_id):
        """导出单个设备的excel格式//bug:暂时不支持勾选设备后直接导出"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        self.plms.sj_list_is_device_exist(device_id, is_check=False)
        self.plms.sj_list_select_device()
        # 导出
        self.plms.sj_list_export_device(exp_is_excel=True)
        # 检查导出的数据
        export_file = scan_dir(SJ_DOCS, 'xlsx')
        device_list = get_excel_data(export_file)
        self.assertTrue(device_id in device_list[0])

    @parameterized.expand(input=filter_param('export'))
    @screenshot
    def test_device_export_03(self, index, menu_en, dev_type_en, device_id):
        """不选中任何设备直接导出excel失败"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        # 导出
        self.plms.sj_list_export_device(exp_is_excel=True, sleep_time=0)
        # 检查导出失败的提示
        self.assertTrue(self.plms.sj_func_is_tips_display(u'请填写导出条件！'))
        sleep(0.5)

    @parameterized.expand(input=filter_param('export'))
    @screenshot
    def test_device_export_04(self, index, menu_en, dev_type_en, device_id):
        """不选中设备直接导出txt失败，需要输入条件"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        self.plms.sj_list_export_device(exp_is_excel=False, sleep_time=0)
        # 提示导出失败，条件不能为空
        content = u'请填写导出条件！'
        self.assertTrue(self.plms.sj_func_is_tips_display(content))

    @parameterized.expand(input=filter_param('export'))
    @screenshot
    def test_device_export_05(self, index, menu_en, dev_type_en, device_id):
        """导出当页所有数据的excel文件//bug:暂时不支持勾选设备后直接导出"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        self.plms.sj_list_select_device(0)
        # 导出
        self.plms.sj_list_export_device(exp_is_excel=True)
        # 检查导出的数据
        export_file = scan_dir(SJ_DOCS, 'xlsx')
        dev_list_excel = get_excel_data(export_file)
        # 获取文件中的设备id
        dev_id_excel = []
        for row in dev_list_excel:
            dev_id_excel.append(row[2])
        # 获取页面中设备id
        dev_list_page = self.plms.sj_list_scan_device()
        dev_id_page = []
        for row in dev_list_page:
            dev_id_page.append(row[0])
        # 断言两个id列表中id元素相等
        self.assertEqual(set(dev_id_excel), set(dev_id_page))

    #bug:txt和excel导出的数据内容格式没有对齐
    @parameterized.expand(input=filter_param('export'))
    @screenshot
    def test_device_export_06(self, index, menu_en, dev_type_en, device_id):
        """导出当页所有数据的txt文件//bug暂时不支持直接勾选设备进行导出"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn, )
        self.plms.sj_list_select_device(0)
        # 导出
        if self.plms.sj_list_export_device(exp_is_excel=False):
            # 检查导出的数据
            export_file = scan_dir(SJ_DOCS, 'txt')
            dev_list_txt = get_txt_data(export_file)
            # 获取文件中的设备id
            dev_id_txt = []
            for row in dev_list_txt:
                dev_id_txt.append(row[1])
            # 获取页面中设备id
            dev_list_page = self.plms.sj_list_scan_device()
            dev_id_page = []
            for row in dev_list_page:
                dev_id_page.append(row[0])
            # 断言两个id列表中id元素相等
            self.assertEqual(set(dev_id_txt), set(dev_id_page))
        else:
            self.assertTrue(self.plms.sj_list_export_device(exp_is_excel=False))

    # bug：无法跨页选中设备
    @parameterized.expand(input=filter_param('export'))
    @screenshot
    def test_device_export_07(self, index, menu_en, dev_type_en, device_id):
        """跨页导出全部设备数据的excel格式 //bug暂时不支持直接勾选设备进行导出"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        page_count = self.plms.sj_list_pagenation(5, is_click=False)
        for i in range(page_count):
            self.plms.sj_list_select_device(0)
            self.plms.sj_list_pagenation(4, is_click=True)      # 点击下一页
        # 导出
        self.plms.sj_list_export_device(exp_is_excel=True)
        # 检查导出的数据
        export_file = scan_dir(SJ_DOCS, 'xlsx')
        dev_list_excel = get_excel_data(export_file)
        # 获取文件中的设备id
        dev_id_excel = []
        for row in dev_list_excel:
            dev_id_excel.append(row[1])
        # 获取页面中设备id
        self.plms.sj_func_back_main_page()
        self.plms.sj_main_to_device_list(1, u'消防设备', u'无线报警主机')
        dev_list_page = self.plms.sj_list_scan_device(is_all_page=True)
        dev_id_page = []
        for row in dev_list_page:
            dev_id_page.append(row[0])
        # 断言两个id列表中id元素相等
        self.assertEqual(set(dev_id_excel), set(dev_id_page))

    # bug：无法跨页选中设备
    @parameterized.expand(input=filter_param('export'))
    @screenshot
    def test_device_export_08(self, index, menu_en, dev_type_en, device_id):
        """跨页导出全部设备数据的txt格式 //bug：暂时不支持直接勾选设备进行导出"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        page_count = self.plms.sj_list_pagenation(5, is_click=False)
        for i in range(page_count):
            self.plms.sj_list_select_device(0)
            self.plms.sj_list_pagenation(4, is_click=True)  # 点击下一页
        # 导出
        self.plms.sj_list_export_device(exp_is_excel=False)
        # 检查导出的数据
        export_file = scan_dir(SJ_DOCS, 'txt')
        dev_list_txt = get_txt_data(export_file)
        # 获取txt中的设备id
        dev_id_txt = []
        for row in dev_list_txt:
            dev_id_txt.append(row[1])
        # 获取页面中设备id
        self.plms.sj_func_back_main_page()
        sleep(0.5)
        self.plms.sj_main_to_device_list(1, u'消防设备', u'无线报警主机')
        dev_list_page = self.plms.sj_list_scan_device(is_all_page=True)
        dev_id_page = []
        for row in dev_list_page:
            dev_id_page.append(row[0])
        # 断言两个id列表中id元素相等
        self.assertEquals(set(dev_id_txt), set(dev_id_page))

    @parameterized.expand(input=filter_param('export'))
    @screenshot
    def test_device_export_09(self, index, menu_en, dev_type_en, device_id):
        """按条件批量导出全部10台JB-QBL-IPC设备到excel，浏览器需要设置自动下载保存xlsx文件和存放目录至os.path.join(SJ_DOCS, 'export')"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn =execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        #下面数据为测试前通过批量生成和设置的batch_num批次号提前加入的数据
        self.plms.sj_list_export_device(dev_type='JB-QBL-IPC', batch_num=batch_num, exp_count=10, exp_is_excel=True)
        print (1)
        # 检查导出的数据
        sleep(3)
        export_file = scan_dir(os.path.join(SJ_DOCS, 'export'), 'xls')
        print (export_file)
        dev_list_excel = get_excel_data(export_file)
        print (2)
        print (dev_list_excel)
        sleep(1)
        # 获取文件中的设备id
        dev_id_excel = []
        for row in dev_list_excel[1:]:
            dev_id_excel.append(row[0])
        # 获取页面中设备id
        self.plms.sj_func_back_main_page()
        sleep(0.5)
        self.plms.sj_main_to_device_list(1, u'消防设备', u'建安消防控制器')
        self.plms.sj_list_is_device_exist(batch_num, is_check=False)
        dev_list_page = self.plms.sj_list_scan_device(is_all_page=False)
        dev_id_page = []
        for row in dev_list_page:
            dev_id_page.append(row[0])
        # 断言excel中id与当前页的id相等
        self.assertEqual(set(dev_id_excel), set(dev_id_page))

    @parameterized.expand(input=filter_param('export'))
    @screenshot
    def test_device_export_10(self, index, menu_en, dev_type_en, device_id):
        """按条件批量导出全部10台JB-QBL-IPC设备到txt，浏览器需要设置为自动下载txt文件"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        self.plms.sj_list_export_device(dev_type='JB-QBL-IPC', batch_num=batch_num, exp_count=10, exp_is_excel=False)
        # 检查导出的数据
        export_file = scan_dir(os.path.join(SJ_DOCS,'export'), 'txt')
        sleep(2)
        dev_list_excel = get_txt_data(export_file)
        # 获取文件中的设备id
        dev_id_txt = []
        for row in dev_list_excel[1:]:
            dev_id_txt.append(row[0])
        # 获取页面中设备id
        self.plms.sj_func_back_main_page()
        sleep(0.5)
        self.plms.sj_main_to_device_list(1, u'消防设备', u'建安消防控制器')
        self.plms.sj_list_is_device_exist(batch_num, is_check=False)
        dev_list_page = self.plms.sj_list_scan_device(is_all_page=False)
        dev_id_page = []
        for row in dev_list_page:
            dev_id_page.append(row[0])
        # 断言两个id列表中id元素相等
        self.assertEquals(set(dev_id_txt), set(dev_id_page))

    @parameterized.expand(input=filter_param('export'))
    @screenshot
    def test_device_export_11(self, index, menu_en, dev_type_en, device_id):
        """批量导出时设备类型为空时导出失败"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        self.plms.sj_list_export_device(dev_type=None, batch_num=batch_num, exp_count=10, sleep_time=0)
        content = u'请填写导出条件！'
        self.assertTrue(self.plms.sj_func_is_tips_display(content))

    @parameterized.expand(input=filter_param('export'))
    @screenshot
    def test_device_export_12(self, index, menu_en, dev_type_en, device_id):
        """批量导出时设备批次为空时导出失败"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        self.plms.sj_list_export_device(dev_type=dev_type_en, batch_num=None, exp_count=10, sleep_time=0)
        content = u'请填写导出条件！'
        self.assertTrue(self.plms.sj_func_is_tips_display(content))

    @parameterized.expand(input=filter_param('export'))
    @screenshot
    def test_device_export_13(self, index, menu_en, dev_type_en, device_id):
        """导出设备中不存在的批次失败，提示友好
        // bug：未有正确的提示，且会跳转出一个新的页面，提示message:未找到该设备"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        self.plms.sj_list_export_device(dev_type=dev_type_en, batch_num=123456788, exp_count=10, sleep_time=0)
        content = u'批次不存在，请重新输入！'
        self.assertTrue(self.plms.sj_func_is_tips_display(content))


    @parameterized.expand(input=filter_param('export'))
    @screenshot
    def test_device_export_14(self, index, menu_en, dev_type_en, device_id):
       """设置批次号导入3台设备，按批次号导出，导出个数为空，设备全部被导出
       //bug：已选择设备类型，导入excel表格依旧提示选择设备类型或者弹出错误提示框"""
       sql = "select classes from classification where id = '%s'" % menu_en
       menu_cn = execute_sql(sql)[0][0]
       sql = "select type from device_type where type_id = '%s'" % dev_type_en
       dev_type_cn = execute_sql(sql)[0][0]
       self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
       sleep(1)
       # 按批次号导入设备
       file_path = os.path.join(SJ_DOCS, 'import') + os.sep + 'test_import_3.xlsx'
       # 从excel文件中获取导入的设备
       dev_id_imp = get_excel_data(file_path, 1)
       dev_id_imp.pop(0)  # 去掉第一个为空的数据
       #  从数据库中获取
       self.plms.sj_list_function('btn_imp')
       #excel表格数据无法被导入，后面操作无法执行
       self.plms.sj_list_import_device(dev_type=dev_type_en, dev_name=u'自动化测试导入的数据', upload_file=True,file_path=file_path,dev_batch='20170602')
       self.plms.sj_list_export_device(dev_type=dev_type_en, batch_num='20170602', exp_count=None, exp_is_excel=True, sleep_time=3)
       # 检查导出的数据，获取导出文件中的设备ID
       export_file = scan_dir(SJ_DOCS, 'xlsx')
       dev_id_exp = get_excel_data(export_file, 2)
       # 检查结果，并恢复数据
       for dev_id_addr in dev_id_imp:
           try:
               # 检查导入的数据均被导出
               for dev_id in dev_id_exp:
                   if dev_id_addr in dev_id:
                       self.assertTrue(True)
                       break
           finally:
               # 清除导入的数据
               self.plms.sj_func_refresh()
               self.assertTrue(self.plms.sj_list_del_device_upgrade(dev_id_addr, count=1, is_last_page=False, flag_device_id=device_id))

    @parameterized.expand(input=filter_param('import'))
    @screenshot
    def test_device_import_01(self, index, menu_en, dev_type_en, device_id):
        """只填必填字段，导入5个完整的设备成功"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        sleep(1)
        file_path = os.path.join(SJ_DOCS, 'import') + os.sep + 'test_import_5.xlsx'
        # 从excel文件中获取导入的设备ID
        dev_id_list = get_excel_data(file_path, 1)
        dev_id_list.pop(0)  # 去掉第一个为空的数据
        self.plms.sj_list_function('btn_imp')
        self.plms.sj_list_import_device(dev_type=dev_type_en, dev_name=u'自动化测试导入的数据', upload_file=file_path)
        # 检查导入成功
        try:
            content = 'devices have been imported and generated'
            self.assertTrue(self.plms.sj_func_is_tips_display(content))
            sleep(1)
        finally:
            # 将导入的数据逐个删除
            self.plms.sj_func_refresh()
            for dev_id in dev_id_list:
                self.assertTrue(
                    self.plms.sj_list_del_device_upgrade(dev_id, count=1, is_last_page=False, flag_device_id=device_id))

    @parameterized.expand(input=filter_param('import'))
    @screenshot
    def test_device_import_02(self, index, menu_en, dev_type_en, device_id):
        """设置批次号，导入12个设备成功  """
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        sleep(1)
        file_path = os.path.join(SJ_DOCS, 'import') + os.sep + 'test_import_12.xlsx'
        # 从excel文件中获取导入的设备ID
        dev_id_list = get_excel_data(file_path, 1)
        dev_id_list.pop(0)  # 去掉第一行
        self.plms.sj_list_function('btn_imp')
        self.plms.sj_list_import_device(dev_type=dev_type_en, dev_name=u'自动化测试导入的数据',upload_file=file_path)
        # 检查导入成功
        try:
            content = 'devices have been imported and generated'
            self.assertTrue(self.plms.sj_func_is_tips_display(content))
            sleep(1)
        finally:
            # 将导入的数据逐个删除
            # self.plms.sj_func_refresh()
            for dev_id in dev_id_list:
                self.plms.sj_func_refresh() # 每次删除都需要刷新页面才能保证成功，放这里规避问题
                self.assertTrue(self.plms.sj_list_del_device_upgrade(dev_id, count=1, is_last_page=False, flag_device_id=device_id))

    @parameterized.expand(input=filter_param('import'))
    @screenshot
    def test_device_import_03(self, index, menu_en, dev_type_en, device_id):
        """导入5个设备并设置属主，成功  //bug属主为设置失败"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        sleep(1)
        file_path = os.path.join(SJ_DOCS, 'import') + os.sep + 'test_import_5.xlsx'
        # 从excel文件中获取导入的设备ID
        dev_id_list = get_excel_data(file_path, 1)
        dev_id_list.pop(0)  # 去掉第一个为空的数据
        self.plms.sj_list_function('btn_imp')
        self.plms.sj_list_import_device(dev_type=dev_type_en, dev_name=u'自动化测试导入的数据', dev_owner=user_device_id1, upload_file=file_path)
        # 检查导入成功
        try:
            content = 'devices have been imported and generated'
            self.assertTrue(self.plms.sj_func_is_tips_display(content))
            sleep(1)
            # 检查设备的属主
            self.plms.sj_list_pagenation(5, is_click=True)
            self.plms.sj_list_edit_device(index=-1)
            owner = self.plms.sj_panel_get_attr('pf-ownerDevice_id')
            self.assertEqual(owner, user_device_id1)
        finally:
            # 将导入的数据逐个删除
            sleep(1)
            self.plms.sj_panel_back_device_list()
            # self.plms.sj_func_refresh()
            for dev_id in dev_id_list:
                self.plms.sj_func_refresh()
                self.assertTrue(self.plms.sj_list_del_device_upgrade(dev_id, count=1, is_last_page=False, flag_device_id=device_id))

    @parameterized.expand(input=filter_param('import'))
    @screenshot
    def test_device_import_04(self, index, menu_en, dev_type_en, device_id):
        """导入3个设备，同时设置属主和分组，成功"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        sleep(1)
        file_path = os.path.join(SJ_DOCS, 'import') + os.sep + 'test_import_3.xlsx'
        # 从excel文件中获取导入的设备ID
        dev_id_list = get_excel_data(file_path, 1)
        dev_id_list.pop(0)  # 去掉第一行
        sql = "select type_id from device_type where type='%s'" % dev_type_cn
        dev_type_en = execute_sql(sql)[0][0]
        self.plms.sj_list_function('btn_imp')
        self.plms.sj_list_import_device(dev_type=dev_type_en, dev_name=u'自动化测试导入的数据', virtual_dev=comm_device_id, dev_owner=user_device_id1, upload_file=file_path)
        # 检查导入成功
        try:
            content = 'devices have been imported and generated'
            self.assertTrue(self.plms.sj_func_is_tips_display(content))
            sleep(1)
            # 检查设备的属主
            self.plms.sj_list_pagenation(5, is_click=True)
            self.plms.sj_list_edit_device(index=-1)
            owner = self.plms.sj_panel_get_attr('pf-ownerDevice_id')
            self.assertEqual(owner, user_device_id1)
            # 检查设备加入分组成功
            self.plms.sj_func_back_main_page()
            self.plms.sj_main_to_device_panel(comm_device_id, 2, '智慧消防', '社区消防站')
            self.plms.sj_panel_function('related')  # 查看已加入分组设备
            dev_id_scan = self.plms.sj_list_scan_page(2, 3)
            # dev_id_list中的每一个元素都分别是dev_id_scan中元素的子串
            result = []
            for dev_key in dev_id_list:
                for dev_id in dev_id_scan:
                    result.append(dev_key in dev_id)
                # result有一个True则为True
                self.assertTrue(any(result))
        finally:
            # 回到主页，重新进入页面并清楚数据
            self.plms.sj_func_back_main_page()
            self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
            # 将导入的数据逐个删除
            for dev_id in dev_id_list:
                self.plms.sj_func_refresh()
                self.assertTrue(self.plms.sj_list_del_device_upgrade(dev_id, count=1, is_last_page=False, flag_device_id=device_id))

    @parameterized.expand(input=filter_param('import'))
    @screenshot
    def test_device_import_05(self, index, menu_en, dev_type_en, device_id):
        """分组导入5个设备成功"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        sleep(1)
        file_path = os.path.join(SJ_DOCS, 'import') + os.sep + 'test_import_5.xlsx'
        # 从excel文件中获取导入的设备ID
        dev_id_list = get_excel_data(file_path, 1)
        dev_id_list.pop(0)  # 去掉第一个为空的数据
        self.plms.sj_list_function('btn_imp')
        self.plms.sj_list_import_device(dev_type=dev_type_en, dev_name=u'自动化测试导入的数据', virtual_dev=comm_device_id, upload_file=file_path)
        # 检查导入成功
        try:
            content = 'devices have been imported and generated'
            self.assertTrue(self.plms.sj_func_is_tips_display(content))
            sleep(1)
            # 检查设备加入分组成功
            self.plms.sj_func_back_main_page()
            self.plms.sj_main_to_device_panel(comm_device_id, 2, '智慧消防', '社区消防站')
            self.plms.sj_panel_function('related')  # 查看已加入分组设备
            dev_id_scan = self.plms.sj_list_scan_page(2, 3)
            # dev_id_list中的每一个元素都分别是dev_id_scan中元素的子串
            result = []
            for dev_key in dev_id_list:
                for dev_id in dev_id_scan:
                    result.append(dev_key in dev_id)
                # result有一个True则为True
                self.assertTrue(any(result))
        finally:
            # 回到主页，重新进入页面并清除数据
            self.plms.sj_func_back_main_page()
            self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
            # 将导入的数据逐个删除
            for dev_id in dev_id_list:
                self.plms.sj_func_refresh()
                self.assertTrue(self.plms.sj_list_del_device_upgrade(dev_id, count=1, is_last_page=False, flag_device_id=device_id))

    @parameterized.expand(input=filter_param('import'))
    @screenshot
    def test_device_import_06(self, index, menu_en, dev_type_en, device_id):
        """导入设备，不上传文件，导入失败，提示合理"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        sleep(1)
        file_path = os.path.join(SJ_DOCS, 'import') + os.sep + 'test_import_3.xlsx'
        self.plms.sj_list_function('btn_imp')
        self.plms.sj_list_import_device(dev_type=dev_type_en, dev_name=u'自动化测试导入的数据')
        # 检查导入失败，提示合理
        content = u'设备类型未选择，设备名称未输入或者excel文件未上传!'
        self.assertTrue(self.plms.sj_func_is_tips_display(content))

    @parameterized.expand(input=filter_param('import'))
    @screenshot
    def test_device_import_07(self, index, menu_en, dev_type_en, device_id):
        """导入设备，上传文件内容未空"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        sleep(1)
        file_path = os.path.join(SJ_DOCS, 'import') + os.sep + 'test_import_0.xlsx'
        # 从excel文件中获取导入的设备ID
        dev_id_list = get_excel_data(file_path, 1)
        sql = "select type_id from device_type where type='%s'" % dev_type_cn
        dev_type_en = execute_sql(sql)[0][0]
        self.plms.sj_list_function('btn_imp')
        self.plms.sj_list_import_device(dev_type=dev_type_en, dev_name=u'自动化测试导入的数据', upload_file=file_path)
        # 检查导入0个设备
        content = 'devices have been imported and generated'
        self.assertTrue(self.plms.sj_func_is_tips_display(content))


    @parameterized.expand(input=filter_param('import'))
    @screenshot
    def test_device_import_08(self, index, menu_en, dev_type_en, device_id):
        """不上传文件，导入失败，不刷新页面，再次上传文件导入成功"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        sleep(1)
        file_path = os.path.join(SJ_DOCS, 'import') + os.sep + 'test_import_3.xlsx'
        # 从excel文件中获取导入的设备ID
        dev_id_list = get_excel_data(file_path, 1)
        dev_id_list.pop(0)  # 去掉第一个为空的数据
        self.plms.sj_list_function('btn_imp')
        self.plms.sj_list_import_device(dev_type=dev_type_en, dev_name=u'自动化测试导入的数据')
        # 检查导入失败，提示合理
        content = u'设备类型未选择，设备名称未输入或者excel文件未上传'
        self.assertTrue(self.plms.sj_func_is_tips_display(content))
        sleep(1)
        # 再次导入
        self.plms.sj_list_function('btn_imp')
        self.plms.sj_list_import_device(dev_type=dev_type_en, dev_name=u'自动化测试导入的数据', upload_file=file_path)
        # 检查导入成功
        try:
            content = 'devices have been imported and generated'
            self.assertTrue(self.plms.sj_func_is_tips_display(content))
            sleep(1)
        finally:
            # 将导入的数据逐个删除
            for dev_id in dev_id_list:
                self.plms.sj_func_refresh()
                self.assertTrue(self.plms.sj_list_del_device_upgrade(dev_id, count=1, is_last_page=False, flag_device_id=device_id))

    @parameterized.expand(input=filter_param('batch'))
    @screenshot
    def test_device_gen_01(self, index, menu_en, dev_type_en, device_id):
        """批量生成5台无线报警设备"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        sleep(1)
        #默认生成的批次号根据当前系统时间自动生成，如当前时间为18年4月23号，则批次号会顺序生成为1804230、1804231
        batch_num = time.strftime("%Y%m%d")[2:]
        total_num = 5
        self.plms.sj_list_gen_device(total_count=total_num, dev_type=dev_type_en,\
                                     dev_name=u'批量生成的测试设备', )
        try:
            # 检查批量生成的设备成功
            # content = '%d new devices have been generated in batches successfully' % total_num
            content='devices'
            self.assertTrue(self.plms.sj_func_is_tips_display(content))
        finally:
            # 删除生成的设备
            self.plms.sj_func_back_main_page()
            self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
            self.plms.sj_list_del_device_upgrade(device_key=batch_num,count=total_num, is_last_page=False,\
                                                 flag_device_id=device_id)


    @parameterized.expand(input=filter_param('batch'))
    @screenshot
    def test_device_gen_02(self, index, menu_en, dev_type_en, device_id):
        """个数为空，批量生成设备失败"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        sleep(1)
        sql = "select type_id from device_type where type='%s'" % dev_type_cn
        dev_type_en = execute_sql(sql)[0][0]
        self.plms.sj_list_gen_device(total_count=None, dev_type=dev_type_en, dev_name=u'批量生成的测试设备', )
        content = '输入框内容都不能为空，其中设备属主为选填!'
        self.assertTrue(self.plms.sj_func_is_tips_display(content))

    @parameterized.expand(input=filter_param('batch'))
    @screenshot
    def test_device_gen_03(self, index, menu_en, dev_type_en, device_id):
        """设备类型为空，批量生成设备失败"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        sleep(1)
        self.plms.sj_list_gen_device(total_count=5, dev_type=None, dev_name=u'批量生成的测试设备', )
        content = '输入框内容都不能为空，其中设备属主为选填!'
        self.assertTrue(self.plms.sj_func_is_tips_display(content))

    @parameterized.expand(input=filter_param('batch'))
    @screenshot
    def test_device_gen_04(self, index, menu_en, dev_type_en, device_id):
        """设备名称为空，批量生成设备失败"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        sleep(1)
        self.plms.sj_list_gen_device(total_count=5, dev_type=dev_type_en, dev_name=None)
        content = '输入框内容都不能为空，其中设备属主为选填!'
        self.assertTrue(self.plms.sj_func_is_tips_display(content))

    @parameterized.expand(input=filter_param('batch'))
    @screenshot
    def test_device_gen_5(self, index, menu_en, dev_type_en, device_id):
        """设置属主为user_device_id1，批量生成设备成功且设备属主均正确  //bug生成失败，待确定具体准确的生成条件"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        sleep(1)
        batch_num = time.strftime("%Y%m%d")[2:]
        total_count = 6
        self.plms.sj_list_gen_device(total_count=total_count, dev_type=dev_type_en,\
                                     dev_name=u'批量生成的测试设备', dev_owner=user_device_id1)
        try:
            # 检查批量生成的最后一个设备的属主
            self.plms.sj_func_refresh()
            self.plms.sj_list_pagenation(5)  # 翻到最后一页
            self.plms.sj_list_edit_device(-1)
            self.assertEqual(self.plms.sj_panel_get_attr("pf-ownerDevice_id"), user_device_id1)
        finally:
            # 检查并删除生成的设备
            sleep(1)
            self.plms.sj_func_back_main_page()
            self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
            self.plms.sj_list_del_device_upgrade(batch_num, count=total_count, is_last_page=False,\
                                                 flag_device_id=device_id)

    @parameterized.expand(input=filter_param('put'))
    @screenshot
    def test_device_edit_01(self, index, menu_en, dev_type_en, device_id):
        """修改属主成功，属主自动关注该设备"""
        # 修改设备alarm_host_id的属主为user_device_id1
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
        sleep(1)
        self.plms.sj_panel_update_attr('pf-ownerDevice_id', user_device_id1)
        sleep(1)
        self.plms.sj_func_back_main_page()
        try:
            # 检查用户user_device_id1已关注alarm_host_id
            self.plms.sj_main_to_device_panel(user_device_id1, index=0, sub_menu=u'公众用户')
            sleep(1)
            self.assertTrue(self.plms.sj_list_is_device_exist(device_id, 'authorized'))
        finally:
            # 还原环境，属主修改为空
            self.plms.sj_func_back_main_page()
            self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
            sleep(1)
            self.plms.sj_panel_update_attr('pf-ownerDevice_id', '')

    @parameterized.expand(input=filter_param('put'))
    @screenshot
    def test_device_edit_02(self, index, menu_en, dev_type_en, device_id):
        """设备的属主从用户1直接修改为用户2//bug,修改属主从1变为2时应该提示：请先取消已有属主的关注，实际只显示了一个错误信息"""
        # 设备的属主修改为用户1
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
        self.plms.sj_panel_update_attr('pf-ownerDevice_id', user_device_id1)
        # 设备的属主从用户1修改用户2
        self.plms.sj_panel_update_attr('pf-ownerDevice_id', user_device_id2)
        #提示内容暂自己设定
        content = '请先取消该属主关注，再进行修改'
        self.assertTrue(self.plms.sj_func_is_tips_display(content))
        try:
            # 检查用户1没有关注该设备
            self.plms.sj_func_back_main_page()
            self.plms.sj_main_to_device_panel(user_device_id1, index=0, sub_menu=u'公众用户')
            self.assertFalse(self.plms.sj_list_is_device_exist(alarm_host_id, 'observed'))    # bug未修复
            self.assertFalse(self.plms.sj_list_is_device_exist(alarm_host_id, 'authorized'))
            # 检查用户2关注了该设备
            self.plms.sj_func_back_main_page()
            self.plms.sj_main_to_device_panel(user_device_id2, index=0, sub_menu=u'公众用户')
            self.assertTrue(self.plms.sj_list_is_device_exist(alarm_host_id, 'observed'))
            self.assertTrue(self.plms.sj_list_is_device_exist(alarm_host_id, 'authorized'))
        finally:
            # 还原环境，属主修改为空
            self.plms.sj_func_back_main_page()
            self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
            self.plms.sj_panel_update_attr('pf-ownerDevice_id', '')


    @parameterized.expand(input=filter_param('put'))
    @screenshot
    def test_device_edit_03(self, index, menu_en, dev_type_en, device_id):
        """修改的属主不存在，提示失败信息，修改失败 //bug未提示修改失败提示框，仅弹出一个错误信息"""
        # 修改设备alarm_host_id的属主为'yangyangyang'
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
        owner = 'yanga' + device_id
        self.plms.sj_panel_update_attr('pf-ownerDevice_id', owner)
        try:
            content = u'属主不存在，修改失败'
            self.assertTrue(self.plms.sj_func_is_tips_display(content), u'提示不存在或者不合理')
        except:
            # 还原环境，属主修改为空
            self.plms.sj_func_back_main_page()
            self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
            self.plms.sj_panel_update_attr('pf-ownerDevice_id', '')
            raise AssertionError('owner is not exist, should not be modified success')

    @parameterized.expand(input=filter_param('put'))
    @screenshot
    def test_device_edit_04(self, index, menu_en, dev_type_en, device_id):
        """修改设备加密方式为不加密"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
        self.plms.sj_panel_update_attr(attr_ele_id='pf-encrypt', new_value='false')
        # 检查修改正确
        self.assertEqual(self.plms.sj_panel_get_attr('pf-encrypt'), u'Empty')

    @parameterized.expand(input=filter_param('put'))
    @screenshot
    def test_device_edit_05(self, index, menu_en, dev_type_en, device_id):
        """修改设备加密方式为aes-128-ecb"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
        self.plms.sj_panel_update_attr('pf-encrypt', new_value="aes-128-ecb")
        # 检查更新记录
        self.plms.sj_func_refresh()
        record = self.plms.sj_panel_change_log()
        self.assertEqual(record[0], username)
        self.assertEqual(record[2], u'加密方式')
        self.assertEqual(record[4], u'aes-128-ecb')
        # 还原加密方式为不加密
        self.plms.sj_panel_update_attr('pf-encrypt', new_value="false")

    @parameterized.expand(input=filter_param('put'))
    @screenshot
    def test_device_edit_06(self, index, menu_en, dev_type_en, device_id):
        """修改设备密钥为空提示错误"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
        self.plms.sj_panel_update_attr('pf-deviceSecret', new_value='', is_save=False)
        content = u'设备密钥不能为空，请设置密钥!'
        self.assertTrue(self.plms.sj_func_is_tips_display(content))

    @parameterized.expand(input=filter_param('put'))
    @screenshot
    def test_device_edit_07(self, index, menu_en, dev_type_en, device_id):
        """修改设备密钥且密钥不加密"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
        attr_id = 'pf-deviceSecret'
        raw_value = self.plms.sj_panel_get_attr(attr_id)
        new_value = 'abcdef' + device_id
        self.plms.sj_panel_update_attr(attr_id, new_value)
        try:
            # 检查修改成功
            self.assertEqual(self.plms.sj_panel_get_attr(attr_id), new_value)
        finally:
            # 属性值还原
            self.plms.sj_panel_update_attr(attr_id, raw_value, is_sure=False)

    @parameterized.expand(input=filter_param('put'))
    @screenshot
    def test_device_edit_08(self, index, menu_en, dev_type_en, device_id):
        """修改设备密钥且密钥加密"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
        attr_id = 'pf-deviceSecret'
        raw_value = self.plms.sj_panel_get_attr(attr_id)
        new_value = 'abcdef34'
        self.plms.sj_panel_update_attr(attr_id, new_value, is_sure=True)
        try:
            # 检查修改成功
            self.assertNotEqual(self.plms.sj_panel_get_attr(attr_id), new_value)
        finally:
            # 属性值还原
            self.plms.sj_panel_update_attr(attr_id,new_value=raw_value, is_sure=True)

    @parameterized.expand(input=filter_param('put'))
    @screenshot
    def test_device_edit_09(self, index, menu_en, dev_type_en, device_id):
        """修改设备名称为空成功"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
        attr_id = 'pf-deviceName'
        raw_value = self.plms.sj_panel_get_attr(attr_id)
        new_value = ''
        self.plms.sj_panel_update_attr(attr_id, new_value)
        try:
            # 检查修改成功
            self.assertEqual(self.plms.sj_panel_get_attr(attr_id), 'Empty')
        finally:
            # 属性值还原
            self.plms.sj_panel_update_attr(attr_id, raw_value)

    @parameterized.expand(input=filter_param('put'))
    @screenshot
    def test_device_edit_10(self, index, menu_en, dev_type_en, device_id):
        """修改设备名称为其他值正常"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
        attr_id = 'pf-deviceName'
        raw_value = self.plms.sj_panel_get_attr(attr_id)
        new_value = 'abc_' + device_id
        self.plms.sj_panel_update_attr(attr_id, new_value)
        try:
            # 检查修改成功
            self.assertEqual(self.plms.sj_panel_get_attr(attr_id), new_value)
        finally:
            # 属性值还原
            self.plms.sj_panel_update_attr(attr_id, raw_value)

    @parameterized.expand(input=filter_param('put'))
    @screenshot
    def test_device_edit_11(self, index, menu_en, dev_type_en, device_id):
        """修改设备描述为空正常"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
        attr_id = 'pf-deviceDesc'
        raw_value = self.plms.sj_panel_get_attr(attr_id)
        new_value = ''
        self.plms.sj_panel_update_attr(attr_id, new_value)
        try:
            # 检查修改成功
            self.assertEqual(self.plms.sj_panel_get_attr(attr_id), 'Empty')
        finally:
            # 属性值还原
            self.plms.sj_panel_update_attr(attr_id, raw_value)

    @parameterized.expand(input=filter_param('put'))
    @screenshot
    def test_device_edit_12(self, index, menu_en, dev_type_en, device_id):
        """修改设备描述为其他值正常"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
        attr_id = 'pf-deviceDesc'
        raw_value = self.plms.sj_panel_get_attr(attr_id)
        new_value = u'又一台 ' + dev_type_cn
        self.plms.sj_panel_update_attr(attr_id, new_value)
        try:
            # 检查修改成功
            self.assertEqual(self.plms.sj_panel_get_attr(attr_id), new_value)
        finally:
            # 属性值还原
            self.plms.sj_panel_update_attr(attr_id, raw_value)

    @parameterized.expand(input=filter_param('put'))
    @screenshot
    def test_device_edit_13(self, index, menu_en, dev_type_en, device_id):
        """修改设备安装地址并确认"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
        attr_id = 'pf-installAddress'
        raw_value = self.plms.sj_panel_get_attr(attr_id)
        new_value = u'深圳西站'
        self.plms.sj_panel_update_attr(attr_id, new_value, is_sure=True)
        try:
            # 检查修改成功
            self.assertEqual(self.plms.sj_panel_get_attr(attr_id), new_value)
            sleep(3)
        finally:
            # 属性值还原
            self.plms.sj_panel_update_attr(attr_id, raw_value,is_sure=True)

    @parameterized.expand(input=filter_param('put'))
    @screenshot
    def test_device_edit_14(self, index, menu_en, dev_type_en, device_id):
        """修改设备安装地址并取消"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
        attr_id = 'pf-installAddress'
        raw_value = self.plms.sj_panel_get_attr(attr_id)
        new_value = u'深圳西站'
        self.plms.sj_panel_update_attr(attr_id, new_value, is_sure=False)
        # 检查地址没有被修改
        self.assertEqual(self.plms.sj_panel_get_attr(attr_id), raw_value)

    @parameterized.expand(input=filter_param('addDevGroup'))
    @screenshot
    def test_device_group_01(self, index, menu_en, dev_type_en, device_id):
        """
        用户设备、消防设备加入分组成功，如：子系统管理--智慧消防下的设备
        """
        print('123')
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
        sleep(1)
        self.plms.sj_panel_function('unrelated')
        device_list = [user_device_id1, user_device_id2, alarm_host_id] # 待加入分组的设备
        for device in device_list:
            self.plms.sj_list_search(device)
            self.plms.sj_list_select_device()
            self.plms.sj_panel_function('btn_bind')
        self.plms.sj_panel_function('related')
        group_device_list = self.plms.sj_list_scan_page(2, 3)
        try:
            # 检查设备已成功加入分组
            self.assertTrue(set(device_list), set(group_device_list))
        finally:
            # 将已加入分组的设备移除分组
            for device in device_list:
                self.plms.sj_list_search(device)
                self.plms.sj_list_select_device()
                self.plms.sj_panel_function('btn_unbind')

    @parameterized.expand(input=filter_param('addDevGroup'))
    @screenshot
    def test_device_group_02(self, index, menu_en, dev_type_en, device_id):
        """第一页所有设备加入分组"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
        sleep(1)
        # 进入未分组设备页面，获取第一页所有设备ID
        self.plms.sj_panel_function('unrelated')
        device_ungroup = self.plms.sj_list_scan_page(2,3)
        # 选中当页所有设备并加入分组
        self.plms.sj_list_select_device(0)
        self.plms.sj_panel_function('btn_bind')
        # 进入已加入分组设备页面，获取所有设备
        self.plms.sj_panel_function('related')
        device_group = self.plms.sj_list_scan_page(2, 3)
        # 选中当页所有设备并移除分组
        self.plms.sj_list_select_device(0)
        self.plms.sj_panel_function('btn_unbind')
        # 检查
        self.assertEqual(set(device_ungroup), set(device_group))


if __name__ == "__main__":
    unittest.main()

