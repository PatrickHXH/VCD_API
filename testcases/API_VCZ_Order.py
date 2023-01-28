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


class Order(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global headersvcz
        headersvcz = headers_vcz(13538878368)
    def test_01(self):
        u'''订单—可查看活动单列表（待完善）'''
        url_profitlist = "http://test.chebufan.cn/vcd/api/cz/profit/order/list"
        json = {"data":{"current":1,"params":{"shopId":"1361"}},"sign":"nosign","timestamp":1636008300749}
        profitlist = requests.post(url_profitlist,json=json,headers=headersvcz)
        self.assertIn("成功",profitlist.json()["msg"])
    def test_02(self):
        u'''订单—可查看到店单列表'''
        #查看到点单列表
        url_ycxReceivelist = "http://test.chebufan.cn/vcd/api/cz/receive/ycxReceive/page"
        json = {"data":{"current":1,"params":{"shopId":"1361"}},"sign":"nosign","timestamp":1636008301835}
        ycxReceivelist = requests.post(url_ycxReceivelist,json=json,headers=headersvcz)
        self.assertIn("成功",ycxReceivelist.json()["msg"])
    def test_03(self):
        u'''订单—可查看违章订单列表（待完善）'''
        url_queryList = "http://test.chebufan.cn/vcd/api/cz/pecc/peccOrder/queryList"
        json = {"data":{"current":1,"params":{"shopId":"1361"}},"sign":"nosign","timestamp":1636008304263}
        queryList = requests.post(url_queryList,json=json,headers=headersvcz)
        self.assertIn("成功",queryList.json()["msg"])

    # def test_04(self):
    #     u'''订单—可查看商品订单列表'''
    #     null = None
    #     url_orderpage = "http://test.chebufan.cn/mall/api/mall/mini/order/page"
    #     json ={"data":{"current":1,"size":8,"params":{"state":null,"orderType":null}},"timestamp":1636008314464,"sign":"nosign"}
    #     orderpage = requests.post(url_orderpage,json=json,headers=headers_vcz)
    #     self.assertIn("成功",orderpage.json()["msg"])
    @classmethod
    def tearDownClass(cls):
        pass



if __name__ == "__main__":
    suite = unittest.TestSuite()
    # suite.addTest(Order("test_01"))
    # suite.addTest(Order("test_02"))
    # suite.addTest(Order("test_03"))
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(suite)
    unittest.main(verbosity=2)