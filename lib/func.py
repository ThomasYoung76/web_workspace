#coding: utf-8
"""
    功能类方法
"""
import os
import shutil
import xlrd
import xlwt
import csv
import sqlite3
from lib.data import *
import traceback
import sys
from selenium import webdriver
from time import sleep

# 处理导出到Excel中的数据
def get_excel_data(file, col=0 ):
    """
    获取Excel表格中的数据
    :param file: 文件位置
    :param col: col为0表示获取Excel中所有数据，col为其他数字，表示获取第col列数据
    :return: col为0时，以两重列表形式返回Excel表中所有数据，col为1或其他数字表示获取第1列或其他列的数据，以列表形式返回
    """
    with xlrd.open_workbook(file) as data:
        table = data.sheet_by_index(0)
    nrows = table.nrows  # 行数
    result = []
    for rownum in range(nrows):
        row_list = table.row_values(rownum)
        result.append(row_list)
    if col == 0:
        return result
    else:
        result_col = []
        for line in result:
            result_col.append(line[col-1])
        return result_col

# 处理导出到txt文本中的数据
def get_txt_data(file):
    result = []
    with open(file, 'r') as fp:
        data = fp.read()
    for row in data.split('\n'):
        row_list = row.split(',')
        result.append(row_list)
    return result

# 获取csv文件
def get_csv_data(file):
    result = []
    with open(file, 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            result.append(row)
    result.pop(0)
    return result

# 扫描目录、获取目录最新生成的文件
def scan_dir(dir_path, suffix, is_newest=True):
    """
    递归遍历目录，默认获取最新某格式文件
    :param dir_path: 目录名
    :param suffix: 文件格式/文件后缀，如'html'
    :is_newest: 是否获取最新文件，True则返回最新文件，False则返回文件列表
    :return: 最新文件，is_newest为False时返回文件列表
    """
    file_list = []
    for root, dirs, files in os.walk(dir_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            if file_name.endswith(suffix):
                file_list.append(file_path)
    # 是否获取最新文件
    if is_newest:
        file_new = ''
        flag = 0
        for file in file_list:
            file_atime = os.path.getmtime(file)
            if file_atime > flag:
                flag = file_atime
                file_new = file
        return file_new
    return file_list

# 写入excel文件 //test
def gen_test():
    """
    写数据到excel文件，尚未使用，demo，仅供参考，实际由测试工程师自己写文件
    :return:
    """
    table = xlwt.Workbook()
    sheet = table.add_sheet('fire_device')
    sheet.write(0, 0, 'a')
    filename= os.path.join(os.path.join(SJ_DOCS, 'plms'), 'testcase.xlsx')
    table.save(filename)

# 拷贝本地文件到目标服务器
def copy_file():
    """
    从本地拷贝文件到公共服务器主机， ---目前拷贝失败，没找到原因
    :return:
    """
    src_path = os.path.join(SJ_RESULT, 'tmp')
    if not os.path.isdir(src_path):
        os.makedirs(src_path)
    file_list = scan_dir(src_path, 'jpg', is_newest=False)
    bak_path = os.path.join(SJ_RESULT, 'screenshot')
    # dst_path = r'\\10.1.73.8\%s\%s\RFS\screenshot' %(u'25_产品测试部', u'测试常用软件')
    dst_path = u'\\\\10.1.73.8\\25_产品测试部\\测试常用软件\\RFS\\screenshot'
    # 备份文件
    for file in file_list:
        shutil.copy2(file, bak_path)
        copy_command = "copy %s %s" % (file, dst_path)
        print(copy_command)
        try:
            os.system(copy_command)
        except:
            sys.stderr.read().decode('utf-8')

def execute_sql(sql):
    """
    执行sql查询语句，从plms.db获取数据
    如：sql = 'select c.tag, d.classes, d.type, t.id  from testcase as t, device_type as d, classification as c ' \
            'where t.type_id = d.type_id and d.classes = c.classes'
    从数据库中表testcase、device_type、classification中联合查询，获取4个字段（如：(1, '消防设备', '无线报警主机', alarm_host_id)）的值
    1是界面主菜单索引值，‘消防设备’子菜单，‘无线报警主机’是设备类型，即第三层子菜单，alarm_host_id是新增的相应设备类型的设备ID
    :return: 参数序列，提供多组参数，供用例使用，如：
        [
            (1, '消防设备', '无线报警主机', alarm_host_id),
            (1, '消防设备', 'LoRaMote_手报', LoRa_device_id),
            (2, '智慧消防', '社区消防站', wise_device_id)
        ]
    :param sql : 查询语句sql
    :return : 查询结果
    """
    db_file = os.path.join(SJ_DOCS, 'plms_data') + os.sep + 'plms.db'
    # 创建/连接数据库
    conn = sqlite3.connect(db_file)
    conn.text_factory = str
    # 创建游标
    cursor = conn.cursor()
    # 执行查询语句的sql
    result = cursor.execute(sql)
    params = result.fetchall()
    conn.close()
    return params

def filter_param(rights_id):
    """
    从查询结果中过滤出拥有权限的参数组， 已根据实际情况将查询字段写死
    :param rights_id: str类型，权限ID，取表rights中的id字段，如'post', 'export', 'import'...
    :return: testcase表中拥有该权限的记录的参数组序列，提供多组参数，供用例使用，如：
        [
            (1, '消防设备', '无线报警主机', alarm_host_id),
            (1, '消防设备', 'LoRaMote_手报', LoRa_device_id),
            (2, '智慧消防', '社区消防站', wise_device_id)
        ]
    """
    # 通过权限ID查询功能，如rights_id为export时查出来的function为导出
    sql = "select function from rights where id = '%s'" % rights_id
    rights_func = execute_sql(sql)
    rights_func = rights_func[0][0]


    # 查询5个字段，如：(1, '消防设备', '无线报警主机', alarm_host_id， "修改，导入，导出")
    # sql = 'select c.tag, d.classes, d.type, t.id, r.functions  from testcase as t, device_type as d, classification as c, ' \
    #       'resource as r where t.type_id = d.type_id and d.classes = c.classes and t.type_id = r.id'
    sql = 'select c.tag, c.id, d.type_id, t.id, r.functions  from testcase as t, device_type as d, classification as c, ' \
          'resource as r where t.type_id = d.type_id and d.classes = c.classes and t.type_id = r.id'
    total_params = execute_sql(sql)
    params = []
    # 如‘导入’在这条记录1, 'fireDevice', 'JB-QBL-6001', '59317dbcc02f1c65'， "修改，导入，导出")的最后一个字段中，则过滤出该条记录
    # 并去掉最后一个字段，该记录过滤后为1, 'fireDevice', 'JB-QBL-6001', '59317dbcc02f1c65'），其他记录类似处理
    for row in total_params:
        row = list(row)
        if rights_func in row[-1]:
            row.pop()
            row = tuple(row)
            params.append(row)
    return params

if __name__ == '__main__':
    # exp_file = scan_dir(SJ_DOCS, 'txt')
    # # excel_data = get_excel_data(exp_file)
    # with open(exp_file) as fp:
    #     data = fp.read()
    # result = []
    # # row_list = []
    # for row in data.split('\n'):
    #     row_list = row.split(',')
    #     print row_list
    #     result.append(row_list)
    # print result
    # copy_file()
    # gen_test()
    # file_path = os.path.join(SJ_DOCS, 'plms_data')
    # csv_file = os.path.join(file_path, 'classification.csv')
    # result = get_csv_data(csv_file)
    # print result
    # 过滤参数
    print(filter_param('import'))
    print(execute_sql("select classes from classification where id = 'fireDevice'"))
