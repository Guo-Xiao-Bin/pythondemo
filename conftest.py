import pytest

from common.readyaml import ReadYamlData
from common.recordlog import logs

read = ReadYamlData()


@pytest.fixture(scope="session", autouse=True)
def fixture_test():
    """前后置处理"""
    read.clear_yaml_data()
    logs.info("--------------接口测试开始-------------")
    yield
    logs.info("--------------接口测试结束-------------")
