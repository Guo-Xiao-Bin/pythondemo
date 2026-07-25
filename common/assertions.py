import operator
import os.path

import allure
import jsonpath

from common.readyaml import get_testcase_yaml
from common.recordlog import logs
from common.connection import ConnectMysql


class Assertions:
    """
    接口断言模式封装，支持
    1、字符串包含
    2、结果不相等断言
    3、结果相等断言
    4、断言接口返回值里面的任意一个值
    5、数据库断言
    """

    def contains_assert(self, value, response, status_code):
        """
        字符串包含断言：断言预期结果的字符串是否包含在接口的实际返回结果中
        :param value: 预期结果yaml文件中validation关键字下的结果
        :param response:
        :param status_code:
        :return:
        """
        # 断言状态标识，0代表成功，其他代表失败
        flag = 0
        if isinstance(value, dict) and isinstance(response, dict):
            for assert_key, assert_value in value.items():
                if assert_key == "status_code":
                    if assert_value != status_code:
                        flag += 1
                        logs.error("contains断言失败，接口返回码【%s】不等于【%s】" % (status_code, assert_value))
                    else:
                        logs.info("contains断言成功：预期结果：【%s】，实际结果：【%s】" % (status_code, assert_value))
                else:
                    # $是json根节点，..是递归向下搜索，不限层级
                    # 在整个json里，任意深度查找所有key名称=assert_key的字段
                    res_list = jsonpath.jsonpath(response, '$..%s' % assert_key)
                    if isinstance(res_list[0], str):
                        res_list = ''.join(res_list)
                    if res_list:
                        # 包含断言，比如msg预期结果为”成功“，接口响应实际msg为“登录成功”，那么”成功“包含在”登录成功”内，属于包含断言
                        if assert_value in res_list:
                            logs.info("字符串断言成功：预期结果：【%s】，实际结果：【%s】" % (assert_value, res_list))
                        else:
                            flag += 1
                            logs.error(f"响应文本断言失败：预期结果为：【%s】，实际结果为：【%s】" % (assert_value, res_list))
        else:
            raise TypeError("相等断言失败--类型错误，预期结果和接口的实际响应结果必须为字典类型")
        return flag

    def equal_assert(self, value, response):
        """相等断言"""
        flag = 0
        res_list = []
        if isinstance(value, dict) and isinstance(response, dict):
            # 处理接口响应实际数据，保持与预期结果的数据结构一致
            for res in response:
                if res != list(value.keys())[0]:
                    res_list.append(res)
            for rl in res_list:
                del response[rl]
            # 判断实际结果和预期结果是否相等
            eq_assert = operator.eq(response, value)
            if eq_assert:
                logs.info(f"相等断言成功：接口的实际结果为：{response}，等于预期结果：{str(value)}")
            else:
                flag += 1
                logs.error(f"相等断言失败：忌口的实际结果为：{response}，不等于预期结果：{str(value)}")
        else:
            raise TypeError("相等断言失败--类型错误，预期结果和接口的实际响应结果必须为字典类型")
        return flag

    def not_equal_assert(self, value, response):
        """
        不相等断言，不相等才是断言成功
        :param value:
        :param response:
        :return:
        """
        flag = 0
        res_list = []
        if isinstance(value, dict) and isinstance(response, dict):
            # 处理接口响应实际数据，保持与预期结果的数据结构一致
            for res in response:
                if res != list(value.keys())[0]:
                    res_list.append(res)
            for rl in res_list:
                del response[rl]
            # 判断实际结果和预期结果是否不相等，不相等返回true
            eq_assert = operator.ne(response, value)
            if eq_assert:
                logs.info(f"不相等断言成功：接口的预期结果：{str(value)}，不等于实际结果为：{response}")
            else:
                flag += 1
                logs.error(f"不相等断言成功：接口的预期结果：{str(value)}，等于实际结果为：{response}")
        else:
            raise TypeError("相等断言失败--类型错误，预期结果和接口的实际响应结果必须为字典类型")
        return flag

    def assert_mysql(self, expected_sql):
        """
        数据库断言
        :param expected_sql: 预期结果，也就是yaml文件中中的sal语句
        :return:
        """
        flag = 0
        conn = ConnectMysql()
        db_value = conn.query(expected_sql)
        if db_value is not None:
            logs.info("数据库断言成功")
        else:
            flag += 1
            logs.error("数据库断言失败，检查数据库是否存在该数据")
        return flag

    def assert_result(self, expected, response, status_code):
        """
        断言模式，通过all_flag标记断言结果
        :param expected: 预期结果
        :param response: 接口实际返回结果（json格式）
        :param status_code: 响应状态码
        :return:
        """
        all_flag = 0
        try:
            # expected是预期结果列表
            for yq in expected:
                # yq是字典，{‘contains’:{'msg':'登录成功'}}
                for key, value in yq.items():
                    # value是{'msg':'登录成功'}
                    if key == "contains":
                        flag = self.contains_assert(value, response, status_code)
                    elif key == "eq":
                        flag = self.equal_assert(value, response)
                    elif key == "ne":
                        flag = self.not_equal_assert(value, response)
                    elif key == "db":
                        flag = self.assert_mysql(value)
                    else:
                        flag = 0
                    all_flag += flag
            assert all_flag == 0
            logs.info("测试成功！")
        except Exception as e:
            logs.error("测试失败！")
            logs.error(f"异常信息：{e}")
            assert all_flag == 0


if __name__ == '__main__':
    data = get_testcase_yaml(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'testcase\Login\login.yaml'))[0]
    value = data['testCase']['validation']
    response = {"error_code": None, "msg": "登录成功", "msg_code": 200, "orgId": "6140913758128971280",
                "token": "2aE2bbDD66D35f5EEda77CE7abe70", "userId": "9337151637697210487"}
    ass = Assertions()
    for i in value:
        for j, k in i.items():
            ass.equal_assert(value=k, response=response)
