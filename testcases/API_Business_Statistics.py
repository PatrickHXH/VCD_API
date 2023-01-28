# -*- encoding=utf8 -*-
__author__ = "HXH"

import random
import time
import unittest
import requests
import datetime
import  string
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
COMMON_DIR = os.path.join(BASE_DIR,"config")
sys.path.append(COMMON_DIR)
from common import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_cxgj,headers_admin_formdata,vpt_header

class Business_Statistics(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global  headersvcz
        headersvcz = headers_vcz(13538878368)

        global headersadmin
        headersadmin = headers_admin()

        global headersgzh
        headersgzh = cookies_headers_gzh(13538878368,123456)

        global  headerscxgj
        headerscxgj = headers_cxgj()

        global headers_admin_formdata
        headers_admin_formdata = headers_admin_formdata()
    def test_0_1(self):
        u''''经营看板—经营统计—可跳转经营统计页'''
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        now = datetime.datetime.now()
        offset = datetime.timedelta(days=+1)
        nextday =(now+offset).strftime("%Y-%m-%d")
        #获取字典
        url = "https://test.chebufan.cn/vcd/api/open/ext/dict/getSonDictByPcodes"
        json = {"data":{"code":"ShopBusinessIncomeType"},"sign":"nosign","timestamp":1653378789566}
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",resp.json()["msg"])
        #获取经营统计金额
        url = "https://test.chebufan.cn/vcd/api/open/shop/incomeData"
        json = {"data":{"startTime":today,"endTime":nextday},"sign":"nosign","timestamp":1653378789573}
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",resp.json()["msg"])

    def test_0_2(self):
        u''''经营看板—经营统计—车险积分和营销活动可跳转积分明细页，会员卡销售、接车开单、美团、平安车主、v养车、车主服务可跳转业务明细页'''
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        now = datetime.datetime.now()
        offset = datetime.timedelta(days=+1)
        nextday =(now+offset).strftime("%Y-%m-%d")
        for i in range(4,9):
            #获取业务明细
            url = "https://test.chebufan.cn/vcd/api/open/shop/incomeDetailPage"
            json = {
                    "data": {
                        "current": 1,
                        "size": 10,
                        "pages": 0,
                        "params": {
                            "type": i,
                            "startTime": today,
                            "endTime": nextday
                        },
                        "total": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1653380799416
                }
            resp = requests.post(url,json=json,headers=headersvcd)
            self.assertEqual("成功",resp.json()["msg"])
            #获取页面明细订单笔数和金额
            url = "https://test.chebufan.cn/vcd/api/open/shop/incomeDetailStatistics"
            json = {
                    "data": {
                        "type": i,
                        "startTime": today,
                        "endTime": nextday
                    },
                    "sign": "nosign",
                    "timestamp": 1653380799419
                }
            resp = requests.post(url,json=json,headers=headersvcd)
            self.assertEqual("成功",resp.json()["msg"])

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)