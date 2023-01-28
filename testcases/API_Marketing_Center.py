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
from XTestRunner import label
from CLOSE_PROFIT_SKU import closeprofit

class Marketing_Center(unittest.TestCase):
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

    def test_1_1(self):
        u'''营销中心—店铺商城—店铺商城营销统计返回正确'''
        url = "https://test.chebufan.cn/vcd/api/open/profit/sku/statistic"
        json = {
                "data": {
                    "startTime": str(startTime),
                    "endTime": str(endTime)
                },
                "sign": "nosign",
                "timestamp": 1658478973396
            }
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",resp.json()["msg"])

    # @label("slow")
    # def test_1_2(self):
    #     u'''营销中心—发布活动—咨询客服—可弹出咨询客服弹窗'''

    def test_1_3(self):
        u'''营销中心—发布活动—拼团活动—可发布拼团活动'''
        time.sleep(3)
        url_saveProfitSku = "http://test.chebufan.cn/vcd/api/open/profit/sku/saveProfitSku"
        json = {
                    "data":{
                        "name":"拼团自动化"+startTime,
                        "salePrice":10000,
                        "stock":"8888",
                        "shouldPay":1,
                        "startTime":str(startTime),
                        "endTime":str(endTime),
                        "limitTimes":3,
                        "validTimeValue": 5,
		                "validTimeUnit": 2,
                        "profitTicketSkuQueryList":[
                            {
                                "name":"拼团自动化",
                                "num":2,
                                "originalPrice":6600,
                                "remindFlag": 0
                            }
                        ],
                        "profitSkuImageList":[
                            {
                                "imageUrl":"https://test.chebufan.cn/vcdfile/modelName/8/e4abc2b8f1b444609972f289d870c789.webp",
                                "sortNo":1,
                                "imageType":1
                            },
                            {
                                "imageUrl":"https://test.chebufan.cn/vcdfile/modelName/8/21123dba375845b5bbd0b0c70455cebd.webp",
                                "sortNo":2,
                                "imageType":2
                            }
                        ],
                        "type":3,
                        "onePurchaser":1,
                        "onlyNewPurchaser":0,
                        "groupPrice":5000,
                        "groupCapacity":2,
                        "supplyPrice":13200,
                        "description":"仅限七座以下非营运车辆可参与,不可与店内其他优惠同时使用"
                    },
                    "sign":"nosign",
                    "timestamp":1632994043189
                }
        saveProfitSku = requests.post(url_saveProfitSku,json=json,headers=headersvcd)
        self.assertIn("成功",saveProfitSku.json()["msg"])
        global group_id
        group_id = saveProfitSku.json()["data"]["id"]
        print("拼团活动id：",group_id)

    def test_1_4(self):
        u'''营销中心—发布活动—付费活动—可发布付费活动'''
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

    def test_1_5(self):
        u'''营销中心—发布活动—抵扣活动—可发布抵扣券活动'''
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

    def test_1_6(self):
        u'''营销中心—活动详情—可查看活动详情'''
        self.test_1_3()
        self.test_1_4()
        self.test_1_5()
        #可查看付费活动详情
        url_profitData = "http://test.chebufan.cn/vcd/api/open/profit/sku/profitData"
        json = {"data":{"id":pay_id},"sign":"nosign","timestamp":1634526456854}
        profitData = requests.post(url_profitData,json=json,headers=headersvcd)
        self.assertEqual(2,profitData.json()['data']['type'])

        #可查看拼团详情
        url_profitData = "http://test.chebufan.cn/vcd/api/open/profit/sku/profitData"
        json = {"data":{"id":group_id},"sign":"nosign","timestamp":1634526456854}
        profitData = requests.post(url_profitData,json=json,headers=headersvcd)
        self.assertEqual(3,profitData.json()['data']['type'])

        #可查看抵扣券详情
        url = "https://test.chebufan.cn/vcd/api/open/profit/sku/profitData"
        json = {"data":{"id":coupon_id},"sign":"nosign","timestamp":1634526456854}
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual(5, resp.json()['data']['type'])

    def test_1_7(self):
        u'''营销中心—活动详情—效果明细—可跳转明细页'''
        self.test_1_4()
        #按人展示，按时间展示
        url = "https://test.chebufan.cn/vcd/api/open/profit/sku/getProfitLogPage"
        for i in range(1,3):
            json = {
                        "data": {
                            "current": 1,
                            "size": 10,
                            "params": {
                                "logType": "1",
                                "profitId": coupon_id,
                                "queryType": i
                            },
                            "total": 1,
                            "pages": 0
                        },
                        "sign": "nosign",
                        "timestamp": 1658388907798
                    }
            resp = requests.post(url,json=json,headers=headersvcd)
            self.assertEqual("成功",resp.json()["msg"])
        # 领取，新绑定
        for i in range(2,4):
            json = {
                        "data": {
                            "current": 1,
                            "size": 10,
                            "params": {
                                "logType": str(i),
                                "profitId": coupon_id,
                                "queryType": ""
                            },
                            "total": 1,
                            "pages": 0
                        },
                        "sign": "nosign",
                        "timestamp": 1658388913965
                    }
            resp = requests.post(url,json=json,headers=headersvcd)
            self.assertEqual("成功",resp.json()["msg"])
        #团列表
        url = "https://test.chebufan.cn/vcd/api/open/profit/sku/getProfitGroupLogPage"
        json = {
                    "data": {
                        "current": 1,
                        "size": 10,
                        "params": {
                            "logType": "4",
                            "profitId": coupon_id,
                            "queryType": ""
                        },
                        "total": 1,
                        "pages": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1658388910840
                }
        self.assertEqual("成功", resp.json()["msg"])

    def test_1_8(self):
        u'''营销中心—活动追踪—可筛选全部/未开始/进心中活动'''
        #进心中、未开始活动统计接口
        url = "https://test.chebufan.cn/vcd/api/open/profit/sku/getAllProfitNumByState"
        json = {"data":{},"sign":"nosign","timestamp":1658393534581}
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",resp.json()["msg"])
        #进行中、未开始、全部活动列表
        for i in range(0,3):
            if i ==0:
                var = 1
            if i ==1:
                var = -1
            if i ==2:
                var =""
            url = "https://test.chebufan.cn/vcd/api/open/profit/sku/profitSkuList"
            json = {"data":{"current":1,"size":10,"params":{"state":var},"total":1,"pages":8},"sign":"nosign","timestamp":1658393805493}
            resp = requests.post(url,json=json,headers=headersvcd)

    def test_1_9(self):
        u'''营销中心—活动详情—曝光—可开关活动且v车主可查看'''
        self.test_1_4()
        #关闭小程序首页曝光
        url_updateProfitSkuStall = "http://test.chebufan.cn/vcd/api/open/profit/sku/updateProfitSkuStall"
        json = {"data":{"skuId":pay_id,"stall":3,"state":0},"sign":"nosign","timestamp":1634697550119}
        updateProfitSkuStall = requests.post(url_updateProfitSkuStall,json=json,headers=headersvcd)
        self.assertIn("成功",updateProfitSkuStall.json()["msg"])


        #开启小程序首页弹窗曝光
        url_updateProfitSkuStall = "https://test.chebufan.cn/vcd/api/open/profit/sku/updateProfitSkuStall"
        json = {"data":{"skuId":pay_id,"stall":2,"state":1},"sign":"nosign","timestamp":1634697550119}
        updateProfitSkuStall = requests.post(url_updateProfitSkuStall,json=json,headers=headersvcd)
        self.assertIn("成功",updateProfitSkuStall.json()["msg"])
        #关闭小程序首页弹窗曝光
        url_updateProfitSkuStall = "http://test.chebufan.cn/vcd/api/open/profit/sku/updateProfitSkuStall"
        json = {"data":{"skuId":pay_id,"stall":2,"state":0},"sign":"nosign","timestamp":1634697550119}
        updateProfitSkuStall = requests.post(url_updateProfitSkuStall,json=json,headers=headersvcd)
        self.assertIn("成功",updateProfitSkuStall.json()["msg"])

        #开启小程序报价详情曝光
        url_updateProfitSkuStall = "https://test.chebufan.cn/vcd/api/open/profit/sku/updateProfitSkuStall"
        json = {"data":{"skuId":pay_id,"stall":1,"state":1},"sign":"nosign","timestamp":1634697550119}
        updateProfitSkuStall = requests.post(url_updateProfitSkuStall,json=json,headers=headersvcd)
        self.assertIn("成功",updateProfitSkuStall.json()["msg"])
        #关闭小程序报价详情曝光
        url_updateProfitSkuStall = "http://test.chebufan.cn/vcd/api/open/profit/sku/updateProfitSkuStall"
        json = {"data":{"skuId":pay_id,"stall":1,"state":0},"sign":"nosign","timestamp":1634697550119}
        updateProfitSkuStall = requests.post(url_updateProfitSkuStall,json=json,headers=headersvcd)
        self.assertIn("成功",updateProfitSkuStall.json()["msg"])

        #开启抵扣券
        self.test_1_5()
        url = "https://test.chebufan.cn/vcd/api/cz/profit/profitSku/listCouponByStall"
        json = {"data":{"shopId":"1361","stall":3},"sign":"nosign","timestamp":1658391002935}
        resp = requests.post(url,json=json,headers=headersvcz)
        self.assertIn(coupon_id,resp.json()["data"][0]["id"])
        #关闭抵扣券活动
        url = "https://test.chebufan.cn/vcd/api/open/profit/sku/updateProfitSkuStall"
        json = {"data":{"skuId":coupon_id,"stall":3,"state":0},"sign":"nosign","timestamp":1658391692436}
        resp = requests.post(url, json=json, headers=headersvcd)
        # 查看车主曝光接口是否有返回
        url = "https://test.chebufan.cn/vcd/api/cz/profit/profitSku/listCouponByStall"
        json = {"data":{"shopId":"1361","stall":3},"sign":"nosign","timestamp":1658391002935}
        resp = requests.post(url,json=json,headers=headersvcz)
        data_list = resp.json()['data']
        for i in data_list:
            self.assertNotEqual(coupon_id,i["id"])

    def test_2_1(self):
        u'''营销中心—活动详情—开关活动—可开关活动'''
        self.test_1_3()
        for i in range(0,2):
            if  i == 0:
                var = 1
            if i == 1:
                var = 0
            url = "https://test.chebufan.cn/vcd/api/open/profit/sku/updateProfitSkuState"
            json = {
                    "data": {
                        "id": group_id,
                        "state": var
                    },
                    "sign": "nosign",
                    "timestamp": 1658394668253
                }
            resp = requests.post(url,json=json,headers=headersvcd)
            self.assertEqual("成功",resp.json()["msg"])

    def test_2_2(self):
        u'''营销中心—活动详情—面对面分享—可识别小程序二维码且跳转正确（测试生成二维码，无法测跳转）'''
        self.test_1_4()
        #生成小程序二维码
        url_getWxAcodeUnlimit = "http://test.chebufan.cn/vcd/api/open/wx/miniapp/getWxAcodeUnlimit"
        json = {"data":{"page":"pages_coupon/couponGet/index","scene":"t=1&id=%s"%(pay_id),"miniFlag":1},"sign":"nosign","timestamp":1634701081700}
        getWxAcodeUnlimit = requests.post(url_getWxAcodeUnlimit,json=json,headers=headersvcd)
        self.assertIn("成功",getWxAcodeUnlimit.json()["msg"])

    # @label("slow")
    # def test_2_3(self):
    #     u'''营销中心—活动详情—微信分享—拼团/优惠购券/抵扣券可分享活动且跳转正确'''

    def test_2_4(self):
        u'''营销中心—活动详情—微信分享—拼团/优惠购券/抵扣券可生成朋友圈海报且识别跳转正确（测试生成二维码，无法测跳转）'''
        #生成拼团海报
        self.test_1_3()
        url = "https://test.chebufan.cn/vcd/api/open/wx/miniapp/getWxAcodeUnlimit"
        json = {"data":{"page":"pages_coupon/couponGet/index","scene":"t=1&id=%s&accountId=1297"%(group_id),"miniFlag":1},"sign":"nosign","timestamp":1652774303742}
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",resp.json()["msg"])

    def test_2_5(self):
        u'''营销中心—活动详情—更多操作—可编辑活动'''
        self.test_1_3()
        #编辑拼团活动
        url_updateProfitSku = "http://test.chebufan.cn/vcd/api/open/profit/sku/updateProfitSku"
        json ={
                    "data":{
                        "id":group_id,
                        "createTime":startTime,
                        "updateTime":startTime,
                        "deleted":0,
                        "state":1,
                        "shopId":"1361",
                        "accountId":"1287",
                        "name":"拼团自动化"+startTime,
                        "description":"仅限七座以下非营运车辆可参与,不可与店内其他优惠同时使用,特惠活动购买不退换不折现",
                        "imageUrl":"https://test.chebufan.cn/vcdfile/modelName/8/153d1952c1e948529f7324756b4e3b14.webp",
                        "stock":8888,
                        "remain":8888,
                        "salePrice":1,
                        "supplyPrice":17600,
                        "shouldPay":1,
                        "startTime":str(startTime),
                        "endTime":str(endTime),
                        "limitTimes":50,
                        "validTimeValue": 6,
                        "validTimeUnit": 3,
                        "hideStock":0,
                        "type":2,
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
                        "tickets":[
                            {
                                "name":"拼团自动化"+startTime,
                                "count":2,
                                "originalPrice":88,
                                "validMonths":12,
                                "num":2
                            }
                        ],
                        "groupPrice":"",
                        "profitTicketSkuQueryList":[
                            {
                                "name":"拼团自动化"+startTime,
                                "count":2,
                                "originalPrice":88,
                                "validMonths":12,
                                "num":2
                            }
                        ]
                    },
                    "sign":"nosign",
                    "timestamp":1634713275950
                }
        updateProfitSku = requests.post(url_updateProfitSku,json=json,headers=headersvcd)
        self.assertIn("成功",updateProfitSku.json()["msg"])

    # @label("slow")
    # def test_2_6(self):
    #     pass

    # @label("slow")
    # def test_2_7(self):
    #     u'''营销中心—活动详情—营销短信—可收到营销短信并跳转车主活动详情'''
    #     pass

    def test_2_8(self):
        u'''营销中心—订单管理—活动订单—可查看待支付/待成团/已完成/已取消订单'''
        for i in range(0,5):
            if i == 4:
                var = ""
            else:
                var = i
            url = "http://test.chebufan.cn/vcd/api/open/profit/order/list"
            json = {
                        "data": {
                            "current": 1,
                            "size": 10,
                            "pages": 0,
                            "params": {
                                "state": var,
                                "startTime": str(startTime),
                                "endTime": str(endTime)
                            },
                            "total": 1
                        },
                        "sign": "nosign",
                        "timestamp": 1658473893674
                    }
            resp = requests.post(url,json=json,headers=headersvcd)
            self.assertEqual("成功",resp.json()["msg"])

    def test_2_9(self):
        u'''营销中心—订单管理—开团记录—可查看待成团/已成团/拼团失败订单'''
        for i in range(0,5):
            if i == 4:
                var = ""
            else:
                var = i
            url = "https://test.chebufan.cn/vcd/api/open/profit/order/teamList"
            json = {
                        "data": {
                            "current": 1,
                            "size": 10,
                            "pages": 0,
                            "params": {
                                "state": var,
                                "startTime": str(startTime),
                                "endTime": str(endTime)
                            },
                            "total": 1
                        },
                        "sign": "nosign",
                        "timestamp": 1658473893674
                    }
            resp = requests.post(url,json=json,headers=headersvcd)
            self.assertEqual("成功",resp.json()["msg"])

    def test_3_1(self):
        u'''营销中心—订单管理—拼团中订单可退款（0元退款，微信支付退款暂不可测试）'''
        #创建拼团活动
        self.test_1_3()
        #创建抵扣券
        self.test_1_5()
        #领取抵扣券
        url = "https://test.chebufan.cn/vcd/api/cz/profit/profitSku/takeCoupon"
        json = {"data":{"id":coupon_id},"sign":"nosign","timestamp":1658474704566}
        resp = requests.post(url,json=json,headers=headersvcz)
        print(resp.text)
        #获取抵扣券id
        url = "https://test.chebufan.cn/vcd/api/cz/profit/profitSku/pageCoupon"
        json = {
                    "data": {
                        "current": 1,
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
            if i["couponValue"] == 8800:
                ticketid = i["id"]
                continue
        print("抵扣券id：",ticketid)
        #使用抵扣券
        url = "https://test.chebufan.cn/vcd/api/cz/profit/profitGroupTeam/create"
        json = {"data":{"id":group_id,"recordId":ticketid},"sign":"nosign","timestamp":1658474800545}
        resp = requests.post(url, json=json, headers=headersvcz)
        print(resp.text)
        orderid = resp.json()["data"]
        print("活动订单id号：",orderid)
        #退款
        url = "https://test.chebufan.cn/vcd/api/open/profit/order/refund"
        json = {"data":{"id":orderid,"refundReason":"退款自动化%s"%(startTime)},"sign":"nosign","timestamp":1658476386831}
        resp = requests.post(url, json=json, headers=headersvcd)
        print(resp.text)
        self.assertEqual("退款成功",resp.json()["data"])

    def test_3_2(self):
        #创建拼团活动
        self.test_1_3()
        url = "https://test.chebufan.cn/vcd/api/open/profit/order/info"
        json = {"data":{"id":group_id},"sign":"nosign","timestamp":1658476387838}
        resp = requests.post(url, json=json, headers=headersvcd)
        self.assertEqual("成功", resp.json()["msg"])

    @classmethod
    def tearDownClass(cls):
        closeprofit()

if __name__ == "__main__":
    time.sleep(3)
    unittest.main(verbosity=2)