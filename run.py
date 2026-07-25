import os
import shutil

import pytest

from conf.setting import REPORT_TYPE

if __name__ == '__main__':
    if REPORT_TYPE == 'allure':
        # allure原始结果数据输出到report/temp文件夹，没有该参数不会生成allure数据
        # 指定运行testcase目录下全部测试用例
        # --clean-alluredir执行前自动清空./report/temp旧数据
        # 额外生成一份标准JUnit xml测试结果文件，可用于jenkins（CI）平台识别
        pytest.main(
            ['-s', '-v', '--alluredir=./report/temp', './testcase', '--clean-alluredir',
             '--junitxml=./report/result.xml']
        )
        # allure报告展示配置信息
        shutil.copy('./environment.xml', './report/temp')
        # 调用系统cmd命令，启动临时本地web服务，自动打开浏览器展示allure报告
        os.system(f"allure serve ./report/temp")
