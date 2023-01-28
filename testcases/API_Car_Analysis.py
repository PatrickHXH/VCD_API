# -*- encoding=utf8 -*-
__author__ = "HXH"

import random
import time
import unittest
import requests
import datetime
import  string
import time
import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
COMMON_DIR = os.path.join(BASE_DIR,"config")
sys.path.append(COMMON_DIR)
from common import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_cxgj,headers_admin_formdata,vpt_header

class Car_Analysis(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global  headersvcz
        headersvcz = headers_vcz(13538878368)


        self.dateEnd = datetime.datetime.now().strftime("%Y-%m-%d")
        self.dateBegin = (datetime.datetime.now()+datetime.timedelta(days=-7)).strftime("%Y-%m-%d")
        self.receiveTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def test_0_1(self):
        u''''进店分析—统计分析—进店统计分析统计正确'''
        #查看进店分析
        url_activeAnalyze = "http://test.chebufan.cn/vcd/api/open/shop/carTrack/enterStoreAnalysis"
        json = {"data":{},"sign":"nosign","timestamp":1631778240625}
        activeAnalyze = requests.post(url_activeAnalyze,json=json,headers=headersvcd)
        print(activeAnalyze.text)
        carbefore = activeAnalyze.json()["data"]["todayCarEnterNum"]


        #创建接车工单，更新车辆信息的门店表,随机车牌
        a = ''.join(random.sample(string.ascii_letters , 3))
        b = ''.join(random.sample(string.digits, 3))
        carNo = "粤"+a.upper()+b
        print("车牌号：",carNo)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #查询车牌id
        url = "http://test.chebufan.cn/vcd/api/open/receive/ycxReceive/getCarCondition"
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
        url = "http://test.chebufan.cn/vcd/api/open/receive/receiveOrder/add"
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

        #查看进店分析
        url_activeAnalyze = "http://test.chebufan.cn/vcd/api/open/shop/carTrack/enterStoreAnalysis"
        json = {"data":{},"sign":"nosign","timestamp":1631778240625}
        activeAnalyze = requests.post(url_activeAnalyze,json=json,headers=headersvcd)
        carafter = activeAnalyze.json()["data"]["todayCarEnterNum"]
        for  i in range(0,10):
            try:
                #断言进店车辆统计是否正确
                print("断言次数:",i)
                self.assertEqual(carbefore+1,carafter)
            except AssertionError:
                time.sleep(3)
                activeAnalyze = requests.post(url_activeAnalyze,json=json,headers=headersvcd)
                carafter = activeAnalyze.json()["data"]["todayCarEnterNum"]

    def test_0_2(self):
        u'''进店分析—统计分析—车辆列表—查看可报价和可年审车辆可跳转车辆列表'''
        #创建接车工单，更新车辆信息的门店表,随机车牌
        null = None
        a = ''.join(random.sample(string.ascii_letters , 3))
        b = ''.join(random.sample(string.digits, 3))
        carNo = "粤"+a.upper()+b
        print("车牌号：",carNo)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #查询车牌id
        url = "http://test.chebufan.cn/vcd/api/open/receive/ycxReceive/getCarCondition"
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
        url = "http://test.chebufan.cn/vcd/api/open/receive/receiveOrder/add"
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
        time.sleep(5)

        #查看进店车辆
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        url_cartrackpage = "http://test.chebufan.cn/vcd/api/open/car/es/search/list"
        json = {
                    "data": {
                        "current": 1,
                        "size": 10,
                        "pages": 0,
                        "queryParam": {
                            "dateBegin": "",
                            "dateEnd": "",
                            "annualVerifiable": null,
                            "quotable": null
                        },
                        "total": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1656658914427
                }
        cartrackpage = requests.post(url_cartrackpage,json=json,headers=headersvcd)
        # print(cartrackpage.text)
        for  i in range(0,10):
            try:
                self.assertIn(carNo,cartrackpage.json()["data"]["records"][0]["plateNumber"])
            except AssertionError:
                cartrackpage = requests.post(url_cartrackpage, json=json, headers=headersvcd)
                self.assertIn(carNo, cartrackpage.json()["data"]["records"][0]["plateNumber"])

    def test_0_3(self):
        u'''进店分析—统计分析—进店记录—可查看进店记录'''
        url = "http://test.chebufan.cn/vcd/api/open/shop/carTrack/enterStorePage"
        json ={
                    "data": {
                        "current": 1,
                        "size": 20,
                        "pages": 0,
                        "queryParam": {
                            "searchKeyword": "",
                            "beginTime": self.dateBegin,
                            "endTime": self.dateEnd
                        },
                        "total": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1657676652657
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        # print(resp.text)
        self.assertEqual("成功",resp.json()["msg"])

    def test_0_4(self):
        u'''进店车辆相关统计接口'''
        #查看进店车辆数
        url = "http://test.chebufan.cn/vcd/api/open/shop/carTrack/enterStoreNum"
        json ={
                    "data": {
                        "dateBegin": self.dateBegin,
                        "dateEnd":  self.dateEnd,
                        "dataVal": 7
                    },
                    "sign": "nosign",
                    "timestamp": 1656659502320
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        # print(resp.text)
        self.assertEqual("成功",resp.json()["msg"])

    def test_0_5(self):
        u'''查看进店车辆品牌'''
        url = "http://test.chebufan.cn/vcd/api/open/shop/carTrack/enterStoreBrand"
        json = {
                    "data": {
                        "dateBegin": self.dateBegin,
                        "dateEnd": self.dateEnd,
                        "dataVal": 7
                    },
                    "sign": "nosign",
                    "timestamp": 1656659502324
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",resp.json()["msg"])

    def test_0_6(self):
        u'''查看进店时段分布'''
        url = "http://test.chebufan.cn/vcd/api/open/shop/carTrack/enterStoreTime"
        json={
            "data": {
                "dateBegin": self.dateBegin,
                "dateEnd": self.dateEnd,
                "dataVal": 7
            },
            "sign": "nosign",
            "timestamp": 1656659502326
        }
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",resp.json()["msg"])

    def test_0_7(self):
        u'''查看车辆到店频次'''
        url = "http://test.chebufan.cn/vcd/api/open/shop/carTrack/enterStoreFrequency"
        json = {
                    "data": {
                        "dateBegin": self.dateBegin,
                        "dateEnd": self.dateEnd,
                        "dataVal": 90
                    },
                    "sign": "nosign",
                    "timestamp": 1656659502330
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",resp.json()["msg"])

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)