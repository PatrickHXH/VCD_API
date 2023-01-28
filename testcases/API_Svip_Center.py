# -*- encoding=utf8 -*-
__author__ = "HXH"

import unittest
import requests
import datetime
import os
import sys
path1 = os.path.abspath('API_SVIP')
print(path1)
sys.path.append(path1+"/config/")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
COMMON_DIR = os.path.join(BASE_DIR,"config")
sys.path.append(COMMON_DIR)
from common import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_cxgj,headers_admin_formdata,vpt_header


class SVIP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global headersvcz
        headersvcz = headers_vcz(13538878368)

    def test_0_1(self):
        u'''会员中心—卡管理—新增—可新增储值卡'''
        url_svipcardadd = "https://test.chebufan.cn/vcd/api/open/svip/svipCard/add"
        json = {
                    "data":{
                        "minRechargeAmount":"77",
                        "openAward":1,
                        "imageUrl":"https://cbfoss.oss-cn-guangzhou.aliyuncs.com/vcd/miniapp/svip/golden.png?versionId=CAEQDhiCgMCh6_C48hciIGQyNWRmMGNmNDY1NTRlMDE5ZWJmZmVlMTg4MjM2NjFh",
                        "name":"储值卡自动化测试",
                        "discount":"5.5",
                        "awardRate":"30",
                        "descriptions":[
                            "仅限七座以下非营运车辆可参与",
                            "不可与店内其他优惠同时使用"
                        ]
                    },
                    "sign":"nosign",
                    "timestamp":1644216541908
                }
        svipcardadd = requests.post(url_svipcardadd,json=json,headers=headersvcd)
        # print(svipcardadd.text)
        self.assertIn("成功",svipcardadd.json()['msg'])
        global carid
        carid = svipcardadd.json()["data"]["id"]

    def test_0_2(self):
        u'''会员中心—卡管理—编辑—可编辑储值卡'''
        self.test_0_1()
        url_svipcardupdate = "https://test.chebufan.cn/vcd/api/open/svip/svipCard/update"
        json = {
                    "data":{
                        "discount":5.5,
                        "descriptions":[
                            "仅限七座以下非营运车辆可参与",
                            "不可与店内其他优惠同时使用"
                        ],
                        "minRechargeAmount":"99",
                        "openAward":1,
                        "imageUrl":"https://cbfoss.oss-cn-guangzhou.aliyuncs.com/vcd/miniapp/svip/golden.png?versionId=CAEQDhiCgMCh6_C48hciIGQyNWRmMGNmNDY1NTRlMDE5ZWJmZmVlMTg4MjM2NjFh",
                        "name":"储值卡自动化测试编辑",
                        "awardRate":"60",
                        "id":carid
                    },
                    "sign":"nosign",
                    "timestamp":1644223107161
                }
        svipcardupdate = requests.post(url_svipcardupdate,json=json,headers=headersvcd)
        self.assertIn("成功",svipcardupdate.json()["msg"])
        global  vipid
        vipid = svipcardupdate.json()["data"]["id"]
        #查看储值卡列表
        url_svipcardget = "https://test.chebufan.cn/vcd/api/open/svip/svipCard/get"
        json = {"data":{"id":vipid},"sign":"nosign","timestamp":1644222925037}
        svipcardget = requests.post(url_svipcardget,json=json,headers=headersvcd)
        # print(svipcardget.text)
        self.assertEqual(60.0000,svipcardget.json()["data"]["awardRate"])
        self.assertEqual(99.00,svipcardget.json()["data"]["minRechargeAmount"])

    def test_0_3(self):
        u'''会员中心—卡管理—新增—可新增套餐卡'''
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
        global carid
        carid = svipcardadd.json()["data"]["id"]

    def test_0_4(self):
        u'''会员中心—卡管理—编辑—可编辑套餐卡'''
        self.test_0_3()
        url_svipcardupdate = "https://test.chebufan.cn/vcd/api/open/profit/sku/comboCard/update"
        json = {
                    "data": {
                        "validTimeValue": 6,
                        "tickets": [{
                            "name": "自动化",
                            "num": 2,
                            "originalPrice": 99
                        }],
                        "salePrice": "77",
                        "descriptions": ["特惠活动购买不退换不折现", "优惠券以及金额等权益过期作废不予退还"],
                        "imageUrl": "https://cbfoss.oss-cn-guangzhou.aliyuncs.com/vcd/miniapp/svip/black.png?versionId=CAEQEhiBgMDZ2pnA8xciIDBjYTJiMmZjZDFhNTRhMTBiZDE3NmNhNjk1YmY0Nzg3",
                        "name": "套餐卡自动化",
                        "openAward": 1,
                        "id": carid,
                        "awardRate": "40",
                        "validTimeUnit": 2
                    },
                    "sign": "nosign",
                    "timestamp": 1644284754647
                }
        svipcardupdate = requests.post(url_svipcardupdate,json=json,headers=headersvcd)
        self.assertIn("成功",svipcardupdate.json()["msg"])
        global comboid
        comboid= svipcardupdate.json()["data"]["id"]
        # print(svipcardupdate.text)
        #查看套餐卡列表
        url_svipcardget = "https://test.chebufan.cn/vcd/api/open/profit/sku/comboCard/get"
        json = {"data":{"id":comboid},"sign":"nosign","timestamp":1644222925037}
        svipcardget = requests.post(url_svipcardget,json=json,headers=headersvcd)
        # print(svipcardget.text)
        self.assertEqual(40.00,svipcardget.json()["data"]["awardRate"])
        self.assertEqual(77.00,svipcardget.json()["data"]["salePrice"])

    def test_0_5(self):
        u'''会员中心—客户开卡—可开储值卡'''
        self.test_0_2()
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
                        "amount": "200",
                        "otherAmount": "50",
                        "payType": 3,
                        "salesperson": "",
                        "cardId": vipid,
                        "licenseNoList": ["粤DGJ136"],
                        "receiveMoney": 1000
                    },
                    "sign": "nosign",
                    "timestamp": 1644289312404
                }
        create = requests.post(url_create,json=json,headers=headersvcd)
        self.assertIn("成功",create.json()["msg"])

    def test_0_6(self):
        u'''会员中心—客户开卡—可开套餐卡'''
        self.test_0_4()
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
                        "salesperson": "1421",
                        "cardId": comboid,
                        "licenseNoList": ["粤DGEC11"],
                        "receiveMoney": 96,
                        "ignoreRepeatedCreateTips": false
                    },
                    "sign": "nosign",
                    "timestamp": 1644304629295
                }
        create = requests.post(url_create,json=json,headers=headersvcd)
        self.assertIn("成功",create.json()["msg"])

    def test_0_7(self):
        u'''会员中心—会员充值—可充值储值卡'''
        #搜索用户信息
        true = True
        url_customerdetail = "https://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/customerDetail"
        json = {
                    "data": {
                        "phone": "13538878368"
                    },
                    "sign": "nosign",
                    "timestamp": 1644304692879
                }
        customerdetail = requests.post(url_customerdetail,json=json,headers=headersvcd)
        accountId = customerdetail.json()["data"]["accountId"]
        svipcarid = customerdetail.json()["data"]["cardId"]
        print("账户id：",accountId)
        #充值储值卡
        url_recharge = "https://test.chebufan.cn/vcd/api/open/svip/svipAccount/recharge"
        json ={
                    "data": {
                        "accountId": accountId,
                        "czPhone": "13538878368",
                        "amount": "300",
                        "otherAmount": "50",
                        "payType": 3,
                        "salesperson": "",
                        "cardId": svipcarid,
                        "ignoreRepeatedCreateTips": true
                    },
                    "sign": "nosign",
                    "timestamp": 1649313603925
                }
        recharge = requests.post(url_recharge,json=json,headers=headersvcd)
        self.assertIn("成功",recharge.json()["msg"])

    def test_0_8(self):
        u'''会员中心—员工提成—可编辑金额和员工'''
        #开套餐卡
        self.test_0_6()
        #查看员工提成列表
        now = datetime.datetime.now().strftime("%Y-%#m")
        print(now)
        url_shopEmployeeAwardpage ="https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page"
        json = {
                    "data": {
                        "date": now,
                        "state": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1644370545566
                }
        shopEmployeeAwardpage = requests.post(url_shopEmployeeAwardpage,json=json,headers=headersvcd)
        # print(shopEmployeeAwardpage.text)
        shopEmployeeAwardpage_id = shopEmployeeAwardpage.json()["data"]["records"][0]["id"]
        #编辑员工和金额
        url_shopEmployeeAwardupdate= "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/update"
        json = {"data":{"salespersonId":"1421","awardAmount":"20","id":shopEmployeeAwardpage_id},"sign":"nosign","timestamp":1644377572777}
        shopEmployeeAwardupdate = requests.post(url_shopEmployeeAwardupdate,json=json,headers=headersvcd)
        self.assertIn("成功",shopEmployeeAwardupdate.json()["msg"])

    def test_0_9(self):
        u'''会员中心—员工提成—可作废'''
        #开套餐卡
        self.test_0_6()
        #查看员工提成列表
        now = datetime.datetime.now().strftime("%Y-%#m")
        print(now)
        url_shopEmployeeAwardpage ="https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page"
        json = {
                    "data": {
                        "date": now,
                        "state": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1644370545566
                }
        shopEmployeeAwardpage = requests.post(url_shopEmployeeAwardpage,json=json,headers=headersvcd)
        # print(shopEmployeeAwardpage.text)
        shopEmployeeAwardpage_id = shopEmployeeAwardpage.json()["data"]["records"][0]["id"]
        #作废
        url_shopEmployeeAwardState = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/updateState"
        json = {
                    "data": {
                        "id": [shopEmployeeAwardpage_id],
                        "state": 9
                    },
                    "sign": "nosign",
                    "timestamp": 1644375020441
                }
        shopEmployeeAwardState = requests.post(url_shopEmployeeAwardState,json=json,headers=headersvcd)
        self.assertIn("成功",shopEmployeeAwardState.json()["msg"])
        # print(shopEmployeeAwardState.text)

    def test_1_1(self):
        u'''会员中心—员工提成—可使用门店积分发放提成'''
        #开套餐卡
        self.test_0_6()
        #查看员工提成列表
        now = datetime.datetime.now().strftime("%Y-%#m")
        print(now)
        url_shopEmployeeAwardpage ="https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/page"
        json = {
                    "data": {
                        "date": now,
                        "state": 0
                    },
                    "sign": "nosign",
                    "timestamp": 1644370545566
                }
        shopEmployeeAwardpage = requests.post(url_shopEmployeeAwardpage,json=json,headers=headersvcd)
        # print(shopEmployeeAwardpage.text)
        shopEmployeeAwardpage_id = shopEmployeeAwardpage.json()["data"]["records"][0]["id"]
        #编辑员工和金额
        url_shopEmployeeAwardupdate= "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/update"
        json = {"data":{"salespersonId":"1421","awardAmount":"0.01","id":shopEmployeeAwardpage_id},"sign":"nosign","timestamp":1644377572777}
        shopEmployeeAwardupdate = requests.post(url_shopEmployeeAwardupdate,json=json,headers=headersvcd)
        #点击确认
        url_shopEmployeeAwardState = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/updateState"
        json = {"data":{"id":[shopEmployeeAwardpage_id],"state":1},"sign":"nosign","timestamp":1644385995383}
        shopEmployeeAwardState = requests.post(url_shopEmployeeAwardState,json=json,headers=headersvcd)
        self.assertIn("成功",shopEmployeeAwardState.json()["msg"])
        #门店积分支付
        url_confirmAndPay = "https://test.chebufan.cn/vcd/api/open/shop/shopEmployeeAward/confirmAndPay"
        json = {"data":{"ids":[shopEmployeeAwardpage_id],"type":[1]},"sign":"nosign","timestamp":1644386004575}
        confirmAndPay = requests.post(url_confirmAndPay,json=json,headers=headersvcd)
        self.assertIn("成功",confirmAndPay.json()["msg"])

    # def test_1_2(self):
    #     u'''会员中心—员工提成—可使用微信支付发放提成'''
    #     pass

    def test_1_3(self):
        u'''会员列表—访客详情—储值卡—可收银'''
        #获取访客详情
        url_getShopVisitorDetail = 'https://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/getShopVisitorDetail'
        json = {
                    "data": {
                        "id": "1422796926413893634"
                    },
                    "sign": "nosign",
                    "timestamp": 1644974920444
                }
        getShopVisitorDetail = requests.post(url_getShopVisitorDetail,json=json,headers=headersvcd)
        vipCardDtoListid = getShopVisitorDetail.json()["data"]["vipCardDtoList"][0]["id"]
        amountbefore = getShopVisitorDetail.json()["data"]["vipCardDtoList"][0]["amount"]
        print("收银前金额：",amountbefore)
        #收银
        url_deduct = "https://test.chebufan.cn/vcd/api/open/svip/svipAccount/deduct"
        json = {
                    "data": {
                        "cardId":  vipCardDtoListid,
                        "amount": "0.01"
                    },
                    "sign": "nosign",
                    "timestamp": 1644572882293
                }
        deduct = requests.post(url_deduct,json=json,headers=headersvcd)
        # 获取访客详情
        url_getShopVisitorDetail = 'https://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/getShopVisitorDetail'
        json = {
                    "data": {
                        "id": "1422796926413893634"
                    },
                    "sign": "nosign",
                    "timestamp": 1644974920444
                }
        getShopVisitorDetail = requests.post(url_getShopVisitorDetail, json=json, headers=headersvcd)
        amountafter = getShopVisitorDetail.json()["data"]["vipCardDtoList"][0]["amount"]
        print("收银后金额：", amountafter)
        self.assertEqual(amountbefore-0.01,amountafter)

    def test_1_4(self):
        u'''会员列表—访客详情—储值卡—可升级'''
        #查询当前储值卡id
        url_getShopVisitorDetail = 'https://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/getShopVisitorDetail'
        json = {
                    "data": {
                        "id": "1422796926413893634"
                    },
                    "sign": "nosign",
                    "timestamp": 1644974920444
                }
        getShopVisitorDetail = requests.post(url_getShopVisitorDetail,json=json,headers=headersvcd)
        vipCardDtoListid = getShopVisitorDetail.json()["data"]["vipCardDtoList"][0]["id"]
        #查看卡升级页
        url_svipCardpage = "https://test.chebufan.cn/vcd/api/open/svip/svipCard/page"
        json = {
                    "data": {
                        "current": 1,
                        "size": 1000,
                        "params": {
                            "states": [1]
                        },
                        "total": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1644978266355
                }
        svipCardpage = requests.post(url_svipCardpage,json=json,headers=headersvcd)
        svipcardid = svipCardpage.json()["data"]["records"][0]["id"]
        #升级储值卡
        url_upgrade = "https://test.chebufan.cn/vcd/api/open/svip/svipAccount/upgrade"
        json = {
                    "data": {
                        "userCardId": vipCardDtoListid,
                        "svipCardId": svipcardid
                    },
                    "sign": "nosign",
                    "timestamp": 1644974787790
                }
        upgrade = requests.post(url_upgrade,json=json,headers=headersvcd)
        self.assertIn("成功",upgrade.json()["msg"])

    def test_1_5(self):
        u'''会员列表—访客详情—储值卡—可查看使用记录'''
        #查询当前储值卡id
        url_getShopVisitorDetail = 'https://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/getShopVisitorDetail'
        json = {
                    "data": {
                        "id": "1422796926413893634"
                    },
                    "sign": "nosign",
                    "timestamp": 1644974920444
                }
        getShopVisitorDetail = requests.post(url_getShopVisitorDetail,json=json,headers=headersvcd)
        vipCardDtoListid = getShopVisitorDetail.json()["data"]["vipCardDtoList"][0]["id"]
        #查看储值卡使用记录
        url_getUsageRecord = "https://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/getUsageRecord"
        json = {
                    "data": {
                        "current": 1,
                        "size": 10,
                        "params": {
                            "id": vipCardDtoListid,
                            "cardType": "1",
                            "logType": "3"
                        },
                        "total": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1644995961248
                }
        getUsageRecord = requests.post(url_getUsageRecord,json=json,headers=headersvcd)
        self.assertIn("成功",getUsageRecord.json()['msg'])

    def test_1_6(self):
        u'''会员列表—访客详情—储值卡—可退卡'''
        #查询当前储值卡id
        url_getShopVisitorDetail = 'https://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/getShopVisitorDetail'
        json = {
                    "data": {
                        "id": "1422796926413893634"
                    },
                    "sign": "nosign",
                    "timestamp": 1644974920444
                }
        getShopVisitorDetail = requests.post(url_getShopVisitorDetail,json=json,headers=headersvcd)
        vipCardDtoListid = getShopVisitorDetail.json()["data"]["vipCardDtoList"][0]["id"]
        #退卡
        url_refund = "https://test.chebufan.cn/vcd/api/open/svip/svipAccount/refund"
        json = {
                    "data": {
                        "id": vipCardDtoListid
                    },
                    "sign": "nosign",
                    "timestamp": 1644983370557
                }
        refund = requests.post(url_refund,json=json,headers=headersvcd)
        self.assertIn("成功",refund.json()["msg"])

    def test_1_7(self):
        u'''会员列表—访客详情—套餐卡—可核销优惠券'''
        #获取访客详情
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
        #获取套餐卡优惠券列表
        url_getTicketList = "https://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/getTicketList"
        json = {
                    "data": {
                        "type": 1,
                        "accountId": "1422796926413893634",
                        "cardId": vipCardDtoListid
                    },
                    "sign": "nosign",
                    "timestamp": 1644998643958
                }
        getTicketList = requests.post(url_getTicketList,json=json,headers=headersvcd)
        Couponsid = getTicketList.json()["data"][0]["id"]
        print(Couponsid)
        #核销优惠券
        url_checkTicket = "https://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/checkTicket"
        json = {
                    "data": {
                        "id": Couponsid
                    },
                    "sign": "nosign",
                    "timestamp": 1644998658015
                }
        checkTicket = requests.post(url_checkTicket,json=json,headers=headersvcd)
        self.assertIn("成功",checkTicket.json()["msg"])
        #断言优惠券列表数量
        url  ="https://test.chebufan.cn/vcd/api/open/shop/shopAccountProfile/getTicketList"
        json = {
            "data": {
                "type": 1,
                "accountId": "1422796926413893634",
                "cardId": vipCardDtoListid
            },
            "sign": "nosign",
            "timestamp": 1644998643958
        }
        getTicketList = requests.post(url_getTicketList, json=json, headers=headersvcd)
        self.assertEqual(1,getTicketList.json()["data"][0]["remainTimes"])

    def test_1_8(self):
        u'''会员列表—访客详情—套餐卡—可退卡'''
        #获取访客详情
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
        #退卡
        url_refund = "https://test.chebufan.cn/vcd/api/open/profit/sku/comboCard/refund"
        json = {
                    "data": {
                        "id": vipCardDtoListid
                    },
                    "sign": "nosign",
                    "timestamp": 1645002778922
                }
        refund = requests.post(url_refund,json=json,headers=headersvcd)
        self.assertIn("成功",refund.json()["msg"])
    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)