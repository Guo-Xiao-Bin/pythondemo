import pytest
import allure
from common.readyaml import get_testcase_yaml
from common.recordlog import logs
from common.sendrequest import SendRequest
from base.apiutil import RequestBase


@allure.feature('商品管理')
class TestProductList:
    @allure.story('成功获取商品列表')
    @pytest.mark.parametrize('params', [get_testcase_yaml('./testcase/productManage/getProductList.yaml')[0]])
    def test_get_product_list(self, params):
        RequestBase().specification_yaml(params)

    @allure.story('成功获取商品详情信息')
    @pytest.mark.parametrize('params', [get_testcase_yaml('./testcase/productManage/productDetail.yaml')[0]])
    def test_get_product_detail(self, params):
        RequestBase().specification_yaml(params)

    @allure.story('商品正常提交订单')
    @pytest.mark.parametrize('params', [get_testcase_yaml('./testcase/productManage/placeAnOrder.yaml')[0]])
    def test_place_an_order(self, params):
        RequestBase().specification_yaml(params)

    @allure.story('正常订单支付')
    @pytest.mark.parametrize('params', [get_testcase_yaml('./testcase/productManage/orderPay.yaml')[0]])
    def test_order_pay(self, params):
        RequestBase().specification_yaml(params)

    @allure.story('成功添加商品到购物车')
    @pytest.mark.parametrize('params', [get_testcase_yaml('./testcase/productManage/shoppingJoinCart.yaml')[0]])
    def test_shopping_join_cart(self, params):
        RequestBase().specification_yaml(params)

    @allure.story('正常校验商品订单状态')
    @pytest.mark.parametrize('params', [get_testcase_yaml('./testcase/productManage/checkOrderStatus.yaml')[0]])
    def test_check_order_status(self, params):
        RequestBase().specification_yaml(params)

    @allure.story('正常校验商品物流状态接口')
    @pytest.mark.parametrize('params', [get_testcase_yaml('./testcase/productManage/checkLogisticsStatus.yaml')[0]])
    def test_check_logistics_status(self, params):
        RequestBase().specification_yaml(params)

    @allure.story('正常校验商品库存')
    @pytest.mark.parametrize('params', [get_testcase_yaml('./testcase/productManage/shoppingInventory.yaml')[0]])
    def test_product_inventory(self, params):
        RequestBase().specification_yaml(params)
