# -*- encoding=utf8 -*-
__author__ = "HXH"

import unittest
import requests
import pymysql
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
COMMON_DIR = os.path.join(BASE_DIR,"config")
sys.path.append(COMMON_DIR)
from common import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_cxgj,headers_admin_formdata,vpt_header


class Love_Car(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global headersvcz
        headersvcz = headers_vcz(13538878368)

    def test_01(self):
        u'''爱车—优惠券—v车主可查看优惠券列表且统计正确'''
        url = "https://test.chebufan.cn/vcd/api/cz/eticket/hcxEticket/eticketPage"
        json = {
                        "data": {
                            "current": 1,
                            "params": {
                                "shopId": "1361",
                                "mobile": "13538878368",
                                "state": 0
                            },
                            "orders": [{}],
                            "shopId": "1361",
                            "mobile": "13538878368",
                            "state": 0
                        },
                        "sign": "nosign",
                        "timestamp": 1673404937425
                    }
        resp = requests.post(url,json=json,headers=headersvcz)
        total = resp.json()["data"]["total"]
        print(total)

        #连接数据库
        conn = pymysql.connect(host="121.201.18.86",port=3325,user="root",passwd="Joysim!@#832727",db="cbf")
        #创建游标
        cur = conn.cursor()
        #查询车主accountid
        sql0 = "SELECT account_id FROM tb_cz_user WHERE phone = 13538878368 and agency_type = 2"
        cur.execute(sql0)
        accountid = cur.fetchall()
        accountid = accountid[0][0]

        #查询优惠券数量
        sql1 = "SELECT count(*) FROM hcx_eticket  WHERE repair_id = 1315 and (mobile = 17324233289 and  account_id = %d) and state = 0 "%accountid
        #执行游标
        cur.execute(sql1)
        total1 = cur.fetchall()
        total1 = total1[0][0]
        sql2 =  "SELECT count(*) FROM hcx_eticket WHERE repair_id =1315 and (mobile = 17324233289 and  account_id IS NULL) and state = 0"
        #执行游标
        cur.execute(sql2)
        total2 = cur.fetchall()
        total2 = total2[0][0]
        actual = total1 + total2
        assert_equal = (total,actual)

    def test_02(self):
        u'''爱车—报价单详情—可查看详情'''
        url_getChexianOrder = "http://test.chebufan.cn/vcd/api/cz/chexian/chexianOrderCzRel/getChexianOrder"
        json = {"data":{"id":"19246"},"sign":"nosign","timestamp":1635837206890}
        getChexianOrder = requests.post(url_getChexianOrder,json=json,headers=headersvcz)
        self.assertIn("成功",getChexianOrder.json()["msg"])

    def test_03(self):
        u'''爱车—更多报价单—可跳转报价单列表'''
        url_pageChexianOrder = "http://test.chebufan.cn/vcd/api/cz/chexian/chexianOrderCzRel/pageChexianOrder"
        json = {"data":{"current":1,"params":{"shopId":"1361"}},"sign":"nosign","timestamp":1635838754583}
        pageChexianOrder = requests.post(url_pageChexianOrder,json=json,headers=headersvcz)
        self.assertIn("18326", pageChexianOrder.json()["data"]["records"][2]["id"])

    def test_04(self):
        u'''爱车—更多电子保单—可跳转电子保单列表'''
        url_chexianPolicyCzRel = "http://test.chebufan.cn/vcd/api/cz/chexian/chexianPolicyCzRel/page"
        json = {"data":{"current":1,"params":{"shopId":"1361"}},"sign":"nosign","timestamp":1635839672011}
        chexianPolicyCzRel = requests.post(url_chexianPolicyCzRel,json=json,headers=headersvcz)
        print(chexianPolicyCzRel.text)
        self.assertIn("粤A3L20R",chexianPolicyCzRel.json()["data"]["records"][0]["licenseNo"])

    def test_05(self):
        u'''爱车—电子保单—电子保单详情可验证'''
        url = "https://test.chebufan.cn/vcd/api/cz/chexian/chexianPolicyCzRel/verify"
        json = {"data":{"id":"1512254138084945921","code":"111111"},"sign":"nosign","timestamp":1649384592086}
        verify = requests.post(url,json=json,headers=headersvcz)
        self.assertIn("输入的证件号有误",verify.json()["msg"])

    def test_06(self):
        u'''爱车—设置—可切换门店'''
        url_pageShop = "http://test.chebufan.cn/vcd/api/cz/czuser/czAccountShopRel/pageShop"
        json = {"data":{"current":1,"params":{"textSearch":"","latitude":"23.12463","longitude":"113.36199"}},"sign":"nosign","timestamp":1635921285972}
        pageShop = requests.post(url_pageShop,json=json,headers=headersvcz)
        shop1= pageShop.json()["data"]['records'][0]["shopId"]
        shop2= pageShop.json()["data"]['records'][1]["shopId"]
        print("门店id：",shop1)
        print("门店id：",shop2)
        #切换门店
        url = "https://test.chebufan.cn/vcd/api/cz/czuser/czAccountShopRel/bind"
        json = {"data":{"id":shop1},"sign":"nosign","timestamp":1649385386066}
        bind = requests.post(url,json=json,headers=headersvcz)
        self.assertIn("成功",bind.json()["msg"])
        json = {"data":{"id":shop2},"sign":"nosign","timestamp":1649385386066}
        bind = requests.post(url,json=json,headers=headersvcz)
        self.assertIn("成功", bind.json()["msg"])
    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)