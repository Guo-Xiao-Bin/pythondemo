import time

import pytest

from common.readyaml import ReadYamlData
from common.recordlog import logs
from common.dingRobot import send_dingding_msg
from common.operJenkins import PJenkins

read = ReadYamlData()
session_start_time = 0.0
pjenkins = PJenkins()

@pytest.fixture(scope="session", autouse=True)
def fixture_test():
    """测试前后置处理，在执行用例时发生，作为执行用例的前后置操作"""
    read.clear_yaml_data()
    logs.info("--------------接口测试开始-------------")
    yield
    logs.info("--------------接口测试结束-------------")


def pytest_sessionstart(session):
    """
    收集完用例后，会启动钩子会话
    测试会话启动时自动记录起始时间
    """
    global session_start_time
    session_start_time = time.time()


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    全部用例执行完收尾整个会话的钩子，钩子作用在整个测试会话生命周期
    内置钩子函数，函数名不可变
    每次pytest测试完成后，会自动收集测试结果的数据，可以与自动发送到钉钉关联
    :param terminalreporter:
    :param exitstatus: 内部终端报告，对象的stats属性
    :param config: 将报告回操作系统的退出状态
    :return: pytest配置对象
    """
    # 收集测试用例总数
    case_total = terminalreporter._numcollected
    # 收集测试用例通过数
    passed = len(terminalreporter.stats.get('passed', []))
    # 收集测试用例失败数
    failed = len(terminalreporter.stats.get('failed', []))
    # 收集测试用例错误数量
    error = len(terminalreporter.stats.get('error', []))
    # 收集测试用例跳过执行数量
    skipped = len(terminalreporter.stats.get('skipped', []))
    # 收集测试用例执行时长，保留两位小数
    duration = round(time.time() - session_start_time, 2)
    # 收集测试报告链接
    report_url = pjenkins.report_success_or_fail()

    content = f"""
        各位好，本次xxx电商项目的测试报告执行结果如下，请注意失败及错误的接口：
        测试用例总数：{case_total}个
        通过数：{passed}个
        失败数：{failed}个
        跳过执行数：{skipped}个
        错误异常：{error}个
        测试用例执行时长：{duration}秒
        点击查看测试报告：{report_url}
        """
    send_dingding_msg(content=content)
