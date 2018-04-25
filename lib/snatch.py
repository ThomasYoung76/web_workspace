# coding: utf-8
"""
    Func : 爬取三江智慧云数据，并存入csv文件中，重新加载testcase表
    Note : 执行该脚本可从三江智慧云重新爬取最新数据
"""

import csv
from lib.page import *
import sqlite3

class SNATCH(object):
    def __init__(self):
        pass

    def open_plms(self):
        plms = PLMS()
        return plms

    def get_classes_data(self):
        plms = self.open_plms()
        plms.sj_main_to_device_list(3, u'系统分类管理')
        result = plms.sj_list_scan_page(2, 5, is_all_page=True)
        sleep(1)
        plms.driver.quit()
        # 增加tag列
        for i, row in enumerate(result):
            row = list(row)
            if row[2] == '用户管理':
                row.append(0)
            elif row[2] == '设备管理':
                row.append(1)
            elif row[2] == '子系统管理':
                row.append(2)
            elif row[2] == '系统配置':
                row.append(3)
            elif row[2] == '用户反馈':
                row.append(4)
            elif row[2] == '数据分析':
                row.append(5)
            else:
                row.append(100)
            result[i] = tuple(row)
        return result

    def get_device_type_data(self):
        plms = self.open_plms()
        plms.sj_main_to_device_list(3, u'设备类型管理')
        result = plms.sj_list_scan_page(2, 6, is_all_page=True)
        sleep(1)
        plms.driver.quit()
        return result

    def get_rights_data(self):
        plms = self.open_plms()
        plms.sj_main_to_device_list(3, 'PLMS权限管理')
        plms.driver.find_element_by_xpath("//a[@href='#/permission/list.html']").click()
        result = plms.sj_list_scan_page(2, 5, is_all_page=True)
        sleep(1)
        plms.driver.quit()
        return result

    def get_resource_data(self):
        plms = self.open_plms()
        plms.sj_main_to_device_list(3, 'PLMS权限管理', '资源')
        result = plms.sj_list_scan_page(2, 7, is_all_page=True)
        sleep(1)
        plms.driver.quit()
        return result

    def put_csv(self, cfile, data, first_row=(), decode=None, encode=None):
        """
        写数据到csv文件中, 第一行默认为空
        :param cfile: 文件路径
        :param data: 待写入的csv数据[(...)]，往csv第二行开始写
        :param first_row: 第一行，默认为空
        :param decode: 解码方式
        :param encode: 编码方式
        :return:
        """
        if decode or encode:
            data = self.update_code(data, decode=decode, encode=encode)
        if os.path.isfile(cfile):
            # 备份文件存在则删除
            if os.path.exists(cfile + '.bak'):
                os.remove(cfile + '.bak')
            # 原文件备份
            os.rename(cfile, cfile + '.bak')
        with open(cfile, 'wb') as cf:
            csv_writer = csv.writer(cf, dialect='excel')
            csv_writer.writerow(first_row)     # 第一行不写内容
            csv_writer.writerows(data)
        print('数据写入文件%s成功'%cfile)
        return None

    def get_csv(self, cfile, decode=None, encode=None):
        """
        读取csv文件中的数据，默认不读第一行
        :param cfile: csv文件路径
        :param decode: 解码方式
        :param encode: 编码方式
        :return:
        """
        data = []
        with open(cfile, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)
            data.pop(0)
        if decode or encode:
            data = self.update_code(data, decode=decode, encode=encode)
        return data

    def update_code(self, data, decode='utf-8', encode='gbk'):
        """
        更改csv数据的编码格式为gbk(原编码格式为utf-8)
        :param data: csv数据，格式为[(...),(...),(...)]
        :param decode: 解码方式
        :param encode: 编码方式，指定了解码方式的话必须制定编码方式
        :return: 返回重新编码的data
        """
        if decode:
            for i, row in enumerate(data):
                row = list(row)
                for j in range(len(row)):
                    # 改变每个数据的编码格式
                    # row[j] = row[j].decode(decode).encode(encode)
                    if decode:
                        row[j] = row[j].decode(decode)
                    if encode:
                        row[j] = row[j].encode(encode)
                data[i] = tuple(row)
        return data

    def reload_testcase(self):
        """重新加载testcase表"""
        # 创建新的数据库
        conn = sqlite3.connect(SJ_DB)
        conn.text_factory = str
        # 创建游标
        cursor = conn.cursor()
        # 从testcase.csv文件中获取数据
        case_file = os.path.join(os.path.dirname(SJ_DB), 'testcase.csv')
        params = self.get_csv(case_file)
        # 清空表数据后重新插入新的数据
        sql_delete = "delete from testcase"
        sql_insert = "insert into testcase values(?,?)"
        try:
            cursor.execute(sql_delete)
            conn.commit()
        finally:
            cursor.executemany(sql_insert, params)
            conn.commit()
        conn.close()


# 爬取网页中数据写入csv文件
if __name__ == "__main__":
    # 数据写入clssification.csv文件
    class_file = os.path.join(os.path.dirname(SJ_DB), 'classification.csv')
    sna = SNATCH()
    data = sna.get_classes_data()
    sna.put_csv(class_file, data, first_row=('ID', 'CLASSES', 'MENU', 'TAG'))
    # 数据写入device_type文件
    device_file = os.path.join(os.path.dirname(SJ_DB), 'device_type.csv')
    data = sna.get_device_type_data()
    sna.put_csv(device_file, data, first_row=('TYPE_ID','CLASSES','TYPE','DESC'))
    # 数据写入rights文件
    rights_file = os.path.join(os.path.dirname(SJ_DB), 'rights.csv')
    data = sna.get_rights_data()
    sna.put_csv(rights_file, data, first_row=('ID','FUNCTION','DESC'))
    # 数据写入resource文件
    resource_file = os.path.join(os.path.dirname(SJ_DB), 'resource.csv')
    data = sna.get_resource_data()
    sna.put_csv(resource_file, data, first_row=('ID', 'name', 'desc', 'url', 'functions'))
