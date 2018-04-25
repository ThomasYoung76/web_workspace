# coding: utf-8
import sqlite3
from lib.data import *
from lib.snatch import SNATCH
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

if __name__ == "__main__":

    # --------------------------------- 创建数据库 ----------------------------------

    # 如果已经存在则备份db文件
    if os.path.isfile(SJ_DB):
        # 备份文件存在则删除
        if os.path.exists(SJ_DB + '.bak'):
            os.remove(SJ_DB + '.bak')
        # 原文件备份
        os.rename(SJ_DB, SJ_DB + '.bak')
        print('bak db file success')
    # 创建新的数据库
    conn = sqlite3.connect(SJ_DB)
    conn.text_factory = str

    # 创建游标
    cursor = conn.cursor()

    # --------------------------------- 创建表 ----------------------------------

    tables = ['classification', 'device_type', 'testcase', 'rights', 'resource']
    # 建表
    sql0 = '''create table classification(
        ID text,
        CLASSES text,
        MENU text,
        TAG int)'''

    sql1 = '''create table device_type(
        TYPE_ID text,
        CLASSES text,
        TYPE text,
        DESC text)
    '''

    sql2 = '''create table testcase(
        ID  text,
        TYPE_ID text
    )
    '''

    sql3 = """create table rights(
        ID text primary key,
        FUNCTION text,
        DESC text
    )
    """

    sql4 = """create table resource(
        ID text,
        name text,
        desc text,
        url text,
        functions text
    )
    """
    cursor.execute(sql0)
    print("Table %s created successfully" % tables[0])
    cursor.execute(sql1)
    print("Table %s created successfully" % tables[1])
    cursor.execute(sql2)
    print("Table %s created successfully" % tables[2])
    cursor.execute(sql3)
    print("Table %s created successfully" % tables[3])
    cursor.execute(sql4)
    print("Table %s created successfully" % tables[4])

    #  ----------------------------------------- 插入数据到表中 ---------------------------------------------------------

    sna = SNATCH()

    # 插入数据到表classification
    class_file = os.path.join(os.path.dirname(SJ_DB), 'classification.csv')
    param0 = sna.get_csv(class_file)
    sql_insert = "insert into classification values(?,?,?,?)"
    cursor.executemany(sql_insert, param0)
    print('Table %s insert data from csv file success' % tables[0])

    # 插入数据到表device_type
    device_file = os.path.join(os.path.dirname(SJ_DB), 'device_type.csv')
    param1 = sna.get_csv(device_file)
    sql_insert = "insert into device_type values(?,?,?,?)"
    cursor.executemany(sql_insert, param1)
    print('Table %s insert data from csv file success' % tables[1])

    # 插入数据到表testcase
    case_file = os.path.join(os.path.dirname(SJ_DB), 'testcase.csv')
    param2 = sna.get_csv(case_file)
    sql_insert = "insert into testcase values(?,?)"
    cursor.executemany(sql_insert, param2)
    print('Table %s insert data from csv file success' % tables[2])

    # 插入数据到表rights
    case_file = os.path.join(os.path.dirname(SJ_DB), 'rights.csv')
    param3 = sna.get_csv(case_file)
    sql_insert = "insert into rights values(?,?,?)"
    cursor.executemany(sql_insert, param3)
    print('Table %s insert data from csv file success' % tables[3])

    # 插入数据到表resource
    case_file = os.path.join(os.path.dirname(SJ_DB), 'resource.csv')
    param3 = sna.get_csv(case_file)
    sql_insert = "insert into resource values(?,?,?,?,?)"
    cursor.executemany(sql_insert, param3)
    print('Table %s insert data from csv file success' % tables[4])

    conn.commit()
    cursor.close()
    conn.close()
