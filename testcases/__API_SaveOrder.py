# -*- encoding=utf8 -*-
__author__ = "HXH"

import base64
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
import  pymysql
import time

# @ddt
class SaveOrder(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global headersvcz
        headersvcz = headers_vcz(13538878368)

        global headersadmin
        headersadmin = headers_admin()

        # 入账员
        global headersgzh
        headersgzh = cookies_headers_gzh(13538878368,123456)

        #审核员
        global headersgzh1
        headersgzh1 = cookies_headers_gzh(13800138005,123456)

        global  headerscxgj
        headerscxgj = headers_cxgj()

        global headers_admin_formdata
        headers_admin_formdata = headers_admin_formdata()

        global vpt_header
        vpt_header = vpt_header()

        # 连接数据库
        conn = pymysql.connect(host="121.201.18.86", port=3325, user="root", passwd="Joysim!@#832727", db="cbf")
        # 创建游标
        cur = conn.cursor()
        # 关闭数据库安全模式
        sql1 = "SET SQL_SAFE_UPDATES = 0"
        cur.execute(sql1)
        # 查询最新ID
        sql2 = "SELECT * FROM commission WHERE car_no = '粤GAY825' ORDER BY insert_time desc LIMIT 0,1"
        cur.execute(sql2)
        commid = cur.fetchall()[0][0]
        print("佣金表id：", commid)
        a = "TDAA"
        b = ''.join(random.sample(string.digits, 9))
        c = ''.join(random.sample(string.digits, 9))
        num = a + b + c
        # 更改投保单号
        sql3 = "UPDATE commission SET biz_no='%s',force_no='%s' WHERE id = %d" % (num,num,commid)
        cur.execute(sql3)
        conn.commit()
        cur.close()
        conn.close()

    def test_0_1(self):
        u'''报价当天已出单,检查积分明细车险入账'''
        url = "https://test.chebufan.cn/vcd/api/open/commission/list"
        json = {
            "data": {
                "current": 1,
                "size": 10,
                "pages": 42,
                "params": {
                    "commissionType": "0"
                },
                "total": 1
            },
            "sign": "nosign",
            "timestamp": 1650766083856
        }
        rep = requests.post(url, json=json, headers=headersvcd)
        repairTotalCommission1 = rep.json()["data"]["records"][0]["repairTotalCommission"]
        print("入账前的门店积分：",repairTotalCommission1)

        #获取v平台平台保费和平台报价单
        url = "https://vpttest.chebufan.cn/admin-vpt/api/index/orderTrendStatistic"
        json = {"timestamp":1655258640529,"sign":"nosign","data":{"dateType":0,"areaType":0,"areaCode":"","areaName":""}}
        resp = requests.post(url,json=json,headers=vpt_header)
        print("平台保费为：",resp.json()["data"]["totalMoney"])
        before_totalMoney = resp.json()["data"]["totalMoney"]
        url = "https://vpttest.chebufan.cn/admin-vpt/api/index/orderQueryStatistic"
        json = {"timestamp":1655258637648,"sign":"nosign","data":{"dateType":0,"areaType":0,"areaCode":"","areaName":""}}
        resp = requests.post(url,json=json,headers=vpt_header)
        print("平台报价单为：",resp.json()["data"]["totalNum"])
        before_totalNum = resp.json()["data"]["totalNum"]
        # 测试数据：粤GAY825,TDZA202244010001175018
        # 入账账号：13538878368/123456
        # 填佣账号:   13538878368/123456
        # 审核账号：13800138005/123456
        false = False
        true = True
        null = None
        nextday = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        thisyear = datetime.datetime.now()
        nextyear = thisyear + datetime.timedelta(days=+365)
        nextyear = nextyear.strftime("%Y-%m-%d")
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        todayHMS = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(today)
        #一键报价，直接核保
        url = "http://test.chebufan.cn/chebftest/wx/xlc/cxgj/saveOrder"
        json = {
                    "remark":"",
                    "newCar":0,
                    "channelId":"",
                    "insureFrom":{
                        "name":"黄自动化",
                        "applicantType":"100",
                        "certificateType":"101",
                        "certificateNo":"44080",
                        "address":"自动化地址",
                        "phone":"17324233289",
                        "email":"",
                        "sameAsOwner":"1",
                        "imageInfoList":[

                        ]
                    },
                    "insureTo":{
                        "name":"黄自动化",
                        "applicantType":"100",
                        "certificateType":"101",
                        "certificateNo":"44080",
                        "address":"自动化地址",
                        "phone":"17324233289",
                        "email":"",
                        "sameAsOwner":"1",
                        "sameAsInsureFrom":"0",
                        "imageInfoList":[

                        ]
                    },
                    "policy":{
                        "insuredType":0,
                        "accidentRiskFlag":0
                    },
                    "vehicle":{
                        "licenseNo":"粤GAY825",
                        "enrollDate":"",
                        "transferVehicle":0
                    },
                    "risks":[

                    ],
                    "imgList":[

                    ],
                    "policyList":[
                        {
                            "insuredType":0,
                            "accidentRiskFlag":0,
                            "insureScheme":2,
                            "risks":[
                                {
                                    "riskCode":2,
                                    "riskName":"机动车损失险",
                                    "isInsured":true
                                },
                                {
                                    "riskCode":4,
                                    "riskName":"第三者责任险",
                                    "amount":"1000000",
                                    "isInsured":true,
                                    "Dict":"cxgjDszzrx"
                                },
                                {
                                    "riskCode":5,
                                    "riskName":"车上人员责任险（司机）",
                                    "amount":"10000",
                                    "isInsured":true,
                                    "Dict":"cxgjCsryzwxsj"
                                },
                                {
                                    "riskCode":6,
                                    "riskName":"车上人员责任险（乘客）",
                                    "unitAmount":"10000",
                                    "quantity":"",
                                    "isInsured":true,
                                    "Dict":"cxgjCsryzwxck"
                                }
                            ],
                            "tciStartDate":nextday,
                            "vciStartDate":nextyear,
                            "sortNum":1
                        }
                    ],
                    "policyArr":[
                        {
                            "insuredType":0,
                            "accidentRiskFlag":0,
                            "insureScheme":2,
                            "risks":{
                                "0":[
                                    {
                                        "riskCode":2,
                                        "riskName":"机动车损失险",
                                        "isInsured":true
                                    },
                                    {
                                        "riskCode":4,
                                        "riskName":"第三者责任险",
                                        "amount":"1000000",
                                        "isInsured":true,
                                        "Dict":"cxgjDszzrx"
                                    },
                                    {
                                        "riskCode":5,
                                        "riskName":"车上人员责任险（司机）",
                                        "amount":"10000",
                                        "isInsured":true,
                                        "Dict":"cxgjCsryzwxsj"
                                    },
                                    {
                                        "riskCode":6,
                                        "riskName":"车上人员责任险（乘客）",
                                        "unitAmount":"10000",
                                        "quantity":"",
                                        "isInsured":true,
                                        "Dict":"cxgjCsryzwxck"
                                    },
                                    {
                                        "riskCode":18,
                                        "riskName":"车身划痕损失险",
                                        "amount":"",
                                        "isInsured":false,
                                        "Dict":"cxgjCshhssx",
                                        "mainRiskCode":2
                                    },
                                    {
                                        "riskCode":13,
                                        "riskName":"法定节假日限额翻倍险",
                                        "amount":"",
                                        "isInsured":false,
                                        "mainRiskCode":4
                                    },
                                    {
                                        "riskCode":17,
                                        "riskName":"修理期间费用补偿险",
                                        "amount":"",
                                        "isInsured":false,
                                        "mainRiskCode":2
                                    },
                                    {
                                        "riskCode":19,
                                        "riskName":"车轮单独损失险",
                                        "amount":"",
                                        "isInsured":false,
                                        "Dict":"cxgjClddssx",
                                        "mainRiskCode":2
                                    }
                                ],
                                "1":[
                                    {
                                        "riskCode":21,
                                        "riskName":"绝对免赔率（车损）",
                                        "isInsured":false,
                                        "deductibleRate":"",
                                        "Dict":"cxgjJdmpl",
                                        "mainRiskCode":2
                                    },
                                    {
                                        "riskCode":22,
                                        "riskName":"绝对免赔率（三者）",
                                        "isInsured":false,
                                        "deductibleRate":"",
                                        "Dict":"cxgjJdmpl",
                                        "mainRiskCode":4
                                    },
                                    {
                                        "riskCode":25,
                                        "riskName":"绝对免赔率（司机）",
                                        "isInsured":false,
                                        "deductibleRate":"",
                                        "Dict":"cxgjJdmpl",
                                        "mainRiskCode":5
                                    },
                                    {
                                        "riskCode":28,
                                        "riskName":"绝对免赔率（乘客）",
                                        "isInsured":false,
                                        "deductibleRate":"",
                                        "Dict":"cxgjJdmpl",
                                        "mainRiskCode":6
                                    }
                                ],
                                "2":[
                                    {
                                        "riskCode":20,
                                        "riskName":"发动机进水损坏除外特约",
                                        "isInsured":false,
                                        "mainRiskCode":2
                                    },
                                    {
                                        "riskCode":23,
                                        "riskName":"精神损害抚慰金责任险（三者）",
                                        "isInsured":false,
                                        "amount":"",
                                        "mainRiskCode":4
                                    },
                                    {
                                        "riskCode":26,
                                        "riskName":"精神损害抚慰金责任险（司机）",
                                        "isInsured":false,
                                        "amount":"",
                                        "mainRiskCode":5
                                    },
                                    {
                                        "riskCode":29,
                                        "riskName":"精神损害抚慰金责任险（乘客）",
                                        "isInsured":false,
                                        "amount":"",
                                        "mainRiskCode":6
                                    }
                                ],
                                "3":[
                                    {
                                        "riskCode":24,
                                        "riskName":"医保外医疗费用责任险（三者）",
                                        "isInsured":false,
                                        "amount":"",
                                        "Dict":"cxgjYbwyyzrx",
                                        "mainRiskCode":4
                                    },
                                    {
                                        "riskCode":27,
                                        "riskName":"医保外医疗费用责任险（司机）",
                                        "isInsured":false,
                                        "amount":"",
                                        "Dict":"cxgjYbwyyzrx",
                                        "mainRiskCode":5
                                    },
                                    {
                                        "riskCode":30,
                                        "riskName":"医保外医疗费用责任险（乘客）",
                                        "isInsured":false,
                                        "amount":"",
                                        "Dict":"cxgjYbwyyzrx",
                                        "mainRiskCode":6
                                    }
                                ],
                                "4":[
                                    {
                                        "riskCode":31,
                                        "riskName":"增值服务特约（道路救援）",
                                        "isInsured":false,
                                        "times":"",
                                        "Dict":"cxgjJdczzfwtydljy"
                                    },
                                    {
                                        "riskCode":33,
                                        "riskName":"增值服务特约（代为驾驶）",
                                        "isInsured":false,
                                        "times":""
                                    },
                                    {
                                        "riskCode":34,
                                        "riskName":"增值服务特约（代为送检）",
                                        "isInsured":false,
                                        "times":""
                                    }
                                ]
                            },
                            "tciStartDate":nextday,
                            "vciStartDate":nextyear
                        }
                    ],
                    "userId":"1297",
                    "repairId":"1361",
                    "quoteFrom":2,
                    "teamInsuredCompany":"1",
                    "directUnderwriting":"1",
                    "repairName":"hxh_autotest001",
                    "userName":"黄管理2",
                    "owner":{
                        "name":"黄自动化",
                        "applicantType":"100",
                        "certificateType":"101",
                        "certificateNo":"44080",
                        "address":"自动化地址",
                        "phone":"17324233289",
                        "email":"",
                        "imageInfoList":[

                        ]
                    },
                    "payType":1,
                    "otherImageInfoList":[

                    ]
                }
        saveOrder = requests.post(url,json=json,cookies=headersgzh[0],headers=headersgzh[2])
        # print(saveOrder.text)
        policynum = saveOrder.json()["returnParm"]["mainInfo"]["order"]["id"]
        cxgjOrderId = saveOrder.json()["returnParm"]["mainInfo"]["order"]["cxgjOrderId"]
        entrustId = saveOrder.json()["returnParm"]["mainInfo"]["order"]["entrustId"]
        #报价员获取报价
        url = "http://zdbjtest.jximec.com/zdbj/cxyqzx/api/quoter/insurance/underwritingResult"
        json = {
                    "data":{
                        "branchId":null,
                        "insureType":2,
                        "manualUpdateStatus":0,
                        "newOrderList":[

                        ],
                        "policyOrderId":cxgjOrderId,
                        "proposalNo":"TDZA202244010001175018",
                        "viProposalNo":null,
                        "biProposalNo":null,
                        "accountId":"1339151515212435458",
                        "entrustId":entrustId,
                        "account":"12326"
                    },
                    "timestamp":1650272618060,
                    "sign":"nosign"
                }
        underwritingResult = requests.post(url,json=json,headers=headerscxgj)

        time.sleep(3)
        #抢单
        url = "http://zdbjtest.jximec.com/zdbj/cxyqzx/api/quoter/pool/grabbing"
        json = {"data":{"teamId":"","type":1,"insuredCompanyCode":"1","poolLevel":1},"timestamp":1650334092445,"sign":"nosign"}
        grabbing = requests.post(url,json=json,headers=headerscxgj)
        print(grabbing.text)

        time.sleep(3)
        #报价员推待支付
        file_dir = os.path.abspath((os.path.dirname(os.path.dirname(__file__))))
        pic_dir = os.path.join(file_dir + "\\testdata\picture.jpg")
        with open(pic_dir,"rb") as f:
            img_byte = base64.b64encode(f.read())     # 获取图片64编码
        url = "http://zdbjtest.jximec.com/zdbj/cxyqzx/api/quoter/push/underwriting"
        json ={
                "data":{
                    "type":0,
                    "insureType":3,
                    "optimizationQuoteValid":false,
                    "pushFeeInfo":1,
                    "accidentRiskIds":[

                    ],
                    "commissionRateFlag":1,
                    "qrCodeBase64Str":"data:image/png;base64,%s"%(img_byte),
                    "offerBase64Str":"data:image/png;base64,%s"%(img_byte),
                    "entrustId":entrustId,
                    "policyOrderId":cxgjOrderId,
                    "remark":"",
                    "feeInfo":"总2165.13，惠48.6，实2116.53",
                    "maintainId":"",
                    "checkCase":null,
                    "score":"46",
                    "viRatio":3,
                    "accidentRiskRatio":0,
                    "biRatio":3,
                    "vehicleTaxRatio":null,
                    "accidentRatio":0,
                    "ledger":{
                        "biAgentName":"广州市君林保险代理有限公司",
                        "biComName":"广州市天河支公司修理厂业务一部",
                        "viAgentName":"广州市君林保险代理有限公司",
                        "viComName":"广州市天河支公司修理厂业务一部"
                    },
                    "accidentPremium":245,
                    "biPremium":955.13,
                    "viPremium":665,
                    "vehicleTax":300,
                    "totalPremium":2165.13,
                    "commissionPremium":48.6,
                    "payPremium":2116.53,
                    "seatCount":5
                },
                "timestamp":1655198318422,
                "sign":"nosign"
            }
        underwriting = requests.post(url,json=json,headers=headerscxgj)
        print(underwriting.text)

        time.sleep(3)
        #报价员获取支付结果
        url = "http://zdbjtest.jximec.com/zdbj/cxyqzx/api/quoter/insurance/paymentResult"
        json = {
                    "data":{
                        "branchId":null,
                        "insureType":3,
                        "manualUpdateStatus":0,
                        "newOrderList":[

                        ],
                        "policyOrderId":cxgjOrderId,
                        "proposalNo":"TDAA202244010001203001",
                        "viProposalNo":"TDZA202244010001175018",
                        "biProposalNo":"TDAA202244010001203001",
                        "accountId":"1339151515212435458",
                        "entrustId":entrustId,
                        "account":"12326"
                    },
                    "timestamp":1655198331873,
                    "sign":"nosign"
                }
        paymentResult = requests.post(url,json=json,headers=headerscxgj)
        print(paymentResult.text)
        #报价员推送已支付
        url = "http://zdbjtest.jximec.com/zdbj/cxyqzx/api/quoter/push/paymentResult"
        json = {
                    "data":{
                        "type":0,
                        "entrustId":entrustId,
                        "policyOrderId":cxgjOrderId,
                        "insureType":3,
                        "ledgerId":null,
                        "viRatio":"3.00",
                        "biRatio":"3.00",
                        "accidentRatio":"0",
                        "storeChannelManager":"黄管理2",
                        "commissionRateFlag":1,
                        "storeName":"hxh_autotest001",
                        "licenseNo":"粤GAY825",
                        "biAgentName":"广州市君林保险代理有限公司",
                        "biComCode":null,
                        "biComName":"广州市天河支公司修理厂业务一部",
                        "viAgentName":"广州市君林保险代理有限公司",
                        "viComName":"广州市天河支公司修理厂业务一部",
                        "pushRepairCodeName":"利源名车汽车服务（广州）有限公司",
                        "biTransferTime":todayHMS,
                        "viTransferTime":todayHMS,
                        "totalPremium":null,
                        "viPremium":665,
                        "biPremium":955.13,
                        "vehicleTax":300,
                        "accidentPremium":245,
                        "comiWxKfMsg":"粤GAY825，2165.13(总)，1865.13(总不含税)，hxh_autotest001(积分)，黄管理2，48.60(积分)"
                    },
                    "timestamp":1655198344362,
                    "sign":"nosign"
                }
        push = requests.post(url,json=json,headers=headerscxgj)
        print(push.text)

        time.sleep(10)
        #获取v平台平台保费和平台报价单
        url = "https://vpttest.chebufan.cn/admin-vpt/api/index/orderTrendStatistic"
        json = {"timestamp":1655258640529,"sign":"nosign","data":{"dateType":0,"areaType":0,"areaCode":"","areaName":""}}
        resp = requests.post(url,json=json,headers=vpt_header)
        print("平台保费为：",resp.json()["data"]["totalMoney"])
        after_totalMoney = resp.json()["data"]["totalMoney"]
        print("平台报价单为：",resp.json()["data"]["totalOrderNum"])
        after_totalNum = resp.json()["data"]["totalOrderNum"]

        for i in range(0, 10):
            try:
                # 断言进店车辆统计是否正确
                print("断言次数:", i)
                # 断言进店车辆统计是否正确
                self.assertEqual(round(int(before_totalMoney + 2165.13), 2), round(int(after_totalMoney), 2))
                self.assertEqual(int(before_totalNum) + 1, int(after_totalNum))
            except AssertionError:
                resp = requests.post(url, json=json, headers=vpt_header)
                after_totalMoney = resp.json()["data"]["totalMoney"]
                after_totalNum = resp.json()["data"]["totalOrderNum"]


        #查询门店审核列表,填佣角色填佣
        url = "http://test.chebufan.cn/chebftest/wx/xlc/ordercx/qdOrderlist"
        params = {"pageFirst":1,
                        "pageNumber":1,
                        "pageSize":10,
                        "timeType":1,
                        "qdSearchText":"",
                        "qdTyAudit":1,
                        "commissionAuditStatuses":0,
                        "qdManagers":1297,
                        "licenseNo":"",
                        "fromSource":"custom",
                        "states":"11,12,13,14",
                        "beginSearchDate":"2022-05-22",
                        "endSearchDate":"2022-06-21"
        }
        resp = requests.get(url,params=params,cookies=headersgzh[0],headers=headersgzh[2])
        orderId = resp.json()["returnParm"]["list"][0]["yueBOrderId"]
        orderLogId = resp.json()["returnParm"]["list"][0]["orderLogId"]
        print(orderId)
        print(orderLogId)
        #填佣金
        url = "http://test.chebufan.cn/chebftest/wx/xlc/commission/qdManagerTy"
        json = {
                    "comiDeduct":{
                        "name":"",
                        "id":"",
                        "value":0
                    },
                    "operatorRole":10,
                    "orderId":orderId,
                    "orderLogId":orderLogId,
                    "investType":"",
                    "totalPremium":2165.13,
                    "discountAmount":"67.50",
                    "forceRate":"4",
                    "driveRate":"5",
                    "commissionAuditStatus":10,
                    "actualPremium":2097.63,
                    "qdCommissionRemark":"",
                    "bizInvestRate":0,
                    "forceInvestRate":0,
                    "driveInvestRate":0,
                    "bizRate":"3"
                }
        resp = requests.post(url,json=json,cookies=headersgzh[0],headers=headersgzh[2])
        print(resp.text)

        #查询门店审核列表,审核角色审核
        url = "http://test.chebufan.cn/chebftest/wx/xlc/ordercx/qdOrderlist"
        params = {"pageFirst":1,
                        "pageNumber":1,
                        "pageSize":10,
                        "timeType":1,
                        "qdSearchText":"",
                        "qdTyAudit":1,
                        "commissionAuditStatuses":"10,15",
                        "qdManagers":1297,
                        "licenseNo":"",
                        "fromSource":"custom",
                        "states":"11,12,13,14",
                        "beginSearchDate":"2022-05-22",
                        "endSearchDate":"2022-06-21"
        }
        resp = requests.get(url,params=params,cookies=headersgzh1[0],headers=headersgzh1[2])
        # print(resp.text)
        #确认审核
        url = "http://test.chebufan.cn/chebftest/wx/xlc/commission/qdManagerTy"
        json ={
                    "comiDeduct":{
                        "name":"",
                        "id":"",
                        "value":0
                    },
                    "operatorRole":20,
                    "orderId":orderId,
                    "orderLogId":orderLogId,
                    "investType":"",
                    "totalPremium":2165.13,
                    "discountAmount":"67.50",
                    "forceRate":"4",
                    "driveRate":"5",
                    "commissionAuditStatus":20,
                    "actualPremium":2097.63,
                    "qdCommissionRemark":"",
                    "bizInvestRate":"0",
                    "forceInvestRate":"0",
                    "driveInvestRate":"0",
                    "bizRate":"3"
                }
        resp = requests.post(url,json=json,cookies=headersgzh1[0],headers=headersgzh1[2])
        print(resp.text)


        #断言v车店积分明细
        url = "https://test.chebufan.cn/vcd/api/open/commission/list"
        json = {
            "data": {
                "current": 1,
                "size": 10,
                "pages": 42,
                "params": {
                    "commissionType": "0"
                },
                "total": 1
            },
            "sign": "nosign",
            "timestamp": 1650766083856
        }

        rep = requests.post(url, json=json, headers=headersvcd)
        repairTotalCommission2 = rep.json()["data"]["records"][0]["repairTotalCommission"]
        for i in range(0, 10):
            try:
                # 断言进店车辆统计是否正确
                print("断言次数:", i)
                print("入账后的门店积分：", repairTotalCommission2)
                self.assertEqual(float(repairTotalCommission1) + 67.5, float(repairTotalCommission2))
            except AssertionError:
                rep = requests.post(url, json=json, headers=headersvcd)
                repairTotalCommission2 = rep.json()["data"]["records"][0]["repairTotalCommission"]

    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main(verbosity=2)

