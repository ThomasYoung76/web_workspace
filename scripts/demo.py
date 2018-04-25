# coding: utf-8

"""
    演示demo
"""

from lib import *
import random

class Demo(MyUnitTest):
    """设备类型测试 -- 演示"""

    def setUp(self):
        """回到主页"""
        log_write(get_current_info() + '\n\n---------------------------------  Test Start  ---------------------------------\n')
        self.plms.sj_func_back_main_page()

    def tearDown(self):
        log_write(
            get_current_info() + '\n\n---------------------------------  Test End  ---------------------------------\n')

    # @parameterized.expand(input=filter_param('import'))
    # @screenshot
    # def test_device_import_03(self, index, menu_en, dev_type_en, device_id):
    #     """导入5个设备并设置属主，成功  //bug"""
    #     sql = "select classes from classification where id = '%s'" % menu_en
    #     log_write(sql)
    #     menu_cn = execute_sql(sql)[0][0]
    #     sql = "select type from device_type where type_id = '%s'" % dev_type_en
    #     dev_type_cn = execute_sql(sql)[0][0]
    #     self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
    #     sleep(1)
    #     file_path = os.path.join(SJ_DOCS, 'import') + os.sep + 'test_import_5.xlsx'
    #     # 从excel文件中获取导入的设备ID
    #     dev_id_list = get_excel_data(file_path, 1)
    #     dev_id_list.pop(0)  # 去掉第一个为空的数据
    #     self.plms.sj_list_function('btn_imp')
    #     self.plms.sj_list_import_device(dev_type=dev_type_en, dev_name=u'自动化测试导入的数据', dev_owner=user_device_id1, upload_file=file_path)
    #     # 检查导入成功
    #     try:
    #         content = '%s new devices have been imported and generated in batches successfully, and 0 devices already existed.'%(len(dev_id_list))
    #         self.assertTrue(self.plms.sj_func_is_tips_display(content))
    #         sleep(1)
    #         # 检查设备的属主
    #         self.plms.sj_list_pagenation(5, is_click=True)
    #         self.plms.sj_list_edit_device(index=-1)
    #         owner = self.plms.sj_panel_get_attr('pf-ownerDevice_id')
    #         self.assertEqual(owner, user_device_id1)
    #     finally:
    #         # 将导入的数据逐个删除
    #         sleep(1)
    #         self.plms.sj_panel_back_device_list()
    #         # self.plms.sj_func_refresh()
    #         for dev_id in dev_id_list:
    #             self.plms.sj_func_refresh()
    #             self.assertTrue(self.plms.sj_list_del_device_upgrade(dev_id, count=1, is_last_page=False, flag_device_id=device_id))

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

    # @parameterized.expand(input=filter_param('import'))
    # @screenshot
    # def test_device_import_02(self, index, menu_en, dev_type_en, device_id):
    #     """设置批次号，导入12个设备成功  # 批次不要随意设置"""
    #     sql = "select classes from classification where id = '%s'" % menu_en
    #     menu_cn = execute_sql(sql)[0][0]
    #     sql = "select type from device_type where type_id = '%s'" % dev_type_en
    #     dev_type_cn = execute_sql(sql)[0][0]
    #     self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
    #     sleep(1)
    #     file_path = os.path.join(SJ_DOCS, 'import') + os.sep + 'test_import_12.xlsx'
    #     # 从excel文件中获取导入的设备ID
    #     dev_id_list = get_excel_data(file_path, 1)
    #     dev_id_list.pop(0)  # 去掉第一行
    #     self.plms.sj_list_function('btn_imp')
    #     self.plms.sj_list_import_device(dev_type=dev_type_en, dev_name=u'自动化测试导入的数据',upload_file=file_path, dev_batch='10086')
    #     # 检查导入成功
    #     try:
    #         content = 'devices have been imported and generated'
    #         self.assertTrue(self.plms.sj_func_is_tips_display(content))
    #         sleep(1)
    #     finally:
    #         # 将导入的数据逐个删除
    #         # self.plms.sj_func_refresh()
    #         for dev_id in dev_id_list:
    #             self.plms.sj_func_refresh() # 每次删除都需要刷新页面才能保证成功，放这里规避问题
    #             self.assertTrue(self.plms.sj_list_del_device_upgrade(dev_id, count=1, is_last_page=False, flag_device_id=device_id))

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
        """导入设备，设置批次号长度11位，导入失败，提示合理"""
        sql = "select classes from classification where id = '%s'" % menu_en
        menu_cn = execute_sql(sql)[0][0]
        sql = "select type from device_type where type_id = '%s'" % dev_type_en
        dev_type_cn = execute_sql(sql)[0][0]
        self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
        sleep(1)
        file_path = os.path.join(SJ_DOCS, 'import') + os.sep + 'test_import_3.xlsx'
        sql = "select type_id from device_type where type='%s'" % dev_type_cn
        dev_type_en = execute_sql(sql)[0][0]
        self.plms.sj_list_function('btn_imp')
        self.plms.sj_list_import_device(dev_type=dev_type_en, dev_name=u'自动化测试导入的数据', dev_batch='1234567890a',upload_file=file_path)
        # 检查导入失败，提示合理
        content = u'设备批次的长度应小于等于10，请重新输入'
        self.assertTrue(self.plms.sj_func_is_tips_display(content))

    @parameterized.expand(input=filter_param('import'))
    @screenshot
    def test_device_import_09(self, index, menu_en, dev_type_en, device_id):
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

                # @parameterized.expand(input=filter_param('batch'))
    # @screenshot
    # def test_device_gen_01(self, index, menu_en, dev_type_en, device_id):
    #     """批量生成5台无线报警设备"""
    #     sql = "select classes from classification where id = '%s'" % menu_en
    #     menu_cn = execute_sql(sql)[0][0]
    #     sql = "select type from device_type where type_id = '%s'" % dev_type_en
    #     dev_type_cn = execute_sql(sql)[0][0]
    #     self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
    #     sleep(1)
    #     batch_num = str(random.randint(100000000, 900000000))
    #     total_num = 5
    #     self.plms.sj_list_gen_device(batch_num=batch_num, total_count=total_num, dev_type=dev_type_en, \
    #                                  dev_name=u'批量生成的测试设备', )
    #     try:
    #         # 检查批量生成的设备成功
    #         # content = '%d new devices have been generated in batches successfully' % total_num
    #         content = 'devices'
    #         self.assertTrue(self.plms.sj_func_is_tips_display(content))
    #     finally:
    #         # 删除生成的设备
    #         self.plms.sj_func_back_main_page()
    #         self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
    #         self.plms.sj_list_del_device_upgrade(batch_num, count=total_num, is_last_page=False, \
    #                                              flag_device_id=device_id)

            # @parameterized.expand(input=filter_param('post'))
    # @screenshot
    # def test_device_add_02(self, index, menu_en, dev_type_en, device_id):
    #     """添加设备，修改ID，名称，描述信息"""
    #     sql = "select classes from classification where id = '%s'" % menu_en
    #     menu_cn = execute_sql(sql)[0][0]
    #     sql = "select type from device_type where type_id = '%s'" % dev_type_en
    #     dev_type_cn = execute_sql(sql)[0][0]
    #     self.plms.sj_main_to_device_list(index, menu_cn, dev_type_cn)
    #     new_device_name = u'这又是一台添加的' + dev_type_cn
    #     new_device_desc = new_device_name + u'的描述信息'
    #     new_device_id = '123abc' + device_id
    #     self.plms.sj_list_add_device(new_device_name, is_save=False)
    #     self.plms.sj_panel_update_attr('pf-_id', new_device_id, is_save=False)
    #     self.plms.sj_panel_update_attr('pf-deviceDesc', new_device_desc, is_save=True)
    #     try:
    #         # 检查设备名称正确
    #         device_name = self.plms.sj_panel_get_attr('pf-deviceName')
    #         device_id = self.plms.sj_panel_get_attr('pf-_id')
    #         device_desc = self.plms.sj_panel_get_attr('pf-deviceDesc')
    #         self.assertEqual(device_name, new_device_name)
    #         self.assertEqual(device_id, new_device_id)
    #         self.assertEqual(device_desc, new_device_desc)
    #     finally:
    #         # 回到搜索页面
    #         self.plms.sj_panel_back_device_list()
    #         # 检查该设备存在并删除
    #         self.assertTrue(self.plms.sj_list_del_device_upgrade(new_device_id, count=1, flag_device_id=device_id))
    #
    # @parameterized.expand(input=filter_param('put'))
    # @screenshot
    # def test_device_edit_01(self, index, menu_en, dev_type_en, device_id):
    #     """修改属主成功，属主自动关注该设备"""
    #     # 修改设备alarm_host_id的属主为user_device_id1
    #     sql = "select classes from classification where id = '%s'" % menu_en
    #     menu_cn = execute_sql(sql)[0][0]
    #     sql = "select type from device_type where type_id = '%s'" % dev_type_en
    #     dev_type_cn = execute_sql(sql)[0][0]
    #     self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
    #     self.plms.sj_panel_update_attr('pf-ownerDevice_id', user_device_id1)
    #     self.plms.sj_func_back_main_page()
    #     try:
    #         # 检查用户user_device_id1已关注alarm_host_id
    #         self.plms.sj_main_to_device_panel(user_device_id1, index=0, sub_menu=u'公众用户')
    #         self.assertTrue(self.plms.sj_list_is_device_exist(device_id, 'authorized'))
    #     finally:
    #         # 还原环境，属主修改为空
    #         self.plms.sj_func_back_main_page()
    #         self.plms.sj_main_to_device_panel(device_id, index, menu_cn, dev_type_cn)
    #         self.plms.sj_panel_update_attr('pf-ownerDevice_id', '')

if __name__ == "__main__":
    run_suite(Demo)
    # 发送邮件
    subject = u'【请阅】三江智慧云PLMS平台测试报告'
    content = u'测试范围：消防设备-无线报警主机\n' \
              u'Notes：测试报告预览和打开模式可能会出现乱码，且页面效果元素效果无法显示，请下载后打开'
    file_html = scan_dir(SJ_RESULT, 'html')
    send_mail(subject, content, attach=file_html)
