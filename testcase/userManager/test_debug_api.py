import pytest

from base.apiutil import RequestBase
from common.readyaml import get_testcase_yaml


class TestDebugApi:
    @pytest.mark.parametrize('case_info', [get_testcase_yaml("./testcase/userManager/addUser.yaml")][0])
    def test_add_user(self, case_info):
        RequestBase().specification_yaml(case_info)