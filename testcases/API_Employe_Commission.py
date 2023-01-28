# -*- encoding=utf8 -*-
__author__ = "HXH"

import datetime
import time
import unittest
import requests
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
COMMON_DIR = os.path.join(BASE_DIR,"config")
sys.path.append(COMMON_DIR)
from common import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_cxgj,headers_admin_formdata,vpt_header
import random
import string
import pymysql
import time

class Employe_Commission(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global headersvcz
        headersvcz = headers_vcz(13538878368)

        self.receiveTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def test_0_1(self):
        u'''员工绩效—绩效管理—会员卡提成—可作废且作废后到已作废列表'''
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
                        "salesperson": "1421",
                        "cardId": 1517030361206063106,
                        "ignoreRepeatedCreateTips": true,
                        "licenseNoList": ["粤DGEC11"],
                        "receiveMoney": 96,
                    },
                    "sign": "nosign",
                    "timestamp": 1644304629295
                }
        create = requests.post(url_create,json=json,headers=headersvcd)
        self.assertIn("成功",create.json()["msg"])
        #进入会员卡提成列表
        month = datetime.datetime.now().strftime("%Y-%m")  #获取当前月份
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page"
        json = {
                    "data": {
                        "date": month,
                        "state": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1650523489211
                }
        list = requests.post(url,json=json,headers=headersvcd)
        id_1 = list.json()["data"]["records"][0]["id"]
        #作废提成
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/updateState"
        json = {
                    "data": {
                        "id": [id_1],
                        "state": 9
                    },
                    "sign": "nosign",
                    "timestamp": 1650523918508
                }
        updatestate = requests.post(url,json=json,headers=headersvcd)
        #查看作废列表
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page"
        json = {
                    "data": {
                        "date": month,
                        "state": 9
                    },
                    "sign": "nosign",
                    "timestamp": 1650523489211
                }
        list = requests.post(url,json=json,headers=headersvcd)
        id_2 = list.json()["data"]["records"][0]["id"]
        #断言作废列表id
        self.assertEqual(id_1,id_2)

    def test_0_2(self):
        u'''员工绩效—绩效管理—会员卡提成—可确认且确认后到已确认列表'''
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
                        "salesperson": "1421",
                        "cardId": 1517030361206063106,
                        "ignoreRepeatedCreateTips": true,
                        "licenseNoList": ["粤DGEC11"],
                        "receiveMoney": 96,
                    },
                    "sign": "nosign",
                    "timestamp": 1644304629295
                }
        create = requests.post(url_create,json=json,headers=headersvcd)
        self.assertIn("成功",create.json()["msg"])
        #进入会员卡提成列表
        month = datetime.datetime.now().strftime("%Y-%m")  #获取当前月份
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page"
        json = {
                    "data": {
                        "date": month,
                        "state": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1650523489211
                }
        list = requests.post(url,json=json,headers=headersvcd)
        id_1 = list.json()["data"]["records"][0]["id"]
        #确认提成
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/updateState"
        json = {
                    "data": {
                        "id": [id_1],
                        "state": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1650523918508
                }
        updatestate = requests.post(url,json=json,headers=headersvcd)
        #查看确认列表
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page"
        json = {
                    "data": {
                        "date": month,
                        "state": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1650523489211
                }
        list = requests.post(url,json=json,headers=headersvcd)
        id_2 = list.json()["data"]["records"][0]["id"]
        #断言确认列表id
        self.assertEqual(id_1,id_2)

    def test_0_3(self):
        u'''员工绩效—绩效管理—会员卡提成—可发放提成且到已发放列表'''
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
                        "salesperson": "1421",
                        "cardId": 1517030361206063106,
                        "ignoreRepeatedCreateTips": true,
                        "licenseNoList": ["粤DGEC11"],
                        "receiveMoney": 96,
                    },
                    "sign": "nosign",
                    "timestamp": 1644304629295
                }
        create = requests.post(url_create,json=json,headers=headersvcd)
        self.assertIn("成功",create.json()["msg"])

        time.sleep(3)
        #进入会员卡提成列表
        month = datetime.datetime.now().strftime("%Y-%m")  #获取当前月份
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page"
        json = {
                    "data": {
                        "date": month,
                        "state": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1650523489211
                }
        list = requests.post(url,json=json,headers=headersvcd)
        id_1 = list.json()["data"]["records"][0]["id"]
        #确认提成
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/updateState"
        json = {
                    "data": {
                        "id": [id_1],
                        "state": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1650523918508
                }
        updatestate = requests.post(url,json=json,headers=headersvcd)

        time.sleep(3)
        #查看确认列表
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page"
        json = {
                    "data": {
                        "date": month,
                        "state": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1650523489211
                }
        list = requests.post(url,json=json,headers=headersvcd)
        id_2 = list.json()["data"]["records"][0]["id"]
        #发放提成
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/confirmAndPay"
        json = {
                    "data": {
                        "ids": [id_2],
                        "type": [1]
                    },
                    "sign": "nosign",
                    "timestamp": 1650524850924
                }
        confirmAndPay = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",confirmAndPay.json()["msg"])

        time.sleep(3)
        #查看提成完成列表
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page"
        json = {
                    "data": {
                        "date": month,
                        "state": 3
                    },
                    "sign": "nosign",
                    "timestamp": 1650523489211
                }
        list = requests.post(url,json=json,headers=headersvcd)
        id_2 = list.json()["data"]["records"][0]["id"]
        self.assertEqual(id_1,id_2)

    def test_0_4(self):
        u'''员工绩效—绩效管理—接车订单提成—可作废且作废后到已作废列表'''
        #更新车辆信息的门店表，随机车牌
        month = datetime.datetime.now().strftime("%Y-%m")  #获取当前月份
        a = ''.join(random.sample(string.ascii_letters , 3))
        b = ''.join(random.sample(string.digits, 3))
        carNo = "粤"+a.upper()+b
        print("车牌号：",carNo)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #查询车牌id
        url = "https://test.chebufan.cn/vcd/api/open/receive/ycxReceive/getCarCondition"
        json = {
                    "data": {
                        "carNo": carNo
                    },
                    "sign": "nosign",
                    "timestamp": 1654753145527
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        carId = resp.json()["data"]["ycxRepairCar"]["id"]
        print("车牌id：",carId)
        #接车开单
        false = False
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/add"
        json = {
                    "data": {
                        "carId": carId,
                        "brandIcon": "",
                        "brandName": "",
                        "modelName": "",
                        "carNo": carNo,
                        "carNoFlag": 1,
                        "mileage": "",
                        "carVin": "",
                        "czName": "",
                        "czPhone": "",
                        "violation": false,
                        "renewal": false,
                        "maintenance": false,
                        "annual": false,
                        "followThePublicAccount": false,
                        "existAccountCard": false,
                        "existComboCard": false,
                        "carDetectionNum": 0,
                        "carDetectionQuoteNum": 0,
                        "price": "88",
                        "award": 0,
                        "model": "",
                        "modelItem": "",
                        "kilometer": "",
                        "relPhone": "",
                        "sendMan": "",
                        "oil": "",
                        "remark": "",
                        "receiveTime": self.receiveTime,
                        "itemList": [{
                            "name": "洗车自动化",
                            "price": 88,
                            "type": "1",
                            "id": "1510164398556831745",
                            "num": 1,
                            "imgBool": false,
                            "award": 0,
                            "projectDistributionRule": [],
                            "key": "1510164398556831745",
                            "sellerId": "1297",
                            "projectId": "1510164398556831745"
                        }],
                        "pendingOrderId": ""
                    },
                    "sign": "nosign",
                    "timestamp": 1648890467928
                }
        add = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",add.json()["msg"])
        order_id = add.json()["data"]["id"]
        print("订单id:",order_id)
        #获取项目单id
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/getItemList"
        json = {
                    "data": {
                        "state": "",
                        "receiveId": order_id
                    },
                    "sign": "nosign",
                    "timestamp": 1649225963512
                }
        getItemList = requests.post(url,json=json,headers=headersvcd)
        getItemListid = getItemList.json()["data"][0]["id"]
        print("项目id：",getItemListid)
        #派工
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/arrangeMember"
        json = {
                    "data": {
                        "itemIdList": [getItemListid],
                        "memberIdList": [1421],
                        "type": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1649225972377
                }
        arrangeMember = requests.post(url,json=json,headers=headersvcd)
        #更新订单状态,订单状态变为已结算
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/updateState"
        json = {"data":{"id":order_id,"state":1,"totalMoney":"88"},"sign":"nosign","timestamp":1649210467326}
        updatestate = requests.post(url,json=json,headers=headersvcd)
        print("订单状态更新：",updatestate.json()["msg"])
        #使用现金支付
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/payByCash"
        json = {"data":{"id":order_id,"type":30},"sign":"nosign","timestamp":1649215179231}
        payByCash = requests.post(url,json=json,headers=headersvcd)
        print("使用现金支付：",payByCash.json()["msg"])
        #查询订单详情，断言订单状态
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/get"
        json = {"data":{"id":order_id},"sign":"nosign","timestamp":1648891209863}
        get = requests.post(url,json=json,headers=headersvcd)
        #断言订单状态为已结算
        self.assertEqual(2,get.json()["data"]["state"])
        #查看接车订单提成列表
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page2"
        json =  {
                    "data": {
                        "date": month,
                        "state": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1650526776765
                }
        page = requests.post(url,json=json,headers=headersvcd)
        receiveOrderId_1 = page.json()["data"]['records'][0]["receiveOrderId"]
        #作废接车订单提成
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/receiveUpdateState"
        json = {
                    "data": {
                        "receiveOrderIds": [receiveOrderId_1],
                        "state": 9
                    },
                    "sign": "nosign",
                    "timestamp": 1650529311564
                }
        receiveUpdateState = requests.post(url,json=json,headers=headersvcd)
        #查看接车订单提成列表
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page2"
        json =  {
                    "data": {
                        "date": month,
                        "state": 9
                    },
                    "sign": "nosign",
                    "timestamp": 1650526776765
                }
        page = requests.post(url,json=json,headers=headersvcd)
        receiveOrderId_2 = page.json()["data"]['records'][0]["receiveOrderId"]
        self.assertEqual(receiveOrderId_1,receiveOrderId_2)

    # def test_0_5(self):
    #     u'''员工绩效—绩效管理—接车订单提成—可确认且确认后到已确认列表'''
    #     #更新车辆信息的门店表，随机车牌
    #     month = datetime.datetime.now().strftime("%Y-%m")  #获取当前月份
    #     a = ''.join(random.sample(string.ascii_letters , 3))
    #     b = ''.join(random.sample(string.digits, 3))
    #     carNo = "粤"+a.upper()+b
    #     print("车牌号：",carNo)
    #     now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     #查询车牌id
    #     url = "https://test.chebufan.cn/vcd/api/open/receive/ycxReceive/getCarCondition"
    #     json = {
    #                 "data": {
    #                     "carNo": carNo
    #                 },
    #                 "sign": "nosign",
    #                 "timestamp": 1654753145527
    #             }
    #     resp = requests.post(url,json=json,headers=headersvcd)
    #     carId = resp.json()["data"]["ycxRepairCar"]["id"]
    #     print("车牌id：",carId)
    #     #接车开单
    #     false = False
    #     url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/add"
    #     json = {
    #                 "data": {
    #                     "carId": carId,
    #                     "brandIcon": "",
    #                     "brandName": "",
    #                     "modelName": "",
    #                     "carNo": carNo,
    #                     "carNoFlag": 1,
    #                     "mileage": "",
    #                     "carVin": "",
    #                     "czName": "",
    #                     "czPhone": "",
    #                     "violation": false,
    #                     "renewal": false,
    #                     "maintenance": false,
    #                     "annual": false,
    #                     "followThePublicAccount": false,
    #                     "existAccountCard": false,
    #                     "existComboCard": false,
    #                     "carDetectionNum": 0,
    #                     "carDetectionQuoteNum": 0,
    #                     "price": "88",
    #                     "award": 0,
    #                     "model": "",
    #                     "modelItem": "",
    #                     "kilometer": "",
    #                     "relPhone": "",
    #                     "sendMan": "",
    #                     "oil": "",
    #                     "remark": "",
    #                     "receiveTime": self.receiveTime,
    #                     "itemList": [{
    #                         "name": "洗车自动化",
    #                         "price": 88,
    #                         "type": "1",
    #                         "id": "1510164398556831745",
    #                         "num": 1,
    #                         "imgBool": false,
    #                         "award": 0,
    #                         "projectDistributionRule": [],
    #                         "key": "1510164398556831745",
    #                         "sellerId": "1297",
    #                         "projectId": "1510164398556831745"
    #                     }],
    #                     "pendingOrderId": ""
    #                 },
    #                 "sign": "nosign",
    #                 "timestamp": 1648890467928
    #             }
    #     add = requests.post(url,json=json,headers=headersvcd)
    #     self.assertEqual("成功",add.json()["msg"])
    #     order_id = add.json()["data"]["id"]
    #     print("订单id:",order_id)
    #     #获取项目单id
    #     url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/getItemList"
    #     json = {
    #                 "data": {
    #                     "state": "",
    #                     "receiveId": order_id
    #                 },
    #                 "sign": "nosign",
    #                 "timestamp": 1649225963512
    #             }
    #     getItemList = requests.post(url,json=json,headers=headersvcd)
    #     getItemListid = getItemList.json()["data"][0]["id"]
    #     print("项目id：",getItemListid)
    #     #派工
    #     url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/arrangeMember"
    #     json = {
    #                 "data": {
    #                     "itemIdList": [getItemListid],
    #                     "memberIdList": [1421],
    #                     "type": 0
    #                 },
    #                 "sign": "nosign",
    #                 "timestamp": 1649225972377
    #             }
    #     arrangeMember = requests.post(url,json=json,headers=headersvcd)
    #     #更新订单状态,订单状态变为已结算
    #     url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/updateState"
    #     json = {"data":{"id":order_id,"state":1,"totalMoney":"88"},"sign":"nosign","timestamp":1649210467326}
    #     updatestate = requests.post(url,json=json,headers=headersvcd)
    #     print("订单状态更新：",updatestate.json()["msg"])
    #     #使用现金支付
    #     url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/payByCash"
    #     json = {"data":{"id":order_id,"type":30},"sign":"nosign","timestamp":1649215179231}
    #     payByCash = requests.post(url,json=json,headers=headersvcd)
    #     print("使用现金支付：",payByCash.json()["msg"])
    #     #查询订单详情，断言订单状态
    #     url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/get"
    #     json = {"data":{"id":order_id},"sign":"nosign","timestamp":1648891209863}
    #     get = requests.post(url,json=json,headers=headersvcd)
    #     #断言订单状态为已结算
    #     self.assertEqual(2,get.json()["data"]["state"])
    #     #查看接车订单提成列表
    #     url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page2"
    #     json =  {
    #                 "data": {
    #                     "date": month,
    #                     "state": 0
    #                 },
    #                 "sign": "nosign",
    #                 "timestamp": 1650526776765
    #             }
    #     page = requests.post(url,json=json,headers=headersvcd)
    #     receiveOrderId_1 = page.json()["data"]['records'][0]["receiveOrderId"]
    #     #确认接车订单提成
    #     url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/receiveUpdateState"
    #     json = {
    #                 "data": {
    #                     "receiveOrderIds": [receiveOrderId_1],
    #                     "state": 1
    #                 },
    #                 "sign": "nosign",
    #                 "timestamp": 1650529311564
    #             }
    #     receiveUpdateState = requests.post(url,json=json,headers=headersvcd)
    #     #查看接车订单提成列表
    #     url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page2"
    #     json =  {
    #                 "data": {
    #                     "date": month,
    #                     "state": 1
    #                 },
    #                 "sign": "nosign",
    #                 "timestamp": 1650526776765
    #             }
    #     page = requests.post(url,json=json,headers=headersvcd)
    #     receiveOrderId_2 = page.json()["data"]['records'][0]["receiveOrderId"]
    #     self.assertEqual(receiveOrderId_1,receiveOrderId_2)

    def test_0_6(self):
        u'''员工绩效—绩效管理—接车订单提成—可发放提成且积分明细返回正确'''
        #更新车辆信息的门店表，随机车牌
        month = datetime.datetime.now().strftime("%Y-%m")  #获取当前月份
        a = ''.join(random.sample(string.ascii_letters , 3))
        b = ''.join(random.sample(string.digits, 3))
        carNo = "粤"+a.upper()+b
        print("车牌号：",carNo)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #查询车牌id
        url = "https://test.chebufan.cn/vcd/api/open/receive/ycxReceive/getCarCondition"
        json = {
                    "data": {
                        "carNo": carNo
                    },
                    "sign": "nosign",
                    "timestamp": 1654753145527
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        carId = resp.json()["data"]["ycxRepairCar"]["id"]
        print("车牌id：",carId)
        #接车开单
        false = False
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/add"
        json = {
                    "data": {
                        "carId": carId,
                        "brandIcon": "",
                        "brandName": "",
                        "modelName": "",
                        "carNo": carNo,
                        "carNoFlag": 1,
                        "mileage": "",
                        "carVin": "",
                        "czName": "",
                        "czPhone": "",
                        "violation": false,
                        "renewal": false,
                        "maintenance": false,
                        "annual": false,
                        "followThePublicAccount": false,
                        "existAccountCard": false,
                        "existComboCard": false,
                        "carDetectionNum": 0,
                        "carDetectionQuoteNum": 0,
                        "price": "88",
                        "award": 0,
                        "model": "",
                        "modelItem": "",
                        "kilometer": "",
                        "relPhone": "",
                        "sendMan": "",
                        "oil": "",
                        "remark": "",
                        "receiveTime": self.receiveTime,
                        "itemList": [{
                            "name": "洗车自动化",
                            "price": 88,
                            "type": "1",
                            "id": "1510164398556831745",
                            "num": 1,
                            "imgBool": false,
                            "award": 0,
                            "projectDistributionRule": [],
                            "key": "1510164398556831745",
                            "sellerId": "1297",
                            "projectId": "1510164398556831745"
                        }],
                        "pendingOrderId": ""
                    },
                    "sign": "nosign",
                    "timestamp": 1648890467928
                }
        add = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",add.json()["msg"])
        order_id = add.json()["data"]["id"]
        print("订单id:",order_id)
        #获取项目单id
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/getItemList"
        json = {
                    "data": {
                        "state": "",
                        "receiveId": order_id
                    },
                    "sign": "nosign",
                    "timestamp": 1649225963512
                }
        getItemList = requests.post(url,json=json,headers=headersvcd)
        getItemListid = getItemList.json()["data"][0]["id"]
        print("项目id：",getItemListid)
        #派工
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/arrangeMember"
        json = {
                    "data": {
                        "itemIdList": [getItemListid],
                        "memberIdList": [1421],
                        "type": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1649225972377
                }
        arrangeMember = requests.post(url,json=json,headers=headersvcd)
        #更新订单状态,订单状态变为已结算
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/updateState"
        json = {"data":{"id":order_id,"state":1,"totalMoney":"88"},"sign":"nosign","timestamp":1649210467326}
        updatestate = requests.post(url,json=json,headers=headersvcd)
        print("订单状态更新：",updatestate.json()["msg"])
        #使用现金支付
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/payByCash"
        json = {"data":{"id":order_id,"type":30},"sign":"nosign","timestamp":1649215179231}
        payByCash = requests.post(url,json=json,headers=headersvcd)
        print("使用现金支付：",payByCash.json()["msg"])
        #查询订单详情，断言订单状态
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/get"
        json = {"data":{"id":order_id},"sign":"nosign","timestamp":1648891209863}
        get = requests.post(url,json=json,headers=headersvcd)
        #断言订单状态为已结算
        self.assertEqual(2,get.json()["data"]["state"])
        #查看接车订单提成列表
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page2"
        json =  {
                    "data": {
                        "date": month,
                        "state": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1650526776765
                }
        page = requests.post(url,json=json,headers=headersvcd)
        receiveOrderId_1 = page.json()["data"]['records'][0]["receiveOrderId"]
        #确认接车订单提成
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/receiveUpdateState"
        json = {
                    "data": {
                        "receiveOrderIds": [receiveOrderId_1],
                        "state": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1650529311564
                }
        receiveUpdateState = requests.post(url,json=json,headers=headersvcd)
        #查看接车订单提成列表
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page2"
        json =  {
                    "data": {
                        "date": month,
                        "state": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1650526776765
                }
        page = requests.post(url,json=json,headers=headersvcd)
        receiveOrderId_2 = page.json()["data"]['records'][0]["receiveOrderId"]
        self.assertEqual(receiveOrderId_1,receiveOrderId_2)
        #发放提成
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/confirmAndPay"
        json = {
                "data": {
                    "receiveOrderId": [receiveOrderId_2],
                    "type": [1]
                },
                "sign": "nosign",
                "timestamp": 1650530527408
            }
        confirmAndPay = requests.post(url,json=json,headers=headersvcd)
        #查看接车订单已发放提成列表
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page2"
        json =  {
                    "data": {
                        "date": month,
                        "state": 3
                    },
                    "sign": "nosign",
                    "timestamp": 1650526776765
                }
        page = requests.post(url,json=json,headers=headersvcd)
        receiveOrderId_3 = page.json()["data"]['records'][0]["receiveOrderId"]
        self.assertEqual(receiveOrderId_2, receiveOrderId_3)

    def test_0_7(self):
        u'''我的绩效—接车开单—接车订单提成返回正确'''
        #更新车辆信息的门店表，随机车牌
        month = datetime.datetime.now().strftime("%Y-%m")  #获取当前月份
        a = ''.join(random.sample(string.ascii_letters , 3))
        b = ''.join(random.sample(string.digits, 3))
        carNo = "粤"+a.upper()+b
        print("车牌号：",carNo)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #查询车牌id
        url = "https://test.chebufan.cn/vcd/api/open/receive/ycxReceive/getCarCondition"
        json = {
                    "data": {
                        "carNo": carNo
                    },
                    "sign": "nosign",
                    "timestamp": 1654753145527
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        carId = resp.json()["data"]["ycxRepairCar"]["id"]
        print("车牌id：",carId)
        #接车开单
        false = False
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/add"
        json = {
                    "data": {
                        "carId": carId,
                        "brandIcon": "",
                        "brandName": "",
                        "modelName": "",
                        "carNo": carNo,
                        "carNoFlag": 1,
                        "mileage": "",
                        "carVin": "",
                        "czName": "",
                        "czPhone": "",
                        "violation": false,
                        "renewal": false,
                        "maintenance": false,
                        "annual": false,
                        "followThePublicAccount": false,
                        "existAccountCard": false,
                        "existComboCard": false,
                        "carDetectionNum": 0,
                        "carDetectionQuoteNum": 0,
                        "price": "88",
                        "award": 0,
                        "model": "",
                        "modelItem": "",
                        "kilometer": "",
                        "relPhone": "",
                        "sendMan": "",
                        "oil": "",
                        "remark": "",
                        "receiveTime": self.receiveTime,
                        "itemList": [{
                            "name": "洗车自动化",
                            "price": 88,
                            "type": "1",
                            "id": "1510164398556831745",
                            "num": 1,
                            "imgBool": false,
                            "award": 0,
                            "projectDistributionRule": [],
                            "key": "1510164398556831745",
                            "sellerId": "1297",
                            "projectId": "1510164398556831745"
                        }],
                        "pendingOrderId": ""
                    },
                    "sign": "nosign",
                    "timestamp": 1648890467928
                }
        add = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",add.json()["msg"])
        order_id = add.json()["data"]["id"]
        print("订单id:",order_id)
        #获取项目单id
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/getItemList"
        json = {
                    "data": {
                        "state": "",
                        "receiveId": order_id
                    },
                    "sign": "nosign",
                    "timestamp": 1649225963512
                }
        getItemList = requests.post(url,json=json,headers=headersvcd)
        getItemListid = getItemList.json()["data"][0]["id"]
        print("项目id：",getItemListid)
        #派工
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/arrangeMember"
        json = {
                    "data": {
                        "itemIdList": [getItemListid],
                        "memberIdList": [1421],
                        "type": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1649225972377
                }
        arrangeMember = requests.post(url,json=json,headers=headersvcd)
        #更新订单状态,订单状态变为已结算
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/updateState"
        json = {"data":{"id":order_id,"state":1,"totalMoney":"88"},"sign":"nosign","timestamp":1649210467326}
        updatestate = requests.post(url,json=json,headers=headersvcd)
        print("订单状态更新：",updatestate.json()["msg"])
        #使用现金支付
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/payByCash"
        json = {"data":{"id":order_id,"type":30},"sign":"nosign","timestamp":1649215179231}
        payByCash = requests.post(url,json=json,headers=headersvcd)
        print("使用现金支付：",payByCash.json()["msg"])
        #查询订单详情，断言订单状态
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/get"
        json = {"data":{"id":order_id},"sign":"nosign","timestamp":1648891209863}
        get = requests.post(url,json=json,headers=headersvcd)
        #断言订单状态为已结算
        self.assertEqual(2,get.json()["data"]["state"])
        #查看接车订单提成列表
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page2"
        json =  {
                    "data": {
                        "date": month,
                        "state": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1650526776765
                }
        page = requests.post(url,json=json,headers=headersvcd)
        receiveOrderId_1 = page.json()["data"]['records'][0]["receiveOrderId"]
        #确认接车订单提成
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/receiveUpdateState"
        json = {
                    "data": {
                        "receiveOrderIds": [receiveOrderId_1],
                        "state": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1650529311564
                }
        receiveUpdateState = requests.post(url,json=json,headers=headersvcd)
        #我的绩效待发放列表
        url ="https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/mine/page"
        json = {"data":{"current":1,"size":10,"params":{"timeType":"1","state":1},"total":1,"pages":1},"sign":"nosign","timestamp":1650534244336}
        page = requests.post(url,json=json,headers=headersvcd)
        #连接数据库断言数据
        conn = pymysql.connect(host="121.201.18.86", port=3325, user="root", passwd="Joysim!@#832727",db="cbf")  # 连接数据库
        cur = conn.cursor()  # 创建游标
        sql = "select * from tb_shop_employee_award where rel_id = %s"%(getItemListid)
        cur.execute(sql)
        obj = cur.fetchall()
        #断言确认发放条数
        self.assertEqual(2,len(obj))

    # def test_0_8(self):
    #     u'''
    #     我的绩效—营销活动—付费活动分销提成返回正确（涉及支付，无法测试）
    #     '''

    # def test_0_9(self):
    #     u'''
    #     我的绩效—营销活动—拼团活动分销提成返回正确（涉及支付，无法测试）
    #     '''
    def test_1_2(self):
        u'''我的绩效—会员卡—储值卡开卡或充值提成返回正确'''
        # 连接数据库断言数据
        conn = pymysql.connect(host="121.201.18.86", port=3325, user="root", passwd="Joysim!@#832727",db="cbf")  # 连接数据库
        cur = conn.cursor()  # 创建游标
        sql = "select * from tb_svip_order "
        cur.execute(sql)
        obj_1 = cur.fetchall()
        print("储值卡表订单数量：",len(obj_1))
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
        url_customerdetail = "https://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/customerDetail"
        json = {"data":{"phone":13538878368},"sign":"nosign","timestamp":1644287602993}
        customerdetail = requests.post(url_customerdetail,json=json,headers=headersvcd)
        self.assertIn("成功",customerdetail.json()["msg"])
        url_create = "https://test.chebufan.cn/vcd/api/open/svip/svipAccount/create"
        json = {
                    "data": {
                        "accountId": accountId,
                        "czPhone": 13538878368,
                        "amount": "10",
                        "otherAmount": "",
                        "payType": 3,
                        "salesperson": "1421",
                        "cardId": 1517406161222729730,
                        "licenseNoList": ["粤DGJ136"],
                        "receiveMoney": 1000
                    },
                    "sign": "nosign",
                    "timestamp": 1644289312404
                }
        create = requests.post(url_create,json=json,headers=headersvcd)
        self.assertIn("成功",create.json()["msg"])

        #进入会员卡提成列表
        month = datetime.datetime.now().strftime("%Y-%m")  #获取当前月份
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page"
        json = {
                    "data": {
                        "date": month,
                        "state": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1650523489211
                }
        list = requests.post(url,json=json,headers=headersvcd)
        id_1 = list.json()["data"]["records"][0]["id"]
        # #确认提成
        # url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/updateState"
        # json = {
        #             "data": {
        #                 "id": [id_1],
        #                 "state": 1
        #             },
        #             "sign": "nosign",
        #             "timestamp": 1650523918508
        #         }
        # updatestate = requests.post(url,json=json,headers=headersvcd)
        #查看确认列表
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page"
        json = {
                    "data": {
                        "date": month,
                        "state": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1650523489211
                }
        list = requests.post(url,json=json,headers=headersvcd)
        id_2 = list.json()["data"]["records"][0]["id"]
        print("储值卡提成列表id：",id_2)
        #发放提成
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/confirmAndPay"
        json = {
                    "data": {
                        "ids": [id_2],
                        "type": [1]
                    },
                    "sign": "nosign",
                    "timestamp": 1650524850924
                }
        confirmAndPay = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",confirmAndPay.json()["msg"])

        #退卡
        url_getShopVisitorDetail = 'https://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/getShopVisitorDetail'
        json = {
                    "data": {
                        "id": "1422796926413893634"
                    },
                    "sign": "nosign",
                    "timestamp": 1644974920444
                }
        getShopVisitorDetail = requests.post(url_getShopVisitorDetail,json=json,headers=headersvcd)
        # print(getShopVisitorDetail.text)
        vipCardDtoListid = getShopVisitorDetail.json()["data"]["vipCardDtoList"][0]["id"]
        print("用户储值卡id：",vipCardDtoListid)
        url_refund = "https://test.chebufan.cn/vcd/api/open/svip/svipAccount/refund"
        json = {
                    "data": {
                            "id": vipCardDtoListid
                    },
                    "sign": "nosign",
                    "timestamp": 1645002778922
                }
        refund = requests.post(url_refund,json=json,headers=headersvcd)
        self.assertIn("成功",refund.json()["msg"])

        # 连接数据库断言数据
        conn = pymysql.connect(host="121.201.18.86", port=3325, user="root", passwd="Joysim!@#832727",db="cbf")  # 连接数据库
        cur = conn.cursor()  # 创建游标
        sql = "select * from tb_svip_order "
        cur.execute(sql)
        obj_2 = cur.fetchall()
        print("储值卡表订单数量：",len(obj_2))
        # 断言确认发放条数
        self.assertEqual(len(obj_1)+1, len(obj_2))

    def test_1_3(self):
        u'''我的绩效—会员卡—套餐卡开卡提成返回正确'''
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
                        "salesperson": "1421",
                        "cardId": 1517030361206063106,
                        "ignoreRepeatedCreateTips": true,
                        "licenseNoList": ["粤DGEC11"],
                        # "receiveMoney": 96,
                    },
                    "sign": "nosign",
                    "timestamp": 1644304629295
                }
        create = requests.post(url_create,json=json,headers=headersvcd)
        self.assertIn("成功",create.json()["msg"])
        #进入会员卡提成列表
        month = datetime.datetime.now().strftime("%Y-%m")  #获取当前月份
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page"
        json = {
                    "data": {
                        "date": month,
                        "state": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1650523489211
                }
        list = requests.post(url,json=json,headers=headersvcd)
        id_1 = list.json()["data"]["records"][0]["id"]
        #确认提成
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/updateState"
        json = {
                    "data": {
                        "id": [id_1],
                        "state": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1650523918508
                }
        updatestate = requests.post(url,json=json,headers=headersvcd)
        #查看确认列表
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page"
        json = {
                    "data": {
                        "date": month,
                        "state": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1650523489211
                }
        list = requests.post(url,json=json,headers=headersvcd)
        id_2 = list.json()["data"]["records"][0]["id"]
        #发放提成
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/confirmAndPay"
        json = {
                    "data": {
                        "ids": [id_2],
                        "type": [1]
                    },
                    "sign": "nosign",
                    "timestamp": 1650524850924
                }
        confirmAndPay = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",confirmAndPay.json()["msg"])
        #查看提成完成列表
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page"
        json = {
                    "data": {
                        "date": month,
                        "state": 3
                    },
                    "sign": "nosign",
                    "timestamp": 1650523489211
                }
        list = requests.post(url,json=json,headers=headersvcd)
        id_2 = list.json()["data"]["records"][0]["id"]
        print("套餐卡订单列表id（tb_profit_order）：",id_2)
        self.assertEqual(id_1,id_2)
        #连接数据库断言数据
        conn = pymysql.connect(host="121.201.18.86", port=3325, user="root", passwd="Joysim!@#832727",db="cbf")  # 连接数据库
        cur = conn.cursor()  # 创建游标
        sql = "select rel_id from tb_shop_employee_award where id=%s"%(id_2)
        cur.execute(sql)
        obj = cur.fetchall()
        rel_id = obj[0][0]
        sql = "select * from tb_profit_order where id=%s"%(rel_id)
        cur.execute(sql)
        obj = cur.fetchall()
        #断言确认发放条数
        self.assertEqual(1,len(obj))

    def test_1_4(self):
        u'''员工绩效—绩效管理—员工提成统计—可查看员工提成统计并返回正确'''
        now = datetime.datetime.now().strftime("%Y-%m")
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/awardAnalyzeData"
        json = {
                        "data": {
                            "date": now
                        },
                        "sign": "nosign",
                        "timestamp": 1651048983408
                    }
        awardAnalyzeData = requests.post(url=url,json=json,headers=headersvcd)
        cardAward_1 = awardAnalyzeData.json()["data"][1]["records"][0]["cardAward"]
        print("当前%s-auto001会员卡提成金额:"%(now),cardAward_1)
        #调用会员卡提成
        self.test_1_3()
        awardAnalyzeData = requests.post(url=url,json=json,headers=headersvcd)
        cardAward_2 = awardAnalyzeData.json()["data"][1]["records"][0]["cardAward"]
        print("当前%s-auto001会员卡提成金额:"%(now),cardAward_2)
        self.assertEqual(float(cardAward_1+ 1),float(cardAward_2) )

    def test_1_5(self):
        u'''员工绩效—绩效管理—提成发放明细—可查看员工提成明细并返回正确'''
        now = datetime.datetime.now().strftime("%Y-%m")
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/awardPayOffRecords"
        json = {
                    "data": {
                        "type": 1,
                        "date": now,
                        "salesperson": 1421
                    },
                    "sign": "nosign",
                    "timestamp": 1651048986376
                }
        awardPayOffRecords = requests.post(url=url,json=json,headers=headersvcd)
        time = awardPayOffRecords.json()["data"][0]["time"]
        self.assertEqual(time.split(" ",1)[0][0:7],now)

    def test_1_6(self):
        u'''我的绩效—申请发放—员工申请发放，门店老板可收到通知，点击跳转员工绩效页（消息模板无法测试）'''
        #申请发送
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/mine/apply"
        json = {"data":{},"sign":"nosign","timestamp":1653466833915}
        resp = requests.post(url,json=json,headers=headersvcd)
        print(resp.text)
        try:
            self.assertEqual("成功", resp.json()["msg"])
        except AssertionError:
            self.assertEqual("您今天已经申请过了，请明天再申请", resp.json()["msg"])
        #确认是否已发送
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/mine/checkApply"
        json = {"data":{},"sign":"nosign","timestamp":1653466833915}
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",resp.json()["msg"])
    @classmethod

    def tearDownClass(cls):
        pass



if __name__ == "__main__":
    suite = unittest.TestSuite()
    unittest.main(verbosity=2)