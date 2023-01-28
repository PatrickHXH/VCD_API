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


class Car_BusinessOpportunities(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global  headersvcz
        headersvcz = headers_vcz(13538878368)

        self.receiveTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    def test_0_1(self):
        u''''车辆商机—编辑—可编辑车辆详情'''
        #随机车牌
        a = ''.join(random.sample(string.ascii_letters , 3))
        b = ''.join(random.sample(string.digits, 3))
        carNo = "粤"+a.upper()+b
        print("车牌号：",carNo)
        #保存车牌到门店表，获取车辆ID
        url = "https://test.chebufan.cn/vcd/api/open/receive/ycxReceive/getCarCondition"
        json = {
                    "data": {
                        "carNo": carNo
                    },
                    "sign": "nosign",
                    "timestamp": 1652840003531
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        print(resp.text)
        carId = resp.json()["data"]["ycxRepairCar"]["id"]
        #编辑车辆
        url = "https://test.chebufan.cn/vcd/api/open/car/update"
        json = {
                    "data": {
                        "carNo": carNo,
                        "brandName": "阿斯顿·马丁",
                        "modelName": "优势V12(09/06-)",
                        "carVin": "1223",
                        "carEn": "44444",
                        "carRegDate": "2022-05-18",
                        "mileage": "8000",
                        "insuredCompanyName": "投保公司名称",
                        "vciTime": "2022-05-14",
                        "tciTime": "2022-05-14",
                        "czName": "测试-车主姓名",
                        "phone": "",
                        "sex": 1,
                        "brandIcon": "http://pic1.jisuapi.cn/car/static/images/logo/300/2.png",
                        "id": carId,
                        "carNoFlag": 1,
                        "repairId": 1361,
                        "czPhone": "15800190443"
                    },
                    "sign": "nosign",
                    "timestamp": 1652840793605
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",resp.json()["msg"])

    def test_0_2(self):
        u'''车辆商机—可补充车主信息、车险到期日和注册日期'''
        #随机车牌
        a = ''.join(random.sample(string.ascii_letters , 3))
        b = ''.join(random.sample(string.digits, 3))
        carNo = "粤"+a.upper()+b
        print("车牌号：",carNo)
        #保存车牌到门店表
        url = "https://test.chebufan.cn/vcd/api/open/receive/ycxReceive/getCarCondition"
        json = {
                    "data": {
                        "carNo": carNo
                    },
                    "sign": "nosign",
                    "timestamp": 1652840003531
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        #补充车主手机
        url = "https://test.chebufan.cn/vcd/api/open/car/business-opportunities/updateCzPhone"
        json = {
                "data": {
                    "carNo": carNo,
                    "phone": "17324233289",
                    "czName": "黄补充",
                    "sex": "1"
                },
                "sign": "nosign",
                "timestamp": 1652842461111
            }
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功", resp.json()["msg"])

    def test_0_3(self):
        u'''车辆商机—可查看订单记录'''
        #随机车牌
        a = ''.join(random.sample(string.ascii_letters , 3))
        b = ''.join(random.sample(string.digits, 3))
        carNo = "粤"+a.upper()+b
        print("车牌号：",carNo)
        #保存车牌到门店表
        url = "https://test.chebufan.cn/vcd/api/open/receive/ycxReceive/getCarCondition"
        json = {
                    "data": {
                        "carNo": carNo
                    },
                    "sign": "nosign",
                    "timestamp": 1652840003531
                }
        resp = requests.post(url, json=json, headers=headersvcd)
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/loadReceive"
        json = {"data":{"current":1,"size":10,"params":{"carNo":carNo,"states":["2","5"]},"total":1},"sign":"nosign","timestamp":1652844843633}
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功", resp.json()["msg"])

    def test_0_4(self):
        u'''车辆商机—可查看优惠卡券'''
        #查看优惠券
        url = "https://test.chebufan.cn/vcd/api/open/eticket/hcxEticket/page"
        json = {
                    "data": {
                        "current": 1,
                        "size": 10,
                        "params": {
                            "phone": "13538878368",
                            "state": []
                        },
                        "total": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1652845586245
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功", resp.json()["msg"])

    def test_0_5(self):
        u'''车辆商机—商机挖掘—车辆检测—可保存检测结果'''
        #上传图片
        url = "https://test.chebufan.cn/vcd/api/open/misc/attachment/upload"
        file_dir = os.path.abspath(os.path.dirname((os.path.dirname(__file__))))
        pic_dir = os.path.join(file_dir + "\\testdata\picture.jpg")
        f = open(pic_dir,"rb")
        files = {"file": f}
        upload = requests.post(url, files=files)
        pic_url = upload.json()["data"]
        print("图片路径：",upload.json()["data"])
        f.close()
        #随机车牌
        a = ''.join(random.sample(string.ascii_letters , 3))
        b = ''.join(random.sample(string.digits, 3))
        carNo = "粤"+a.upper()+b
        print("车牌号：",carNo)
        #保存车牌到门店表
        url = "https://test.chebufan.cn/vcd/api/open/receive/ycxReceive/getCarCondition"
        false = False
        json = {
                    "data": {
                        "carNo": carNo
                    },
                    "sign": "nosign",
                    "timestamp": 1652840003531
                }
        resp = requests.post(url, json=json, headers=headersvcd)
        #保存检测结果
        url = "https://test.chebufan.cn/vcd/api/open/carDetection/addCarDetection"
        json = {
                        "data": {
                            "licenseNo": carNo,
                            "itemList": [{
                                "projectCode": "1",
                                "projectName": "漆面",
                                "state": 0,
                                "czPhone": "135388783668",
                                "czName": "黄先生",
                                "price": "100",
                                "award": "5",
                                "adviceList": [{
                                    "name": "美容",
                                    "price": 80,
                                    "type": "1",
                                    "id": "1506818439986761730",
                                    "num": 1,
                                    "imgBool": false,
                                    "award": 5,
                                    "key": "1506818439986761730",
                                    "sellerId": "1488",
                                    "projectId": "1506818439986761730"
                                }],
                                "remark": "备注测试",
                                "imgList": [{
                                    "imgUrl": pic_url
                                }],
                                "categoryCode": "carDetectionCategoryType1"
                            }, {
                                "projectCode": "2",
                                "projectName": "室内",
                                "state": 1,
                                "categoryCode": "carDetectionCategoryType1"
                            }, {
                                "projectCode": "3",
                                "projectName": "方向盘",
                                "state": 1,
                                "categoryCode": "carDetectionCategoryType1"
                            }, {
                                "projectCode": "4",
                                "projectName": "座椅",
                                "state": 1,
                                "categoryCode": "carDetectionCategoryType1"
                            }, {
                                "projectCode": "1",
                                "projectName": "油品",
                                "state": 1,
                                "categoryCode": "carDetectionCategoryType2"
                            }, {
                                "projectCode": "2",
                                "projectName": "滤芯",
                                "state": 1,
                                "categoryCode": "carDetectionCategoryType2"
                            }]
                        },
                        "sign": "nosign",
                        "timestamp": 1652854411190
                    }
        resp = requests.post(url,json=json,headers=headersvcd)
        resultid = resp.json()["data"]
        self.assertEqual("成功", resp.json()["msg"])
        #获取检测结果详情
        url = "https://test.chebufan.cn/vcd/api/open/carDetection/getCarDetectionResult"
        json = {"data":{"id":resultid},"sign":"nosign","timestamp":1652858169345}
        resp = requests.post(url,json=json,headers=headersvcd)
        detectionId = resp.json()["data"]["detectionId"]
        projectDictId = resp.json()["data"]["detectionItemList"][0]["projectDictId"]
        detectionItemId = resp.json()["data"]["detectionItemList"][0]["detectionItemId"]
        #分享生成报价单
        url = "https://test.chebufan.cn/vcd/api/open/carDetection/generateQuoteOrder"
        json = {
                "data": {
                    "detectionId": detectionId,
                    "itemList": [{
                        "projectId": projectDictId,
                        "receiveProjectName": "美容",
                        "num": 1,
                        "price": 80,
                        "awardAmount": 5,
                        "detectionItemId": detectionItemId
                    }]
                },
                "sign": "nosign",
                "timestamp": 1652858180167
            }
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功", resp.json()["msg"])
        global QuoteOrderID
        QuoteOrderID = resp.json()["data"]

    def test_0_6(self):
        u'''车辆商机—商机挖掘—报价单—可同意报价，报价状态变为成功'''
        self.test_0_5()
        #同意报价
        url = "https://test.chebufan.cn/vcd/api/cz/receive/receiveOrder/agreeState"
        json = {"data":{"id":QuoteOrderID},"sign":"nosign","timestamp":1652859736922}
        resp = requests.post(url,json=json,headers=headersvcz)
        self.assertEqual(True, resp.json()["data"])

    def test_0_7(self):
        u'''车辆商机—商机挖掘—报价单—可取消报价，报价状态变为已取消'''
        self.test_0_5()
        #取消报价
        url = "https://test.chebufan.cn/vcd/api/open/carDetection/cancelQuote"
        json = {"data":{"id":QuoteOrderID},"sign":"nosign","timestamp":1652860908648}
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功", resp.json()["msg"])

    def test_0_8(self):
        u'''车辆商机—进行中的订单—可查看进行中和待结算的订单'''
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
        print("订单id:", order_id)
        #查看车辆商机
        url = "https://test.chebufan.cn/vcd/api/open/receive/receiveOrder/receiveOrder"
        json = {"data":{"carNo":carNo},"sign":"nosign","timestamp":1652863893183}
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual(order_id,resp.json()["data"][0]["orderId"])

    def test_0_9(self):
        u'''车辆商机—项目提醒—可设置提醒日期'''
        #当前时间
        now =datetime.datetime.now().strftime("%Y-%m-%d")
        #随机车牌
        a = ''.join(random.sample(string.ascii_letters , 3))
        b = ''.join(random.sample(string.digits, 3))
        carNo = "粤"+a.upper()+b
        print("车牌号：",carNo)
        #保存车牌到门店表，获取车辆ID
        url = "https://test.chebufan.cn/vcd/api/open/receive/ycxReceive/getCarCondition"
        json = {
                    "data": {
                        "carNo": carNo
                    },
                    "sign": "nosign",
                    "timestamp": 1652840003531
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        print(resp.text)
        carId = resp.json()["data"]["ycxRepairCar"]["id"]
        #设置日期
        url = "https://test.chebufan.cn/vcd/api/open/carRemind/addRemind"
        json = {"data":{"carId":carId,"licenseNo":carNo,"projectCode":"5","remindTime":now},"sign":"nosign","timestamp":1652864298088}
        resp = requests.post(url,json=json,headers=headersvcd)
        #到期提醒列表
        url = "https://test.chebufan.cn/vcd/api/open/carRemind/listRemindData"
        json = {"data":{"carId":carId},"sign":"nosign","timestamp":1652864298281}
        resp = requests.post(url, json=json, headers=headersvcd)
        self.assertEqual(now,resp.json()["data"][0]["remindTime"])
        global remindid
        remindid = resp.json()["data"][0]["id"]

    def test_1_1(self):
        u'''车辆商机—项目提醒—可添加保持跟进记录'''
        self.test_0_9()
        #创建提醒时间
        remindTime = (datetime.datetime.now()+datetime.timedelta(days=+7)).strftime("%Y-%m-%d")
        #添加跟进记录
        url = "https://test.chebufan.cn/vcd/api/open/carRemind/addRemindLog"
        json = {
                     "data": {
                        "remindId": remindid,
                        "followState": "1",
                        "followReason": "1",
                        "remark": "备注",
                        "remindTime": remindTime,
                        "timeType": "3"
                    },
                    "sign": "nosign",
                    "timestamp": 1652865100556
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",resp.json()["msg"])

    def test_1_2(self):
        u'''车辆商机—项目提醒—可添加成功跟进记录，上次跟进结果回显正确'''
        self.test_0_9()
        null =None
        #创建提醒时间
        remindTime = (datetime.datetime.now()+datetime.timedelta(days=+7)).strftime("%Y-%m-%d")
        #添加跟进记录,成功
        url = "https://test.chebufan.cn/vcd/api/open/carRemind/addRemindLog"
        json = {
                "data": {
                    "remindId": remindid,
                    "followState": "2",
                    "followReason": null,
                    "remark": "备注成功",
                    "remindTime": remindTime,
                    "timeType": null
                },
                "sign": "nosign",
                "timestamp": 1652865470189
            }
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",resp.json()["msg"])

    def test_1_3(self):
        u'''车辆商机—项目提醒—可添加失败跟进记录，上次跟进结果回显正确'''
        self.test_0_9()
        null =None
        #创建提醒时间
        remindTime = (datetime.datetime.now()+datetime.timedelta(days=+7)).strftime("%Y-%m-%d")
        #添加跟进记录,成功
        url = "https://test.chebufan.cn/vcd/api/open/carRemind/addRemindLog"
        json = {
                    "data": {
                        "remindId": remindid,
                        "followState": "3",
                        "followReason": "1,2",
                        "remark": "备注失败",
                        "remindTime": remindTime,
                        "timeType": null
                    },
                    "sign": "nosign",
                    "timestamp": 1652865621470
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",resp.json()["msg"])
    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)