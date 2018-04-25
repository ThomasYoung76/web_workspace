# coding: utf-8
"""
    Function: 
"""
import os
import unittest
import sys
sys.path.append("..")
from BeautifulReport import BeautifulReport
from scripts.device import *

def run_without_report():
    """
    运行excel中的测试用例。自动填充结果，但不输出测试报告，也不发送邮件
    :return: None
    """
    result = {}
    suite = unittest.TestLoader().loadTestsFromTestCase(Device)
    test_result = unittest.TextTestRunner(verbosity=1).run(suite)

def run_with_report():
    """
    采用测试报告文件中对unittest库的二次封装，运行excel中的测试用例。自动填充结果，并输出测试报告
    :return: 成功率, 如0.5
    """
    test_suite = unittest.defaultTestLoader.discover(start_dir=SJ_SCRIPTS, pattern='device.py')
    result = BeautifulReport(test_suite)
    report_name = time.strftime("%Y%m%d_%H%M")
    result.report(filename=report_name, description=REPORT_DESC, log_path=SJ_RESULT)
    # 过滤出失败的结果
    fail_result = {}
    for info in result.result_list:
        if info[4] == '失败':
            fail_result[info[1]] = info[4]
    return (len(result.result_list) - result.failure_count) / len(result.result_list)


def main():
    """
    执行测试用例，根据settins.py的配置，决定是否输出测试报告，是否发送邮件
    :return: None
    """
    if IS_REPORT:
        pass_rate = run_with_report()
        if IS_EMAIL and pass_rate > PASS_RATE:
            file_html = scan_dir(SJ_RESULT, 'html')
            send_mail('测试邮件', plain_contant=None, attach=file_html)
    else:
        run_without_report()

if __name__ == '__main__':
    main()
    import os
    os.system("pause")
