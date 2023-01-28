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



class Profitsku(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global headersvcz
        headersvcz = headers_vcz(13538878368)

        global startTime
        global endTime
        startTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        endTime = datetime.datetime.now()+datetime.timedelta(days=+30)
        endTime = endTime.strftime("%Y-%m-%d %H:%M:%S")

    def test_0_1(self):
        u'''首页—可进入活动详情'''
        #发布付费活动
        startTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        endTime = datetime.datetime.now()+datetime.timedelta(days=+30)
        time.sleep(3)
        url_saveProfitSku = "http://test.chebufan.cn/vcd/api/open/profit/sku/saveProfitSku"
        json = {
                    "data":{
                        "name":"付费活动自动化"+startTime,
                        "salePrice":1,
                        "stock":"8888",
                        "shouldPay":1,
                        "startTime":str(startTime),
                        "endTime":str(endTime),
                        "limitTimes":"50",
                        "validTimeValue": 5,
                        "validTimeUnit": 2,
                        "profitTicketSkuQueryList":[
                            {
                                "name":"付费自动化",
                                "num":2,
                                "originalPrice":8800
                            }
                        ],
                        "profitSkuImageList":[
                            {
                                "imageUrl":"https://test.chebufan.cn/vcdfile/modelName/8/153d1952c1e948529f7324756b4e3b14.webp",
                                "sortNo":1,
                                "imageType":1
                            },
                            {
                                "imageUrl":"https://test.chebufan.cn/vcdfile/modelName/8/21123dba375845b5bbd0b0c70455cebd.webp",
                                "sortNo":2,
                                "imageType":2
                            }
                        ],
                        "type":2,
                        "onePurchaser":1,
                        "onlyNewPurchaser":0,
                        "groupPrice":"",
                        "groupCapacity":2,
                        "supplyPrice":17600,
                        "description":"仅限七座以下非营运车辆可参与,不可与店内其他优惠同时使用,特惠活动购买不退换不折现"
                    },
                    "sign":"nosign",
                    "timestamp":1632993615023
                }
        saveProfitSku = requests.post(url_saveProfitSku,json=json,headers=headersvcd)
        self.assertIn("成功",saveProfitSku.json()["msg"])
        global pay_id
        pay_id = saveProfitSku.json()["data"]["id"]
        print("付费活动id：",pay_id)

        #查看活动详情
        url_detail = "http://test.chebufan.cn/vcd/api/cz/profit/profitSku/detail"
        json = {"data":{"id":pay_id},"sign":"nosign","timestamp":1636014892061}
        detail = requests.post(url_detail,json=json,headers=headersvcz)
        self.assertIn("成功",detail.json()["msg"])
        # print(detail.text)

    def test_0_2(self):
        u'''活动详情—抵扣券—可领取抵扣券'''
        url = "https://test.chebufan.cn/vcd/api/open/profit/sku/saveProfitSku"
        json = {
                    "data": {
                        "name": "抵扣券自动化" +startTime,
                        "startTime": str(startTime),
                        "endTime": str(endTime),
                        "couponValue": 8800,
                        "stock": "50",
                        "validTimeValue": 5,
                        "validTimeUnit": 2,
                        "type": 5
                    },
                    "sign": "nosign",
                    "timestamp": 1658387259525
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertIn("成功",resp.json()["msg"])
        global coupon_id
        coupon_id = resp.json()["data"]["id"]
        print("抵扣券id",coupon_id)
        #领取抵扣券
        url = "https://test.chebufan.cn/vcd/api/cz/profit/profitSku/takeCoupon"
        json = {"data":{"id":coupon_id},"sign":"nosign","timestamp":1658474704566}
        resp = requests.post(url,json=json,headers=headersvcz)
        self.assertIn("成功",resp.json()["msg"])

    def test_0_3(self):
        u'''活动详情—抵扣券—可预约抵扣券'''
        startTime = datetime.datetime.now() + datetime.timedelta(days=+10)
        startTime  = startTime.strftime("%Y-%m-%d %H:%M:%S")
        url = "https://test.chebufan.cn/vcd/api/open/profit/sku/saveProfitSku"
        json = {
                    "data": {
                        "name": "抵扣券自动化" +startTime,
                        "startTime": str(startTime),
                        "endTime": str(endTime),
                        "couponValue": 8800,
                        "stock": "50",
                        "validTimeValue": 5,
                        "validTimeUnit": 2,
                        "type": 5
                    },
                    "sign": "nosign",
                    "timestamp": 1658387259525
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertIn("成功",resp.json()["msg"])
        global coupon_id
        coupon_id = resp.json()["data"]["id"]
        print("抵扣券id",coupon_id)

        #预约抵扣券
        url = "https://test.chebufan.cn/vcd/api/cz/profit/profitSku/orderCoupon"
        json = {"data":{"id":coupon_id},"sign":"nosign","timestamp":1658714361028}
        resp = requests.post(url, json=json, headers=headersvcz)
        self.assertEqual("预约成功",resp.json()["data"])

    def test_0_4(self):
        u'''活动详情—拼团/付费—可不使用抵扣券购买拼团/付费活动'''
        #创建拼团活动
        url_saveProfitSku = "http://test.chebufan.cn/vcd/api/open/profit/sku/saveProfitSku"
        json = {
            "data": {
                "name": "拼团自动化" + startTime,
                "salePrice": 10000,
                "stock": "8888",
                "shouldPay": 1,
                "startTime": str(startTime),
                "endTime": str(endTime),
                "limitTimes": 3,
                "validTimeValue": 5,
                "validTimeUnit": 2,
                "profitTicketSkuQueryList": [
                    {
                        "name": "拼团自动化",
                        "num": 2,
                        "originalPrice": 6600,
                        "remindFlag": 0
                    }
                ],
                "profitSkuImageList": [
                    {
                        "imageUrl": "https://test.chebufan.cn/vcdfile/modelName/8/e4abc2b8f1b444609972f289d870c789.webp",
                        "sortNo": 1,
                        "imageType": 1
                    },
                    {
                        "imageUrl": "https://test.chebufan.cn/vcdfile/modelName/8/21123dba375845b5bbd0b0c70455cebd.webp",
                        "sortNo": 2,
                        "imageType": 2
                    }
                ],
                "type": 3,
                "onePurchaser": 1,
                "onlyNewPurchaser": 0,
                "groupPrice": 5000,
                "groupCapacity": 2,
                "supplyPrice": 13200,
                "description": "仅限七座以下非营运车辆可参与,不可与店内其他优惠同时使用"
            },
            "sign": "nosign",
            "timestamp": 1632994043189
        }
        saveProfitSku = requests.post(url_saveProfitSku, json=json, headers=headersvcd)
        self.assertIn("成功", saveProfitSku.json()["msg"])
        global group_id
        group_id = saveProfitSku.json()["data"]["id"]
        print("拼团活动id：", group_id)
        #创建拼团订单
        url = "https://test.chebufan.cn/vcd/api/cz/profit/profitGroupTeam/create"
        json = {"data":{"id":group_id,"recordId":""},"sign":"nosign","timestamp":1658717507772}
        resp = requests.post(url, json=json, headers=headersvcz)
        group_payid = resp.json()["data"]
        #调起拼团支付
        url = "https://test.chebufan.cn/vcd/api/cz/profit/profitGroupTeam/pay"
        json  = {"data":{"id":group_payid},"sign":"nosign","timestamp":1658717508035}
        resp = requests.post(url, json=json, headers=headersvcz)
        self.assertIn("成功",resp.json()["msg"])

        #创建个人购买订单
        url = "https://test.chebufan.cn/vcd/api/cz/profit/order/submitOrder"
        json = {"data":{"profitSkuId":group_id,"shopId":"1361","recordId":""},"sign":"nosign","timestamp":1658717547336}
        resp = requests.post(url, json=json, headers=headersvcz)
        person_payid = resp.json()["data"]
        #调起个人支付
        url = "https://test.chebufan.cn/vcd/api/cz/profit/order/pay"
        json  = {"data":{"id":person_payid},"sign":"nosign","timestamp":1658717547526}
        resp = requests.post(url, json=json, headers=headersvcz)
        self.assertIn("成功",resp.json()["msg"])

    def test_0_5(self):
        u'''活动详情—付费—可使用抵扣券购买付费活动'''
        #创建拼团活动
        url_saveProfitSku = "http://test.chebufan.cn/vcd/api/open/profit/sku/saveProfitSku"
        json = {
            "data": {
                "name": "拼团自动化" + startTime,
                "salePrice": 10000,
                "stock": "8888",
                "shouldPay": 1,
                "startTime": str(startTime),
                "endTime": str(endTime),
                "limitTimes": 3,
                "validTimeValue": 5,
                "validTimeUnit": 2,
                "profitTicketSkuQueryList": [
                    {
                        "name": "拼团自动化",
                        "num": 2,
                        "originalPrice": 6600,
                        "remindFlag": 0
                    }
                ],
                "profitSkuImageList": [
                    {
                        "imageUrl": "https://test.chebufan.cn/vcdfile/modelName/8/e4abc2b8f1b444609972f289d870c789.webp",
                        "sortNo": 1,
                        "imageType": 1
                    },
                    {
                        "imageUrl": "https://test.chebufan.cn/vcdfile/modelName/8/21123dba375845b5bbd0b0c70455cebd.webp",
                        "sortNo": 2,
                        "imageType": 2
                    }
                ],
                "type": 3,
                "onePurchaser": 1,
                "onlyNewPurchaser": 0,
                "groupPrice": 5000,
                "groupCapacity": 2,
                "supplyPrice": 13200,
                "description": "仅限七座以下非营运车辆可参与,不可与店内其他优惠同时使用"
            },
            "sign": "nosign",
            "timestamp": 1632994043189
        }
        saveProfitSku = requests.post(url_saveProfitSku, json=json, headers=headersvcd)
        self.assertIn("成功", saveProfitSku.json()["msg"])
        global group_id
        group_id = saveProfitSku.json()["data"]["id"]
        print("拼团活动id：", group_id)

        #创建抵扣券
        url = "https://test.chebufan.cn/vcd/api/open/profit/sku/saveProfitSku"
        json = {
                    "data": {
                        "name": "抵扣券自动化" +startTime,
                        "startTime": str(startTime),
                        "endTime": str(endTime),
                        "couponValue": 2000,
                        "stock": "50",
                        "validTimeValue": 5,
                        "validTimeUnit": 2,
                        "type": 5
                    },
                    "sign": "nosign",
                    "timestamp": 1658387259525
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertIn("成功",resp.json()["msg"])
        coupon_id = resp.json()["data"]["id"]
        print("抵扣券活动id",coupon_id)
        #领取抵扣券
        url = "https://test.chebufan.cn/vcd/api/cz/profit/profitSku/takeCoupon"
        json = {"data":{"id":coupon_id},"sign":"nosign","timestamp":1658474704566}
        resp = requests.post(url,json=json,headers=headersvcz)
        print(resp.text)

        # 拥有抵扣券的数量
        url = "https://test.chebufan.cn/vcd/api/cz/eticket/hcxEticket/eticketStatistic"
        json = {
            "data": {
                "shopId": "1361",
                "state": [0]
            },
            "sign": "nosign",
            "timestamp": 1658888556340
        }
        resp = requests.post(url, json=json, headers=headersvcz)
        print(resp.text)
        total = resp.json()["data"]["couponNum"]
        if total % 10 == 0:
            pages = total // 10
            print("页数为：", pages)
        else:
            pages = (total // 10) + 1
            print("页数为：", pages)

        #获取抵扣券id
        url = "https://test.chebufan.cn/vcd/api/cz/profit/profitSku/pageCoupon"
        json = {
                    "data": {
                        "current": pages,
                        "params": {
                            "shopId": "1361",
                            "mobile": "135388788368",
                            "state": 0
                        },
                        "orders": [{}],
                        "shopId": "1361",
                        "mobile": "135388788368",
                        "state": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1658477566430
                }
        resp = requests.post(url, json=json, headers=headersvcz)
        # print("线上优惠券列表：",resp.text)

        coupon_list = resp.json()["data"]["records"]
        for i in coupon_list:
            if i["couponValue"] == 2000:
                ticketid = i["id"]
                continue
        print("领取抵扣券id：",ticketid)

        #创建个人购买订单
        url = "https://test.chebufan.cn/vcd/api/cz/profit/order/submitOrder"
        json = {"data":{"profitSkuId":group_id,"shopId":"1361","recordId":ticketid},"sign":"nosign","timestamp":1658717547336}
        resp = requests.post(url, json=json, headers=headersvcz)
        person_payid = resp.json()["data"]
        #调起个人支付
        url = "https://test.chebufan.cn/vcd/api/cz/profit/order/pay"
        json  = {"data":{"id":person_payid},"sign":"nosign","timestamp":1658717547526}
        resp = requests.post(url, json=json, headers=headersvcz)
        self.assertIn("成功",resp.json()["msg"])

    def test_0_6(self):
        u'''活动详情—拼团—可使用抵扣券购买拼团活动'''
        #创建拼团活动
        url_saveProfitSku = "http://test.chebufan.cn/vcd/api/open/profit/sku/saveProfitSku"
        json = {
            "data": {
                "name": "拼团自动化" + startTime,
                "salePrice": 10000,
                "stock": "8888",
                "shouldPay": 1,
                "startTime": str(startTime),
                "endTime": str(endTime),
                "limitTimes": 3,
                "validTimeValue": 5,
                "validTimeUnit": 2,
                "profitTicketSkuQueryList": [
                    {
                        "name": "拼团自动化",
                        "num": 2,
                        "originalPrice": 6600,
                        "remindFlag": 0
                    }
                ],
                "profitSkuImageList": [
                    {
                        "imageUrl": "https://test.chebufan.cn/vcdfile/modelName/8/e4abc2b8f1b444609972f289d870c789.webp",
                        "sortNo": 1,
                        "imageType": 1
                    },
                    {
                        "imageUrl": "https://test.chebufan.cn/vcdfile/modelName/8/21123dba375845b5bbd0b0c70455cebd.webp",
                        "sortNo": 2,
                        "imageType": 2
                    }
                ],
                "type": 3,
                "onePurchaser": 1,
                "onlyNewPurchaser": 0,
                "groupPrice": 5000,
                "groupCapacity": 2,
                "supplyPrice": 13200,
                "description": "仅限七座以下非营运车辆可参与,不可与店内其他优惠同时使用"
            },
            "sign": "nosign",
            "timestamp": 1632994043189
        }
        saveProfitSku = requests.post(url_saveProfitSku, json=json, headers=headersvcd)
        self.assertIn("成功", saveProfitSku.json()["msg"])
        global group_id
        group_id = saveProfitSku.json()["data"]["id"]
        print("拼团活动id：", group_id)

        #创建抵扣券
        url = "https://test.chebufan.cn/vcd/api/open/profit/sku/saveProfitSku"
        json = {
                    "data": {
                        "name": "抵扣券自动化" +startTime,
                        "startTime": str(startTime),
                        "endTime": str(endTime),
                        "couponValue": 2000,
                        "stock": "50",
                        "validTimeValue": 5,
                        "validTimeUnit": 2,
                        "type": 5
                    },
                    "sign": "nosign",
                    "timestamp": 1658387259525
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertIn("成功",resp.json()["msg"])
        global coupon_id
        coupon_id = resp.json()["data"]["id"]
        print("抵扣券活动id",coupon_id)
        #领取抵扣券
        url = "https://test.chebufan.cn/vcd/api/cz/profit/profitSku/takeCoupon"
        json = {"data":{"id":coupon_id},"sign":"nosign","timestamp":1658474704566}
        resp = requests.post(url,json=json,headers=headersvcz)
        print(resp.text)

        # 拥有抵扣券的数量
        url = "https://test.chebufan.cn/vcd/api/cz/eticket/hcxEticket/eticketStatistic"
        json = {
            "data": {
                "shopId": "1361",
                "state": [0]
            },
            "sign": "nosign",
            "timestamp": 1658888556340
        }
        resp = requests.post(url, json=json, headers=headersvcz)
        print(resp.text)
        total = resp.json()["data"]["couponNum"]
        if total % 10 == 0:
            pages = total // 10
            print("页数为：", pages)
        else:
            pages = (total // 10) + 1
            print("页数为：", pages)

        #获取抵扣券id
        url = "https://test.chebufan.cn/vcd/api/cz/profit/profitSku/pageCoupon"
        json = {
                    "data": {
                        "current": pages,
                        "params": {
                            "shopId": "1361",
                            "mobile": "135388788368",
                            "state": 0
                        },
                        "orders": [{}],
                        "shopId": "1361",
                        "mobile": "135388788368",
                        "state": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1658477566430
                }
        resp = requests.post(url, json=json, headers=headersvcz)
        coupon_list = resp.json()["data"]["records"]
        for i in coupon_list:
            if i["couponValue"] == 2000:
                ticketid = i["id"]
                continue
        # ticketid = resp.json()["data"]["records"][0]["id"]
        # print("领取的抵扣券id：",ticketid)

        #创建拼团订单
        url = "https://test.chebufan.cn/vcd/api/cz/profit/profitGroupTeam/create"
        json = {"data":{"id":group_id,"recordId":ticketid},"sign":"nosign","timestamp":1658717507772}
        resp = requests.post(url, json=json, headers=headersvcz)
        print("创建拼团订单",resp.text)
        group_payid = resp.json()["data"]
        #调起拼团支付
        url = "https://test.chebufan.cn/vcd/api/cz/profit/profitGroupTeam/pay"
        json  = {"data":{"id":group_payid},"sign":"nosign","timestamp":1658717508035}
        resp = requests.post(url, json=json, headers=headersvcz)
        self.assertIn("成功",resp.json()["msg"])

    def test_0_8(self):
        u'''活动详情—分享—拼团/优惠购券/抵扣券可分享活动链接(暂无法测试分享动作，调用接口测试)'''
        self.test_0_2()
        url = "https://test.chebufan.cn/vcd/api/cz/profit/profitSku/share"
        json = {"data":{"id":coupon_id},"sign":"nosign","timestamp":1653534111022}
        resp = requests.post(url,json=json,headers=headersvcz)
        self.assertEqual("成功",resp.json()["msg"])

    def test_0_9(self):
        u'''活动详情—拼团/优惠购券/抵扣券可生成海报并识别小程序二维码（暂无法测试识别动作，调用接口验证是否生成图片）'''
        self.test_0_2()
        url = "https://test.chebufan.cn/vcd/api/open/wx/miniapp/getWxAcodeUnlimit"
        json = {"data":{"page":"pages_coupon/couponGet/index","scene":"t=1&id=%s"%(coupon_id),"miniFlag":1},"sign":"nosign","timestamp":1653534118550}
        resp = requests.post(url, json=json, headers=headersvcz)
        self.assertEqual("成功",resp.json()["msg"])


    @classmethod
    def tearDownClass(cls):
        pass



if __name__ == "__main__":
    unittest.main(verbosity=2)