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

class Shop_Info(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global  headersvcz
        headersvcz = headers_vcz(13538878368)

        global headersadmin
        headersadmin = headers_admin()

        global  headerscxgj
        headerscxgj = headers_cxgj()

        global headers_admin_formdata
        headers_admin_formdata = headers_admin_formdata()
    def test_0_1(self):
        u''''系统付费—已开通—可使用v车店功能'''
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        #查询门店是否开通付费功能
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopLicence/licenceInfo"
        json = {"data":{},"sign":"nosign","timestamp":1653364277178}
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual(0,resp.json()["data"]["licenceFlag"])
        #开通
        url = "https://test.chebufan.cn/vcd/api/shop/shopLicenceLog/add"
        json = {"timestamp":1653371094826,"sign":"nosign","data":{"shopId":"1361","validDateBegin":now,"validDateEnd":"2040-06-30"}}
        resp = requests.post(url,json=json,headers=headersadmin)
        #查询开通记录
        url ="https://test.chebufan.cn/vcd/api/shop/shopLicenceLog/page"
        json = {"timestamp":1653372751216,"sign":"nosign","data":{"size":10,"current":1,"params":{"shopId":"1361"},"orders":[]}}
        resp = requests.post(url,json=json,headers=headersadmin)
        currentpage = resp.json()["data"]["pages"]
        print("共几页",currentpage)
        #查询门店是否开通付费功能
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopLicence/licenceInfo"
        json = {"data":{},"sign":"nosign","timestamp":1653364277178}
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual(1,resp.json()["data"]["licenceFlag"])
        #查询开通记录
        url ="https://test.chebufan.cn/vcd/api/shop/shopLicenceLog/page"
        json = {"timestamp":1653372751216,"sign":"nosign","data":{"size":10,"current":currentpage,"params":{"shopId":"1361"},"orders":[]}}
        resp = requests.post(url,json=json,headers=headersadmin)
        print(resp.text)
        total= resp.json()["data"]["total"]
        size = resp.json()["data"]["size"]
        if total == 10 and size ==10:
            currentpagenum = 10
        else:
            currentpagenum = total - size * (currentpage - 1)
        print("当前页数开通记录数量：",currentpagenum)
        for i in range(0,currentpagenum):
            record = resp.json()["data"]["records"][i]["state"]
            if record == 1:
                startupid = resp.json()["data"]["records"][i]["id"]
            else:
                pass
        print("启用中的id：",startupid)
        #撤销记录
        url = "https://test.chebufan.cn/vcd/api/shop/shopLicenceLog/revoke"
        json = {"timestamp":1653372754716,"sign":"nosign","data":{"id":startupid}}
        resp = requests.post(url,json=json,headers=headersadmin)
        self.assertEqual("成功",resp.json()["msg"])


    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)