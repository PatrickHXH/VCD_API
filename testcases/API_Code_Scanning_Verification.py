# -*- encoding=utf8 -*-
__author__ = "HXH"

import unittest
import requests
import datetime
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
COMMON_DIR = os.path.join(BASE_DIR,"config")
sys.path.append(COMMON_DIR)
from common import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_cxgj,headers_admin_formdata,vpt_header

class Code_Scanning_Verification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global  headersvcz
        headersvcz = headers_vcz(13538878368)

    def test_01(self):
        u'''扫码核验—核验—可核验优惠券'''
        #使用套餐卡，发送优惠券
        url_svipcardadd = "https://test.chebufan.cn/vcd/api/open/profit/sku/comboCard/add"
        json = {
                    "data": {
                        "name": "套餐卡自动化",
                        "salePrice": "66",
                        "descriptions": ["特惠活动购买不退换不折现", "优惠券以及金额等权益过期作废不予退还"],
                        "tickets": [{
                            "name": "自动化",
                            "num": 2,
                            "originalPrice": "99"
                        }],
                        "openAward": 1,
                        "awardRate": "30",
                        "validTimeValue": 6,
                        "validTimeUnit": 2,
                        "imageUrl": "https://cbfoss.oss-cn-guangzhou.aliyuncs.com/vcd/miniapp/svip/black.png?versionId=CAEQEhiBgMDZ2pnA8xciIDBjYTJiMmZjZDFhNTRhMTBiZDE3NmNhNjk1YmY0Nzg3",
                        "supplyPrice": "198"
                    },
                    "sign": "nosign",
                    "timestamp": 1644284732457
                }
        svipcardadd = requests.post(url_svipcardadd,json=json,headers=headersvcd)
        self.assertIn("成功",svipcardadd.json()['msg'])
        carid = svipcardadd.json()["data"]["id"]

        #搜索用户信息
        url_customerdetail = "https://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/customerDetail"
        json = {
                    "data": {
                        "phone": "13538878368"
                    },
                    "sign": "nosign",
                    "timestamp": 1644304692879
                }
        customerdetail = requests.post(url_customerdetail,json=json,headers=headersvcd)
        global  accountId
        accountId = customerdetail.json()["data"]["accountId"]

        #开套餐卡
        self.assertIn("成功",customerdetail.json()["msg"])
        false = False
        true = True
        url_create = "https://test.chebufan.cn/vcd/api/open/profit/sku/comboCard/create"
        json = {
                    "data": {
                        "accountId": accountId,
                        "czPhone": "13538878368",
                        "amount": "",
                        "otherAmount": "",
                        "payType": 3,
                        "salesperson": "",
                        "cardId": carid,
                        "ignoreRepeatedCreateTips": false,
                        "licenseNoList": ["粤DGEC11"],
                        "receiveMoney": 96,
                    },
                    "sign": "nosign",
                    "timestamp": 1644304629295
                }
        create = requests.post(url_create,json=json,headers=headersvcd)
        self.assertIn("成功",create.json()["msg"])

        #查询车主优惠券列表
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
        print(resp.text)
        id = resp.json()['data']['records'][0]['id']

        #查询最新优惠券code
        url_code = "http://test.chebufan.cn/vcd/api/cz/eticket/hcxEticket/get"
        json = {"data":{"id":id,"longitude":113.35693359375,"latitude":23.13553810119629},"sign":"nosign","timestamp":1629100773231}
        code = requests.post(url_code,json=json,headers=headersvcz)
        code_text = code.json()['data']['code']
        print("券码为：",code_text)

        #核验优惠券
        url_checkinfo = "http://test.chebufan.cn/vcd/api/open/eticket/check/info"
        json = {"data":code_text,"sign":"nosign","timestamp":1631692763463}
        checkinfo = requests.post(url_checkinfo,json=json,headers=headersvcd)
        # print(checkinfo.text)
        self.assertIn("成功",checkinfo.json()["msg"])

        #确认核验
        url_check = "http://test.chebufan.cn/vcd/api/open/eticket/check"
        json = {"data":{"eticketCode":code_text},"sign":"nosign","timestamp":1631693510287}
        check = requests.post(url_check,json=json,headers=headersvcd)
        print(check.text)
        self.assertIn("自动化",check.json()["data"]["product"])

    def test_02(self):
        u'''扫码核验—验券记录—可筛选查看验券记录表且字段正确'''
        #使用套餐卡，发送优惠券
        url_svipcardadd = "https://test.chebufan.cn/vcd/api/open/profit/sku/comboCard/add"
        json = {
                    "data": {
                        "name": "套餐卡自动化",
                        "salePrice": "66",
                        "descriptions": ["特惠活动购买不退换不折现", "优惠券以及金额等权益过期作废不予退还"],
                        "tickets": [{
                            "name": "自动化",
                            "num": 2,
                            "originalPrice": "99"
                        }],
                        "openAward": 1,
                        "awardRate": "30",
                        "validTimeValue": 6,
                        "validTimeUnit": 2,
                        "imageUrl": "https://cbfoss.oss-cn-guangzhou.aliyuncs.com/vcd/miniapp/svip/black.png?versionId=CAEQEhiBgMDZ2pnA8xciIDBjYTJiMmZjZDFhNTRhMTBiZDE3NmNhNjk1YmY0Nzg3",
                        "supplyPrice": "198"
                    },
                    "sign": "nosign",
                    "timestamp": 1644284732457
                }
        svipcardadd = requests.post(url_svipcardadd,json=json,headers=headersvcd)
        self.assertIn("成功",svipcardadd.json()['msg'])
        carid = svipcardadd.json()["data"]["id"]

        #搜索用户信息
        url_customerdetail = "https://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/customerDetail"
        json = {
                    "data": {
                        "phone": "13538878368"
                    },
                    "sign": "nosign",
                    "timestamp": 1644304692879
                }
        customerdetail = requests.post(url_customerdetail,json=json,headers=headersvcd)
        global  accountId
        accountId = customerdetail.json()["data"]["accountId"]

        #开套餐卡
        self.assertIn("成功",customerdetail.json()["msg"])
        false = False
        true = True
        url_create = "https://test.chebufan.cn/vcd/api/open/profit/sku/comboCard/create"
        json = {
                    "data": {
                        "accountId": accountId,
                        "czPhone": "13538878368",
                        "amount": "",
                        "otherAmount": "",
                        "payType": 3,
                        "salesperson": "",
                        "cardId": carid,
                        "ignoreRepeatedCreateTips": false,
                        "licenseNoList": ["粤DGEC11"],
                        "receiveMoney": 96,
                    },
                    "sign": "nosign",
                    "timestamp": 1644304629295
                }
        create = requests.post(url_create,json=json,headers=headersvcd)
        self.assertIn("成功",create.json()["msg"])

        #查询车主优惠券列表
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
        print(resp.text)
        id = resp.json()['data']['records'][0]['id']

        #查询最新优惠券code
        url_code = "http://test.chebufan.cn/vcd/api/cz/eticket/hcxEticket/get"
        json = {"data":{"id":id,"longitude":113.35693359375,"latitude":23.13553810119629},"sign":"nosign","timestamp":1629100773231}
        code = requests.post(url_code,json=json,headers=headersvcz)
        code_text = code.json()['data']['code']
        print("券码为：",code_text)

        #核验优惠券
        url_checkinfo = "http://test.chebufan.cn/vcd/api/open/eticket/check/info"
        json = {"data":code_text,"sign":"nosign","timestamp":1631692763463}
        checkinfo = requests.post(url_checkinfo,json=json,headers=headersvcd)
        # print(checkinfo.text)
        self.assertIn("成功",checkinfo.json()["msg"])

        #确认核验
        url_check = "http://test.chebufan.cn/vcd/api/open/eticket/check"
        json = {"data":{"eticketCode":code_text},"sign":"nosign","timestamp":1631693510287}
        check = requests.post(url_check,json=json,headers=headersvcd)
        # print(check.text)
        self.assertIn("自动化",check.json()["data"]["product"])

        #查看验券列表
        url_checklist = "https://test.chebufan.cn/vcd/api/open/eticket/check/list"
        Date = datetime.datetime.now().strftime("%Y-%m-%d")
        json = {"data":{"current":1,"params":{"startDate":Date,"endDate":Date,"condition":"","verifyEvidence":"","picState":""}},"sign":"nosign","timestamp":1631694341314}
        checklist = requests.post(url_checklist,json=json,headers=headersvcd)
        print(checklist.text)
        self.assertIn("自动化",checklist.json()["data"]["records"][0]["product"])
        self.assertIn("黄管理2", checklist.json()["data"]["records"][0]["creator"])

    def test_03(self):
        u'''扫码核验—验券记录—详情—支持根据手机号和券名称搜索'''
        #使用套餐卡，发送优惠券
        url_svipcardadd = "https://test.chebufan.cn/vcd/api/open/profit/sku/comboCard/add"
        json = {
                    "data": {
                        "name": "套餐卡自动化",
                        "salePrice": "66",
                        "descriptions": ["特惠活动购买不退换不折现", "优惠券以及金额等权益过期作废不予退还"],
                        "tickets": [{
                            "name": "自动化",
                            "num": 2,
                            "originalPrice": "99"
                        }],
                        "openAward": 1,
                        "awardRate": "30",
                        "validTimeValue": 6,
                        "validTimeUnit": 2,
                        "imageUrl": "https://cbfoss.oss-cn-guangzhou.aliyuncs.com/vcd/miniapp/svip/black.png?versionId=CAEQEhiBgMDZ2pnA8xciIDBjYTJiMmZjZDFhNTRhMTBiZDE3NmNhNjk1YmY0Nzg3",
                        "supplyPrice": "198"
                    },
                    "sign": "nosign",
                    "timestamp": 1644284732457
                }
        svipcardadd = requests.post(url_svipcardadd,json=json,headers=headersvcd)
        self.assertIn("成功",svipcardadd.json()['msg'])
        carid = svipcardadd.json()["data"]["id"]

        #搜索用户信息
        url_customerdetail = "https://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/customerDetail"
        json = {
                    "data": {
                        "phone": "13538878368"
                    },
                    "sign": "nosign",
                    "timestamp": 1644304692879
                }
        customerdetail = requests.post(url_customerdetail,json=json,headers=headersvcd)
        global  accountId
        accountId = customerdetail.json()["data"]["accountId"]

        #开套餐卡
        self.assertIn("成功",customerdetail.json()["msg"])
        false = False
        true = True
        url_create = "https://test.chebufan.cn/vcd/api/open/profit/sku/comboCard/create"
        json = {
                    "data": {
                        "accountId": accountId,
                        "czPhone": "13538878368",
                        "amount": "",
                        "otherAmount": "",
                        "payType": 3,
                        "salesperson": "",
                        "cardId": carid,
                        "ignoreRepeatedCreateTips": false,
                        "licenseNoList": ["粤DGEC11"],
                        "receiveMoney": 96,
                    },
                    "sign": "nosign",
                    "timestamp": 1644304629295
                }
        create = requests.post(url_create,json=json,headers=headersvcd)
        self.assertIn("成功",create.json()["msg"])

        #查询车主优惠券列表
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
        print(resp.text)
        id = resp.json()['data']['records'][0]['id']

        #查询最新优惠券code
        url_code = "http://test.chebufan.cn/vcd/api/cz/eticket/hcxEticket/get"
        json = {"data":{"id":id,"longitude":113.35693359375,"latitude":23.13553810119629},"sign":"nosign","timestamp":1629100773231}
        code = requests.post(url_code,json=json,headers=headersvcz)
        code_text = code.json()['data']['code']
        print("券码为：",code_text)

        #核验优惠券
        url_checkinfo = "http://test.chebufan.cn/vcd/api/open/eticket/check/info"
        json = {"data":code_text,"sign":"nosign","timestamp":1631692763463}
        checkinfo = requests.post(url_checkinfo,json=json,headers=headersvcd)
        # print(checkinfo.text)
        self.assertIn("成功",checkinfo.json()["msg"])

        #确认核验
        url_check = "http://test.chebufan.cn/vcd/api/open/eticket/check"
        json = {"data":{"eticketCode":code_text},"sign":"nosign","timestamp":1631693510287}
        check = requests.post(url_check,json=json,headers=headersvcd)
        # print(check.text)
        self.assertIn("自动化",check.json()["data"]["product"])

        #搜索手机号和名称
        url_checklist = "http://test.chebufan.cn/vcd/api/open/eticket/check/list"
        Date = datetime.datetime.now().strftime("%Y-%m-%d")
        json = {"data":{"current":1,"params":{"startDate":Date,"endDate":Date,"condition":"13538878368","verifyEvidence":"","picState":""}},"sign":"nosign","timestamp":1631694341314}
        checklist = requests.post(url_checklist,json=json,headers=headersvcd)
        print(checklist.text)
        self.assertNotEqual("0",str(checklist.json()["data"]["total"]))
        self.assertIn("自动化", checklist.json()["data"]["records"][0]["product"])
        self.assertIn("13538878368", checklist.json()["data"]["records"][0]["useMobile"])


    @classmethod
    def tearDownClass(cls):
        pass



if __name__ == "__main__":
    suite = unittest.TestSuite()
    unittest.main(verbosity=2)