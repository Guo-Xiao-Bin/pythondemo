import pytest
import allure
from common.readyaml import get_testcase_yaml
from common.recordlog import logs
from common.sendrequest import SendRequest
from base.apiutil import RequestBase


@allure.feature('登录接口')
class TestLogin:
    @allure.story('用户名和密码登录正常校验')
    @pytest.mark.parametrize('params', [get_testcase_yaml('./testcase/Login/login.yaml')[0]])
    def test_case01(self, params):
        RequestBase().specification_yaml(params)

    @allure.story('用户名和密码登录错误校验')
    @pytest.mark.parametrize('params', [get_testcase_yaml('./testcase/Login/login.yaml')[1]])
    def test_case02(self, params):
        RequestBase().specification_yaml(params)


