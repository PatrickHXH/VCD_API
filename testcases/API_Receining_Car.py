# -*- encoding=utf8 -*-
__author__ = "HXH"
import random
import unittest
import requests
import datetime
import  string
import time
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
COMMON_DIR = os.path.join(BASE_DIR,"config")
sys.path.append(COMMON_DIR)
from common import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_cxgj,headers_admin_formdata,vpt_header

class Receining_Car(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global headersvcz
        headersvcz = headers_vcz(13538878368)

        self.receiveTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def test_0_2(self):
        u''''摄像头进店—可查看未开单和已开单车辆'''
        #随机车牌
        a = ''.join(random.sample(string.ascii_letters , 3))
        b = ''.join(random.sample(string.digits, 3))
        carNo = "粤"+a.upper()+b
        print("车牌号：", carNo)
        url = "http://test.chebufan.cn/chebftest/inter/lpr/testLPR?carNo=%s&sno=10088"%(carNo)
        camera = requests.get(url)
        time.sleep(3)
        #断言车辆列表是否有摄像头识别进店
        url = "https://test.chebufan.cn/vcd/api/open/car/lpr/list"
        json = {"data":{"current":1,"size":10,"params":{"dateSpan":0,"noSeeReceive":1},"total":1,"pages":0},"sign":"nosign","timestamp":1648870980227}
        list = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual(carNo,list.json()["data"]["records"][0]["licenseNo"])

    def test_0_3(self):
        u''''快捷开单—可添加配置项目'''
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/setCommonProjectList"
        json = {"data":[{"id":"1506818603686252545","num":1}],"sign":"nosign","timestamp":1648878539259}
        project = requests.post(url,json=json,headers=headersvcd)
        self.assertIn("成功",project.json()["msg"])
        #断言是否添加成功
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/getCommonProjectList"
        json = {"data":{},"sign":"nosign","timestamp":1648878539469}
        project = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("1506818603686252545",project.json()["data"][0]["id"])

    def test_0_4(self):
        u'''快捷开单—可快速开单'''
        #更新车辆信息的门店表
        #随机车牌
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
        #添加车辆
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
                    "relPhone": "",
                    "sendMan": "",
                    "model": "",
                    "kilometer": "",
                    "receiveTime": self.receiveTime,
                    "itemList": [{
                        "name": "精品",
                        "projectId": "1506818603686252545",
                        "num": 1
                    }],
                    "oil": "",
                    "remark": ""
                },
                "sign": "nosign",
                "timestamp": 1648882786123
            }
        add = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",add.json()["msg"])

    def test_0_5(self):
        u'''接车开单—选择项目—可新增或删除项目'''
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #新增项目
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/addProject"
        json = {"data":{"type":1,"name":"洗车自动化"+now,"price":"88"},"sign":"nosign","timestamp":1648885212709}
        addProject = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",addProject.json()["msg"])
        #断言项目是否新增
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/getProjectList"
        json = {"data":{"current":1,"size":100,"params":{"type":1,"name":""},"total":1,"pages":1},"sign":"nosign","timestamp":1648885213201}
        getprojectlist = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",getprojectlist.json()["msg"])

    # def test_0_6(self):
    #     u'''接车开单—选择项目—可添加项目并编辑（前端操作）'''

    def test_0_7(self):
        u'''接车开单—已开单'''
        #更新车辆信息的门店表,随机车牌
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
        #添加车辆
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
        print("订单id:", order_id)
        #查询订单详情
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/get"
        json = {"data":{"id":order_id},"sign":"nosign","timestamp":1648891209863}
        get = requests.post(url,json=json,headers=headersvcd)
        #断言订单状态为已开单
        self.assertEqual(0,get.json()["data"]["state"])

    def test_0_8(self):
        u''''接车开单—已开单—待结算'''
        #更新车辆信息的门店表
        #随机车牌
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
        #添加车辆
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
        #更新状态为待结算
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/updateState"
        json = {"data":{"id":order_id,"state":1,"totalMoney":"88"},"sign":"nosign","timestamp":1648892419655}
        update = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",update.json()["msg"])
        #查询订单详情
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/get"
        json = {"data":{"id":order_id},"sign":"nosign","timestamp":1648891209863}
        get = requests.post(url,json=json,headers=headersvcd)
        #断言订单状态为待结算
        self.assertEqual(1,get.json()["data"]["state"])

    # def test_0_9(self):
    #     u'''接车开单—已开单—待结算—已结算—可扫二维码支付，订单状态变为已结算（暂无法测试）'''


    def test_1__1(self):
        u'''接车开单—已开单—已结算—可使用会员卡支付，订单状态变为已结算'''
        #更新车辆信息的门店表
        #随机车牌
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
        #创建储值卡
        url = "https://test.chebufan.cn/vcd/api/open/svip/svipAccount/create"
        json = {
                    "data": {
                        "accountId": "1422796926413893634",
                        "czPhone": "13538878368",
                        "amount": "500",
                        "otherAmount": "50",
                        "payType": 3,
                        "salesperson": "",
                        "cardId": "1511513440830308353",
                        "licenseNoList": ["粤DGJ136"],
                    },
                    "sign": "nosign",
                    "timestamp": 1649210112661
                }
        createsvip = requests.post(url,json=json,headers=headersvcd)
        #绑定会员卡，获取会员卡信息
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/getSvipCardInfo"
        json = {"data":{"receiveOrderId":order_id,"czAccountId":"","czPhone":"13538878368"},"sign":"nosign","timestamp":1649209124504}
        bindsvip = requests.post(url,json=json,headers=headersvcd)
        svipid = bindsvip.json()["data"]["id"]
        #更新订单状态,订单状态变为待结算
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/updateState"
        json = {"data":{"id":order_id,"state":1,"totalMoney":"88"},"sign":"nosign","timestamp":1649210467326}
        updatestate = requests.post(url,json=json,headers=headersvcd)
        print("订单状态更新：",updatestate.json()["msg"])
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/payBySvipCard"
        json = {"data":{"id":order_id,"cardId":svipid,"amount":48.4},"sign":"nosign","timestamp":1649210467995}
        payBySvipCard = requests.post(url,json=json,headers=headersvcd)
        print("使用储值卡支付：",payBySvipCard.json()["msg"])
        #断言储值卡余额返回正确
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/getCardList"
        json = {"data":{"accountId":"1422796926413893634"},"sign":"nosign","timestamp":1649210990683}
        getCardList = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual(501.60,getCardList.json()["data"][0]["amount"])
        svipid = getCardList.json()["data"][0]["id"]
        #查询订单详情，断言订单状态
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/get"
        json = {"data":{"id":order_id},"sign":"nosign","timestamp":1648891209863}
        get = requests.post(url,json=json,headers=headersvcd)
        #断言订单状态为已结算
        self.assertEqual(2,get.json()["data"]["state"])
        #退卡
        url = "https://test.chebufan.cn/vcd/api/open/svip/svipAccount/refund"
        json = {"data":{"id":svipid},"sign":"nosign","timestamp":1649211627498}
        refund = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",refund.json()["msg"])

    def test_1__2(self):
        u'''接车开单—已开单—已结算—可使用现金支付，订单状态变为已结算'''
        #更新车辆信息的门店表
        #随机车牌
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

    def test_1__3(self):
        u'''接车开单—已开单—已结算—可使用其他支付，订单状态变为已结算'''
        #更新车辆信息的门店表
        #随机车牌
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
        #更新订单状态,订单状态变为已结算
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/updateState"
        json = {"data":{"id":order_id,"state":1,"totalMoney":"88"},"sign":"nosign","timestamp":1649210467326}
        updatestate = requests.post(url,json=json,headers=headersvcd)
        print("订单状态更新：",updatestate.json()["msg"])
        #使用其他支付
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/payByCash"
        json = {"data":{"id":order_id,"type":99},"sign":"nosign","timestamp":1649215179231}
        payByCash = requests.post(url,json=json,headers=headersvcd)
        print("使用其他支付：",payByCash.json()["msg"])
        #查询订单详情，断言订单状态
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/get"
        json = {"data":{"id":order_id},"sign":"nosign","timestamp":1648891209863}
        get = requests.post(url,json=json,headers=headersvcd)
        #断言订单状态为已结算
        self.assertEqual(2,get.json()["data"]["state"])

    def test_1_4(self):
        u'''接车开单—已开单—已取消'''
        #更新车辆信息的门店表
        #随机车牌
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
        #取消订单
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/cancel"
        json = {"data":{"id":order_id},"sign":"nosign","timestamp":1649216452702}
        cancel = requests.post(url,json=json,headers=headersvcd)
        print("订单取消：",cancel.json()["msg"])
        #查询订单详情，断言订单状态
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/get"
        json = {"data":{"id":order_id},"sign":"nosign","timestamp":1648891209863}
        get = requests.post(url,json=json,headers=headersvcd)
        #断言订单状态为已结算
        self.assertEqual(3,get.json()["data"]["state"])

    def test_1_5(self):
        u'''接车开单—已开单—修改订单—可修改订单'''
        #更新车辆信息的门店表，随机车牌
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
        #修改订单
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/updateProject"
        json = {
                    "data": {
                        "czPhone": "",
                        "czName": "",
                        "id": order_id,
                        "shopId": 1361,
                        "carNo": carNo,
                        "carVin": "",
                        "brandName": "",
                        "modelName": "",
                        "phone": "",
                        "oil": "",
                        "kilometer": "",
                        "remark": "",
                        "state": 0,
                        "totalMoney": 88,
                        "createUserId": 1297,
                        "createUserName": "黄管理2",
                        "itemList": [{
                            "id": "1510164398556831745",
                            "receiveId": order_id,
                            "projectId": "1510164398556831745",
                            "projectName": "洗车自动化",
                            "num": 2,
                            "price": 77,
                            "state": 1,
                            "sellerId": "1297",
                            "memberName": [],
                            "sellerAward": 0,
                            "memberAward": 0,
                            "imgList": [],
                            "createUserName": "黄管理2",
                            "award": 0,
                            "name": "洗车自动化"
                        }, {
                            "name": "保养",
                            "price": 40,
                            "type": "3",
                            "id": "1506818495301242881",
                            "num": 1,
                            "imgBool": false,
                            "award": 0,
                            "projectDistributionRule": [],
                            "key": "1506818495301242881",
                            "sellerId": "1297",
                            "projectId": "1506818495301242881"
                        }, {
                            "name": "健康",
                            "price": 50,
                            "type": "4",
                            "id": "1506818543594459138",
                            "num": 1,
                            "imgBool": false,
                            "award": 0,
                            "projectDistributionRule": [],
                            "key": "1506818543594459138",
                            "sellerId": "1297",
                            "projectId": "1506818543594459138"
                        }],
                        "imgList": [],
                        "createTime": now,
                        "updateTime": now,
                        "price": "178",
                        "award": 0,
                        "pendingOrderId": ""
                    },
                    "sign": "nosign",
                    "timestamp": 1649217646795
                }
        updateProject = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",updateProject.json()["msg"])
        #查询订单详情，断言订单状态
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/get"
        json = {"data":{"id":order_id},"sign":"nosign","timestamp":1648891209863}
        get = requests.post(url,json=json,headers=headersvcd)
        # print(get.text)
        #断言订单状态和项目金额
        self.assertEqual(0,get.json()["data"]["state"])
        self.assertEqual(str('154.00'),get.json()["data"]["itemList"][0]["totalMoney"])
        self.assertEqual(str('40.00'),get.json()["data"]["itemList"][1]["totalMoney"])
        self.assertEqual(str("50.00"),get.json()["data"]["itemList"][2]["totalMoney"])

    # def test_1_6(self):
    #     u'''接车开单—已开单—派工管理—可派工并收到消息模板通知'''

    def test_1_7(self):
        u'''接车开单—已开单—待结算/已结算—项目待派工变为无需派工状态，其他变为质检通过状态'''
        #更新车辆信息的门店表，随机车牌
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
                        "carId":carId,
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
                        "price": "158",
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
                        }, {
                            "name": "配件",
                            "price": 70,
                            "type": "6",
                            "id": "1506818647860662273",
                            "num": 1,
                            "imgBool": false,
                            "award": 0,
                            "projectDistributionRule": [],
                            "key": "1506818647860662273",
                            "sellerId": "1297",
                            "projectId": "1506818647860662273"
                        }],
                        "pendingOrderId": ""
                    },
                    "sign": "nosign",
                    "timestamp": 1649225900599
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
                        "memberIdList": [1297],
                        "type": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1649225972377
                }
        arrangeMember = requests.post(url,json=json,headers=headersvcd)
        #更新状态为待结算
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/updateState"
        json = {"data":{"id":order_id,"state":1,"totalMoney":"158"},"sign":"nosign","timestamp":1648892419655}
        update = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",update.json()["msg"])
        #查询订单详情
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/get"
        json = {"data":{"id":order_id},"sign":"nosign","timestamp":1648891209863}
        get = requests.post(url,json=json,headers=headersvcd)
        #断言项目施工单状态
        self.assertEqual(5,get.json()["data"]["itemList"][0]["state"])
        self.assertEqual(0,get.json()["data"]["itemList"][1]["state"])

    def test_1_8(self):
        u''' 施工单—待派工—待施工'''
        #更新车辆信息的门店表，随机车牌
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
                        "carId":carId,
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
                        "price": "158",
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
                        }, {
                            "name": "配件",
                            "price": 70,
                            "type": "6",
                            "id": "1506818647860662273",
                            "num": 1,
                            "imgBool": false,
                            "award": 0,
                            "projectDistributionRule": [],
                            "key": "1506818647860662273",
                            "sellerId": "1297",
                            "projectId": "1506818647860662273"
                        }],
                        "pendingOrderId": ""
                    },
                    "sign": "nosign",
                    "timestamp": 1649225900599
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
                        "memberIdList": [1297],
                        "type": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1649225972377
                }
        arrangeMember = requests.post(url,json=json,headers=headersvcd)
        #断言项目施工状态为待施工
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/getMyWorkingItemList"
        json = {"data":{"size":10,"current":1,"params":{"state":"2"}},"sign":"nosign","timestamp":1649235340677}
        getMyWorkingItemList = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual(carNo,getMyWorkingItemList.json()["data"]["records"][0]["licenseNo"])

    def test_1_9(self):
        u''' 施工单—待派工—待施工—施工中'''
        #更新车辆信息的门店表，随机车牌
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
                        "carId":carId,
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
                        "price": "158",
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
                        }, {
                            "name": "配件",
                            "price": 70,
                            "type": "6",
                            "id": "1506818647860662273",
                            "num": 1,
                            "imgBool": false,
                            "award": 0,
                            "projectDistributionRule": [],
                            "key": "1506818647860662273",
                            "sellerId": "1297",
                            "projectId": "1506818647860662273"
                        }],
                        "pendingOrderId": ""
                    },
                    "sign": "nosign",
                    "timestamp": 1649225900599
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
                        "memberIdList": [1297],
                        "type": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1649225972377
                }
        arrangeMember = requests.post(url,json=json,headers=headersvcd)
        #施工,上传图片
        url = "https://test.chebufan.cn/vcd/api/open/misc/attachment/upload"
        file_dir = os.path.abspath((os.path.dirname(os.path.dirname(__file__))))
        pic_dir = os.path.join(file_dir + "\\testdata\picture.jpg")
        files = {"file": open(pic_dir, "rb")}
        upload = requests.post(url, files=files)
        print("图片路径：",upload.json()["data"])
        #确认施工
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/itemWork"
        json = {
                    "data": {
                        "id": getItemListid,
                        "state": 3,
                        "imgList": [{
                            "imgUrl": upload.json()["data"],
                            "relId": getItemListid,
                            "relType": 2,
                            "type": 1
                        }]
                    },
                    "sign": "nosign",
                    "timestamp": 1649235133571
                }
        itemWork = requests.post(url,json=json,headers=headersvcd)
        #断言施工状态
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/getMyWorkingItemList"
        json = {"data":{"size":10,"current":1,"params":{"state":"3"}},"sign":"nosign","timestamp":1649235340677}
        getMyWorkingItemList = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual(carNo,getMyWorkingItemList.json()["data"]["records"][0]["licenseNo"])

    def test_2_1(self):
        u'''施工单—待派工—待施工—施工中—待质检'''
        #更新车辆信息的门店表，随机车牌
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
                        "carId":carId,
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
                        "price": "158",
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
                        }, {
                            "name": "配件",
                            "price": 70,
                            "type": "6",
                            "id": "1506818647860662273",
                            "num": 1,
                            "imgBool": false,
                            "award": 0,
                            "projectDistributionRule": [],
                            "key": "1506818647860662273",
                            "sellerId": "1297",
                            "projectId": "1506818647860662273"
                        }],
                        "pendingOrderId": ""
                    },
                    "sign": "nosign",
                    "timestamp": 1649225900599
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
                        "memberIdList": [1297],
                        "type": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1649225972377
                }
        arrangeMember = requests.post(url,json=json,headers=headersvcd)
        #施工,上传图片
        url = "https://test.chebufan.cn/vcd/api/open/misc/attachment/upload"
        file_dir = os.path.abspath((os.path.dirname(os.path.dirname(__file__))))
        pic_dir = os.path.join(file_dir + "\\testdata\picture.jpg")
        files = {"file": open(pic_dir, "rb")}
        upload = requests.post(url, files=files)
        print("图片路径：",upload.json()["data"])
        #确认施工
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/itemWork"
        json = {
                    "data": {
                        "id": getItemListid,
                        "state": 3,
                        "imgList": [{
                            "imgUrl": upload.json()["data"],
                            "relId": getItemListid,
                            "relType": 2,
                            "type": 1
                        }]
                    },
                    "sign": "nosign",
                    "timestamp": 1649235133571
                }
        itemWork = requests.post(url,json=json,headers=headersvcd)
        #确认完工
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/itemWork"
        json = {
                    "data": {
                        "id": getItemListid,
                        "state": 4,
                        "imgList": [{
                            "imgUrl": upload.json()["data"],
                            "relId": getItemListid,
                            "relType": 2,
                            "type": 1
                        }, {
                            "imgUrl": upload.json()["data"],
                            "relId": getItemListid,
                            "relType": 2,
                            "type": 2
                        }]
                    },
                    "sign": "nosign",
                    "timestamp": 1649236119216
                }
        itemWork =requests.post(url,json=json,headers=headersvcd)
        #断言施工状态
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/getMyWorkingItemList"
        json = {"data":{"size":10,"current":1,"params":{"state":"4"}},"sign":"nosign","timestamp":1649235340677}
        getMyWorkingItemList = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual(carNo,getMyWorkingItemList.json()["data"]["records"][0]["licenseNo"])

    def test_2_2(self):
        u'''施工单—待派工—待施工—施工中—待质检—质检通过'''
        true = True
        #更新车辆信息的门店表，随机车牌
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
                        "carId":carId,
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
                        "price": "158",
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
                        }, {
                            "name": "配件",
                            "price": 70,
                            "type": "6",
                            "id": "1506818647860662273",
                            "num": 1,
                            "imgBool": false,
                            "award": 0,
                            "projectDistributionRule": [],
                            "key": "1506818647860662273",
                            "sellerId": "1297",
                            "projectId": "1506818647860662273"
                        }],
                        "pendingOrderId": ""
                    },
                    "sign": "nosign",
                    "timestamp": 1649225900599
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
                        "memberIdList": [1297],
                        "type": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1649225972377
                }
        arrangeMember = requests.post(url,json=json,headers=headersvcd)
        #施工,上传图片
        url = "https://test.chebufan.cn/vcd/api/open/misc/attachment/upload"
        file_dir = os.path.abspath((os.path.dirname(os.path.dirname(__file__))))
        pic_dir = os.path.join(file_dir + "\\testdata\picture.jpg")
        files = {"file": open(pic_dir, "rb")}
        upload = requests.post(url, files=files)
        print("图片路径：",upload.json()["data"])
        #确认施工
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/itemWork"
        json = {
                    "data": {
                        "id": getItemListid,
                        "state": 3,
                        "imgList": [{
                            "imgUrl": upload.json()["data"],
                            "relId": getItemListid,
                            "relType": 2,
                            "type": 1
                        }]
                    },
                    "sign": "nosign",
                    "timestamp": 1649235133571
                }
        itemWork = requests.post(url,json=json,headers=headersvcd)
        #确认完工
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/itemWork"
        json = {
                    "data": {
                        "id": getItemListid,
                        "state": 4,
                        "imgList": [{
                            "imgUrl": upload.json()["data"],
                            "relId": getItemListid,
                            "relType": 2,
                            "type": 1
                        }, {
                            "imgUrl": upload.json()["data"],
                            "relId": getItemListid,
                            "relType": 2,
                            "type": 2
                        }]
                    },
                    "sign": "nosign",
                    "timestamp": 1649236119216
                }
        itemWork =requests.post(url,json=json,headers=headersvcd)
        #质检通过
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/inspect"
        json = {
                    "data": {
                        "id": getItemListid,
                        "result": true,
                        "remark": "备注"
                    },
                    "sign": "nosign",
                    "timestamp": 1649236716564
                }
        inspect = requests.post(url,json=json,headers=headersvcd)
        #断言施工状态
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/getMyWorkingItemList"
        json = {"data":{"size":10,"current":1,"params":{"state":"5"}},"sign":"nosign","timestamp":1649237044086}
        getMyWorkingItemList = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual(carNo,getMyWorkingItemList.json()["data"]["records"][0]["licenseNo"])

    def test_2_3(self):
        u''' 施工单—待派工—待施工—施工中—待质检—质检不通过—施工中'''
        #更新车辆信息的门店表，随机车牌
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
                        "carId":carId,
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
                        "price": "158",
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
                        }, {
                            "name": "配件",
                            "price": 70,
                            "type": "6",
                            "id": "1506818647860662273",
                            "num": 1,
                            "imgBool": false,
                            "award": 0,
                            "projectDistributionRule": [],
                            "key": "1506818647860662273",
                            "sellerId": "1297",
                            "projectId": "1506818647860662273"
                        }],
                        "pendingOrderId": ""
                    },
                    "sign": "nosign",
                    "timestamp": 1649225900599
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
                        "memberIdList": [1297],
                        "type": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1649225972377
                }
        arrangeMember = requests.post(url,json=json,headers=headersvcd)
        #施工,上传图片
        url = "https://test.chebufan.cn/vcd/api/open/misc/attachment/upload"
        file_dir = os.path.abspath((os.path.dirname(os.path.dirname(__file__))))
        pic_dir = os.path.join(file_dir + "\\testdata\picture.jpg")
        files = {"file": open(pic_dir, "rb")}
        upload = requests.post(url, files=files)
        print("图片路径：",upload.json()["data"])
        #确认施工
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/itemWork"
        json = {
                    "data": {
                        "id": getItemListid,
                        "state": 3,
                        "imgList": [{
                            "imgUrl": upload.json()["data"],
                            "relId": getItemListid,
                            "relType": 2,
                            "type": 1
                        }]
                    },
                    "sign": "nosign",
                    "timestamp": 1649235133571
                }
        itemWork = requests.post(url,json=json,headers=headersvcd)
        #确认完工
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/itemWork"
        json = {
                    "data": {
                        "id": getItemListid,
                        "state": 4,
                        "imgList": [{
                            "imgUrl": upload.json()["data"],
                            "relId": getItemListid,
                            "relType": 2,
                            "type": 1
                        }, {
                            "imgUrl": upload.json()["data"],
                            "relId": getItemListid,
                            "relType": 2,
                            "type": 2
                        }]
                    },
                    "sign": "nosign",
                    "timestamp": 1649236119216
                }
        itemWork =requests.post(url,json=json,headers=headersvcd)
        #质检不通过
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/inspect"
        json = {
                    "data": {
                        "id": getItemListid,
                        "result": false,
                        "remark": "备注"
                    },
                    "sign": "nosign",
                    "timestamp": 1649236716564
                }
        inspect = requests.post(url,json=json,headers=headersvcd)
        #断言施工状态
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrderItem/getMyWorkingItemList"
        json = {"data":{"size":10,"current":1,"params":{"state":"3"}},"sign":"nosign","timestamp":1649237044086}
        getMyWorkingItemList = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual(carNo,getMyWorkingItemList.json()["data"]["records"][0]["licenseNo"])



    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    # suite = unittest.TestSuite()
    # suite.addTest(Receining_Car("test_01"))
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(suite)
    time.sleep(3)
    unittest.main(verbosity=2)