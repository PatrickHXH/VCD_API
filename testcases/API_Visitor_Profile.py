# -*- encoding=utf8 -*-
__author__ = "HXH"

import datetime
import random
import unittest
import requests
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
COMMON_DIR = os.path.join(BASE_DIR,"config")
sys.path.append(COMMON_DIR)
from common import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_cxgj,headers_admin_formdata,vpt_header
import time

class Visitor_Profile(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global headersvcz
        headersvcz = headers_vcz(13538878368)

    def test_1_1(self):
        u'''访客档案—可查看用户浏览门店首页 / 活动 / 报价单记录'''
        #浏览首页增加记录
        import random
        randomnum = ''.join(random.sample("123456789",5))
        beginTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url = "https://test.chebufan.cn/vcd/api/cz/misc/flowLog/addFlowLog"
        json = {
                    "data": {
                        "bizId": "1361",
                        "shopId": "1361",
                        "bizType": 3,
                        "visitType": 1,
                        "systemType": 3,
                        "beginTime": beginTime
                    },
                    "sign": "nosign",
                    "timestamp": 1651115903539
                }
        addFlowLog = requests.post(url=url,json=json,headers=headersvcz)
        logid = addFlowLog.json()["data"]
        #更新浏览首页记录
        now = datetime.datetime.now()
        offset = datetime.timedelta(days=0.5)
        endTime = (now+offset).strftime("%Y-%m-%d %H:%M:%S")
        url = "https://test.chebufan.cn/vcd/api/cz/misc/flowLog/updateFlowLog"
        json = {
                    "data": {
                        "id": logid,
                        "endTime": endTime,
                        "stayTime": randomnum
                    },
                    "sign": "nosign",
                    "timestamp": 1651115920555
                }
        updateFlowLog = requests.post(url,json=json,headers=headersvcz)
        # print(updateFlowLog.text)

        #新增活动
        startTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        endTime = datetime.datetime.now()+datetime.timedelta(days=+30)
        time.sleep(5)
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
                        "validTimeUnit": 2,
                        "validTimeValue": 6,
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
        print(saveProfitSku.text)
        self.assertIn("成功",saveProfitSku.json()["msg"])
        global pay_id
        pay_id = saveProfitSku.json()["data"]["id"]
        print("付费活动id：",pay_id)
        #浏览活动增加记录
        beginTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url = "https://test.chebufan.cn/vcd/api/cz/misc/flowLog/addFlowLog"
        json = {
                    "data": {
                        "bizId": pay_id,
                        "shopId": "1361",
                        "bizType": 1,
                        "visitType": 1,
                        "systemType": 3,
                        "beginTime": beginTime
                    },
                    "sign": "nosign",
                    "timestamp": 1651130491983
                }
        addFlowLog = requests.post(url=url,json=json,headers=headersvcz)
        logid = addFlowLog.json()["data"]
        #更新浏览首页记录
        now = datetime.datetime.now()
        offset = datetime.timedelta(days=0.5)
        endTime = (now+offset).strftime("%Y-%m-%d %H:%M:%S")
        url = "https://test.chebufan.cn/vcd/api/cz/misc/flowLog/updateFlowLog"
        json = {
                    "data": {
                        "id": logid,
                        "endTime": endTime,
                        "stayTime": randomnum
                    },
                    "sign": "nosign",
                    "timestamp": 1651130494545
                }
        updateFlowLog = requests.post(url,json=json,headers=headersvcz)
        # print(updateFlowLog.text)

        #浏览报价单增加记录
        beginTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url = "https://test.chebufan.cn/vcd/api/cz/misc/flowLog/addFlowLog"
        json = {
                    "data": {
                        "bizId": "25652",
                        "shopId": "1361",
                        "bizType": 2,
                        "visitType": 1,
                        "systemType": 3,
                        "beginTime": beginTime
                    },
                    "sign": "nosign",
                    "timestamp": 1651132090871
                }
        addFlowLog = requests.post(url=url,json=json,headers=headersvcz)
        logid = addFlowLog.json()["data"]
        #更新浏览报价单记录
        now = datetime.datetime.now()
        offset = datetime.timedelta(days=0.5)
        endTime = (now+offset).strftime("%Y-%m-%d %H:%M:%S")
        url = "https://test.chebufan.cn/vcd/api/cz/misc/flowLog/updateFlowLog"
        json = {
                    "data": {
                        "id": logid,
                        "endTime": endTime,
                        "stayTime": randomnum
                    },
                    "sign": "nosign",
                    "timestamp": 1651130494545
                }
        updateFlowLog = requests.post(url,json=json,headers=headersvcz)

    def test_1_2(self):
        u'''访客档案—筛选—可根据授权 / 未授权 / 内容筛选'''
        url_flowAccountList = "http://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/flowAccountList"
        json = {"data":{"current":1,"size":10,"params":{"type":1},"total":1,"pages":0},"sign":"nosign","timestamp":1634798420205}
        flowAccountList = requests.post(url_flowAccountList,json=json,headers=headersvcd)
        self.assertIn("成功",flowAccountList.json()["msg"])

        url_flowAccountList = "http://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/flowAccountList"
        json = {"data":{"current":1,"size":10,"params":{"type":2},"total":1,"pages":0},"sign":"nosign","timestamp":1634798420205}
        flowAccountList = requests.post(url_flowAccountList,json=json,headers=headersvcd)
        self.assertIn("成功",flowAccountList.json()["msg"])

        url_flowBizList = "http://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/flowBizList"
        json = {"data":{"current":1,"size":10,"params":{"type":3},"total":1,"pages":0},"sign":"nosign","timestamp":1634798422670}
        flowBizList = requests.post(url_flowBizList,json=json,headers=headersvcd)
        self.assertIn("成功",flowBizList.json()["msg"])
        global  id
        id = flowBizList.json()["data"]["records"][0]["bizId"]

    def test_1_3(self):
        u'''访客档案—搜索—点击可跳转客户档案'''
        url_getAccountProfileList = "http://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/getAccountProfileList"
        json = {"data":{"searchText":""},"sign":"nosign","timestamp":1634799704518}
        getAccountProfileList = requests.post(url_getAccountProfileList,json=json,headers=headersvcd)
        self.assertIn("成功",getAccountProfileList.json()["msg"])

    def test_1_4(self):
        u'''访客档案—按内容—详情—点击可跳转内容详情'''
        url_flowBizAccountRecord = "http://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/flowBizAccountRecord"
        json = {"data":{"current":1,"size":10,"params":{"bizId":id},"total":1},"sign":"nosign","timestamp":1634800387263}
        flowBizAccountRecord = requests.post(url_flowBizAccountRecord,json=json,headers=headersvcd)
        self.assertIn("成功",flowBizAccountRecord.json()["msg"])
        global  account_id
        account_id = flowBizAccountRecord.json()["data"]["records"][0]["accountId"]

    def test_1_5(self):
        u'''访客档案—按内容—用户—点击可跳转访客详情'''
        url_getShopVisitorDetail = "http://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/getShopVisitorDetail"
        json = {"data":{"id":"1422796926413893634"},"sign":"nosign","timestamp":1634800863672}
        getShopVisitorDetail = requests.post(url_getShopVisitorDetail,json=json,headers=headersvcd)
        self.assertIn("成功",getShopVisitorDetail.json()["msg"])

    def test_1_6(self):
        u'''访客档案—客户档案—搜索—可搜索用户'''
        url_getAccountProfileList = "http://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/getAccountProfileList"
        json = {"data":{"searchText":"ui_test"},"sign":"nosign","timestamp":1634869503306}
        getAccountProfileList = requests.post(url_getAccountProfileList,json=json,headers=headersvcd)
        self.assertIn("ui_test", getAccountProfileList.json()["data"][0]["nickName"])

    # def test_1_7(self):
    #     u'''访客档案—客户档案—用户—点击可跳转访客详情'''

    def test_1_8(self):
        u'''访客档案—访客详情—编辑—可编辑用户名称和备注'''
        url_updateRemark = "http://test.chebufan.cn/vcd/api/open/czuser/czAccountShopRel/updateRemark"
        json = {"data":{"czAccountId":CzAccountId(13538878368),"remarks":"备注test","name":"HXH"},"sign":"nosign","timestamp":1634871545847}
        updateRemark = requests.post(url_updateRemark,json=json,headers=headersvcd)
        self.assertIn("成功",updateRemark.json()["msg"])

    # def test_1_9(self):
    #     u'''访客档案—访客详情—客户画像—车牌—可跳转车辆商机'''

    def test_2_1(self):
        u'''访客档案—访客详情—商机线索—可查看用户停留时间'''
        url_getShopVisitorRecord = "http://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/getShopVisitorRecord"
        json = {"data":{"current":1,"size":10,"params":{"accountId":CzAccountId(13538878368)},"total":1},"sign":"nosign","timestamp":1634872612005}
        getShopVisitorRecord = requests.post(url_getShopVisitorRecord,json=json,headers=headersvcd)
        self.assertIn("成功",getShopVisitorRecord.json()["msg"])

    @classmethod
    def tearDownClass(cls):
        pass



if __name__ == "__main__":
    suite = unittest.TestSuite()
    unittest.main(verbosity=2)