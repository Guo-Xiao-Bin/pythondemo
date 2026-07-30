import allure
import pytest

from common.readyaml import get_testcase_yaml
from base.apiutil import RequestBase


@allure.feature("物流管理")
class TestLogistics:
    @allure.story("成功获取下单材料")
    @pytest.mark.parametrize('caseInfo', [get_testcase_yaml("./testcase/logisticsManage/getMaterial.yaml")[0]])
    def test_get_material(self, caseInfo):
        RequestBase().specification_yaml(caseInfo)

    @allure.story("货主成功创建订单")
    @pytest.mark.parametrize('caseInfo', [get_testcase_yaml("./testcase/logisticsManage/commitOrder.yaml")[0]])
    def test_commit_order(self, caseInfo):
        RequestBase().specification_yaml(caseInfo)

    @allure.story("总调集团接单成功")
    @pytest.mark.parametrize('caseInfo', [get_testcase_yaml("./testcase/logisticsManage/receiveOrder.yaml")[0]])
    def test_receive_order(self, caseInfo):
        RequestBase().specification_yaml(caseInfo)

    @allure.story("总调集团成功分配订单")
    @pytest.mark.parametrize('caseInfo', [get_testcase_yaml("./testcase/logisticsManage/assignOrder.yaml")[0]])
    def test_assign_order(self, caseInfo):
        RequestBase().specification_yaml(caseInfo)

    @allure.story("物流公司成功接单")
    @pytest.mark.parametrize('caseInfo', [get_testcase_yaml("./testcase/logisticsManage/getOrder.yaml")[0]])
    def test_get_order(self, caseInfo):
        RequestBase().specification_yaml(caseInfo)