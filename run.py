import os
import shutil
import pytest

from conf.setting import REPORT_TYPE

if __name__ == '__main__':
    if REPORT_TYPE == 'allure':
        # 首先加载pytest.ini配置文件，自动扫描所有目录下的conftest文件，加载所有钩子函数，fixture夹具
        # 然后收集用例，会话钩子启动（记录会话开始时间），执行用例，全部用例执行完执行收尾钩子（在main内部完成）
        pytest.main(['-v', '-s', '--alluredir=./report/temp', '--clean-alluredir', '--junitxml=./report/result.xml'])
        if os.path.exists('./environment.xml'):
            shutil.copy('./environment.xml', './report/temp')
        if "JENKINS_URL" not in os.environ:
            os.system(f"allure serve ./report/temp")
