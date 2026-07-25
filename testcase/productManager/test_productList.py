import pytest
import allure
from common.readyaml import get_testcase_yaml
from common.recordlog import logs
from common.sendrequest import SendRequest
from base.apiutil import RequestBase


@allure.feature('商品列表')
class TestLogin:
    @allure.story('获取商品列表')
    @pytest.mark.parametrize('params', [get_testcase_yaml('./testcase/productManager/getProductList.yaml')[0]])
    def test_get_product_list(self, params):
        RequestBase().specification_yaml(params)

    @allure.story('获取商品详情信息')
    @pytest.mark.parametrize('params', [get_testcase_yaml('./testcase/productManager/productDetail.yaml')[0]])
    def test_get_product_detail(self, params):
        RequestBase().specification_yaml(params)

