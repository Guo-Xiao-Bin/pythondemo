import allure
import pytest

from base.apiutil import RequestBase
from common.readyaml import get_testcase_yaml

@allure.feature("用户管理")
class TestDebugApi:
    @allure.story("新增用户")
    @pytest.mark.parametrize('case_info', [get_testcase_yaml("./testcase/userManager/addUser.yaml")[0]])
    def test_add_user(self, case_info):
        RequestBase().specification_yaml(case_info)

    @allure.story("删除用户")
    @pytest.mark.parametrize('case_info', [get_testcase_yaml("./testcase/userManager/deleteUser.yaml")[0]])
    def test_delete_user(self, case_info):
        RequestBase().specification_yaml(case_info)

    @allure.story("查询用户")
    @pytest.mark.parametrize('case_info', [get_testcase_yaml("./testcase/userManager/queryUser.yaml")[0]])
    def test_query_user(self, case_info):
        RequestBase().specification_yaml(case_info)

    @allure.story("修改用户")
    @pytest.mark.parametrize('case_info', [get_testcase_yaml("./testcase/userManager/updateUser.yaml")[0]])
    def test_update_user(self, case_info):
        RequestBase().specification_yaml(case_info)

