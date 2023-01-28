# -*- encoding=utf8 -*-
__author__ = "HXH"

import unittest
import requests
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
COMMON_DIR = os.path.join(BASE_DIR,"config")
sys.path.append(COMMON_DIR)
from common import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_cxgj,headers_admin_formdata,vpt_header


class Change_Password(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global headersvcz
        headersvcz = headers_vcz(13538878368)

    def test_1_1(self):
        u'''修改密码—可修改密码并在公众号重新登录成功'''
        url = "https://test.chebufan.cn/vcd/api/open/sys/sysUser/updatePwd"
        json = {
                "data": {
                    "oldPwd": "123456",
                    "newPwd": "456789",
                    "confirmPwd": "456789"
                },
                "sign": "nosign",
                "timestamp": 1649646576198
            }
        updatePwd = requests.post(url,json=json,headers=headersvcd)
        #登录公众号
        url_login = "http://test.chebufan.cn/chebftest/wx/xlc/account/loginByPassword"
        data = {"account": 13538878368, "password": 456789}
        login = requests.post(url_login, data=data)
        self.assertEqual("登陆成功",login.json()["msg"])
        #修改密码
        url = "https://test.chebufan.cn/vcd/api/open/sys/sysUser/updatePwd"
        json = {
                "data": {
                    "oldPwd": "456789",
                    "newPwd": "123456",
                    "confirmPwd": "123456"
                },
                "sign": "nosign",
                "timestamp": 1649646576198
            }
        updatePwd = requests.post(url,json=json,headers=headersvcd)
        #登录公众号
        url_login = "http://test.chebufan.cn/chebftest/wx/xlc/account/loginByPassword"
        data = {"account": 13538878368, "password": 123456}
        login = requests.post(url_login, data=data)
        self.assertEqual("登陆成功",login.json()["msg"])

    @classmethod
    def tearDownClass(cls):
        pass



if __name__ == "__main__":
    suite = unittest.TestSuite()
    unittest.main(verbosity=2)