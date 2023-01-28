# -*- encoding=utf8 -*-
__author__ = "HXH"

import unittest
import requests
import datetime
import  time
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
COMMON_DIR = os.path.join(BASE_DIR,"config")
sys.path.append(COMMON_DIR)
from common import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_cxgj,headers_admin_formdata,vpt_header


class Bind_Shop(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global headersvcz
        headersvcz = headers_vcz(13538878368)
    # def test_01(self):
    #     u'''门店公众号分享报价单—v车主可绑定订单归属门店（暂无法测试绑定动作，调用绑定门店接口测试）'''

    # def test_02(self):
    #     u'''v车主小程序分享报价单—v车主可绑定订单归属门店（暂无法测试绑定动作，调用绑定门店接口测试）'''

    def test_03(self):
        u'''绑定门店—筛选—可筛选门店地区和类型'''
        url = "https://test.chebufan.cn/vcd/api/cz/shop/page"
        json = {
                    "data": {
                        "current": 1,
                        "size": 10,
                        "pages": 0,
                        "params": {
                            "type": "",
                            "latitude": 23.135547751746262,
                            "longitude": 113.35686948588241,
                            "cityCode": "440",
                            "areaCode": "440106"
                        },
                        "total": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1653537113301
                }
        resp = requests.post(url,json=json,headers=headersvcz)
        self.assertEqual("成功",resp.json()["msg"])


    def test_04(self):
        u'''绑定门店—选择—可选择门店绑定并返回首页'''
        url = "https://test.chebufan.cn/vcd/api/cz/shop/page"
        for i in range(1,6):
            json = {
                "data": {
                    "current": 1,
                    "size": 10,
                    "pages": 0,
                    "params": {
                        "type": "%d"%(i),
                        "latitude": 23.135547751746262,
                        "longitude": 113.35686948588241,
                        "cityCode": "440",
                        "areaCode": "440106"
                    },
                    "total": 1
                },
                "sign": "nosign",
                "timestamp": 1653537113301
            }
            resp = requests.post(url,json=json,headers=headersvcz)
            self.assertEqual("成功",resp.json()["msg"])

    # def test_05(self):
    #     u'''绑定门店—微信二维码扫码—v车主可绑定门店'''

    @classmethod
    def tearDownClass(cls):
        pass



if __name__ == "__main__":
    suite = unittest.TestSuite()
    unittest.main(verbosity=2)