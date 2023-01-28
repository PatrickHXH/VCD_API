# -*- encoding=utf8 -*-
__author__ = "HXH"

import base64
import datetime
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
# from dateutil.relativedelta import relativedelta
# from ddt import ddt, data, file_data

# global TEST_DATA
# FILE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
# TEST_DATA = os.path.join(FILE_DIR, "config", "TEST_DATA.json")

# @ddt
class My_Commission(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global headersvcz
        headersvcz = headers_vcz(13538878368)

        global headersadmin
        headersadmin = headers_admin()

        global headersgzh
        headersgzh = cookies_headers_gzh(13538878368,123456)

        global  headerscxgj
        headerscxgj = headers_cxgj()

        global headers_admin_formdata
        headers_admin_formdata = headers_admin_formdata()

    def test_0_1(self):
        u'''我的积分—门店认证—可保存门店认证信息，认证状态变为待审核，认证记录显示在管理端待审核列表'''
        global null
        null = None
        #获取当前时间
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #获取随机数
        randomnum = "".join(random.sample(string.ascii_letters+string.digits,20))
        randomnum = randomnum.upper()
        #上传图片
        file_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        #营业执照路径
        business_pic_dir = os.path.join(file_dir + "\\testdata\\business_auth.png")
        files = {"file":open(business_pic_dir,"rb")}
        url = "https://test.chebufan.cn/vcd/api/open/misc/ocr/businessLicense"
        upload = requests.post(url,files=files)
        print(upload.text)
        business_upload_dir = upload.json()["data"]["fileVisitUrl"]
        resultStr = upload.json()["data"]["resultStr"]
        #门头照路径
        shophead_pic_dir = os.path.join(file_dir+"\\testdata\picture.jpg")
        files = {"file":open(shophead_pic_dir,"rb")}
        url = "https://test.chebufan.cn/vcd/api/open/misc/attachment/upload"
        upload = requests.post(url,files=files)
        print(upload.text)
        shophead_upload_dir = upload.json()["data"]

        #上传门店信息
        url = "https://test.chebufan.cn/vcd/api/open/shop/updateLicense"
        json = {
                    "data": {
                        "businessLicenseImg": business_upload_dir,
                        "businessLicenseNo": randomnum,
                        "businessBeginTime": now,
                        "businessStatus": 10,
                        "businessFrontImg": shophead_pic_dir,
                        "businessRemark": "备注test",
                        "ocrJsonStr":resultStr
                    },
                    "sign": "nosign",
                    "timestamp": 1649749475803
                }
        updateLicense = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",updateLicense.json()["msg"])

    # def test_0_5(self):
    #     u'''我的积分—提现—银行卡—可添加或删除银行卡(需要获取验证码，暂无法测试)'''

    '''
    INSERT INTO `cbf`.`commission_account`(`id`, `repair_id`, `sys_user_id`, `phone`, `card_no`, `card_holder`, `attribute`, `remark`,
                         `update_time`, `update_user`, `insert_time`, `insert_user`, `card_name`, `card_code`)
    VALUES(100, 1361, 1297, '15800190443', '622908393223688212', '测试', 0, NULL, '2021-11-02 17:58:28', 1297,
           '2021-11-02 17:58:28', 1297, '兴业银行', 'CIB');
    '''

    # def test_0_7(self):
    #     u'''我的积分—提现—可提现并跳转提现进度页（需要获取验证码，暂无法测试）'''

    def test_0_8(self):
        u'''我的积分—提现—提现记录—提现记录返回正确（需要获取验证码，暂无法测试）'''
        url = "https://test.chebufan.cn/vcd/api/open/commission/withdrawLogList"
        json = {"data":{"current":1,"size":10,"pages":0,"params":{"state":1},"total":1},"sign":"nosign","timestamp":1653374770807}
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",resp.json()["msg"])

    # def test_0_9(self):
    #     u'''我的积分—积分明细—车险积分返回正确'''

    def test_1_1(self):
        u'''我的积分—积分明细—营销活动积分返回正确（涉及支付，暂无法测试，调用接口测试）'''
        url = "https://test.chebufan.cn/vcd/api/open/commission/list"
        json = {
                    "data": {
                        "current": 1,
                        "size": 10,
                        "pages": 42,
                        "params": {
                            "commissionType": "5"
                        },
                        "total": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1650766083856
                }
        rep = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",rep.json()["msg"])


    # def test_1_2(self):
    #     u'''我的积分—积分明细—对账结算积分返回正确（写在对账结算脚本里）'''

    def test_1_3(self):
        u'''我的积分—积分明细—积分收益返回正确（需通过定时器执行，暂无法测试，调用接口测试）'''
        url = "https://test.chebufan.cn/vcd/api/open/commission/list"
        json = {
            "data": {
                "current": 1,
                "size": 10,
                "pages": 42,
                "params": {
                    "commissionType": "7"
                },
                "total": 1
            },
            "sign": "nosign",
            "timestamp": 1650766083856
        }
        rep = requests.post(url, json=json, headers=headersvcd)
        self.assertEqual("成功", rep.json()["msg"])

    def test_1_4(self):
        u'''我的积分—积分明细—积分合并返回正确（暂无法测试，调用接口测试）'''
        url = "https://test.chebufan.cn/vcd/api/open/commission/list"
        json = {
            "data": {
                "current": 1,
                "size": 10,
                "pages": 42,
                "params": {
                    "commissionType": "8"
                },
                "total": 1
            },
            "sign": "nosign",
            "timestamp": 1650766083856
        }
        rep = requests.post(url, json=json, headers=headersvcd)
        self.assertEqual("成功", rep.json()["msg"])

    # def test_1_5(self):
    #     u'''我的积分—积分明细—绩效发放返回正确'''

    def test_1_6(self):
        u'''我的积分—积分明细—绩效提成返回正确（暂无法测试，调用列表接口测试）'''
        url = "https://test.chebufan.cn/vcd/api/open/commission/list"
        json = {
            "data": {
                "current": 1,
                "size": 10,
                "pages": 42,
                "params": {
                    "commissionType": "9"
                },
                "total": 1
            },
            "sign": "nosign",
            "timestamp": 1650766083856
        }
        rep = requests.post(url, json=json, headers=headersvcd)
        self.assertEqual("成功",rep.json()["msg"])
        # print(rep.text)
        # repairTotalCommission_1 = rep.json()["data"]["records"][0]["repairTotalCommission"]
        # print("员工积分发放前总额：",repairTotalCommission_1)
        # self.test_1_5()
        # rep = requests.post(url, json=json, headers=headers_vcd(13533131756))
        # repairTotalCommission_2 = rep.json()["data"]["records"][0]["repairTotalCommission"]
        # print("员工积分发放后总额：",repairTotalCommission_2)
        # self.assertEqual(float(repairTotalCommission_2) - 0.02, float(repairTotalCommission_1))

    def test_1_8(self):
        u'''我的积分—积分明细—会员卡返回正确（涉及支付，暂无法测试，调用接口测试）'''
        url = "https://test.chebufan.cn/vcd/api/open/commission/list"
        json = {
            "data": {
                "current": 1,
                "size": 10,
                "pages": 42,
                "params": {
                    "commissionType": "11"
                },
                "total": 1
            },
            "sign": "nosign",
            "timestamp": 1650766083856
        }
        rep = requests.post(url, json=json, headers=headersvcd)
        self.assertEqual("成功", rep.json()["msg"])

    def test_1_9(self):
        u'''我的积分—积分明细—接车开单返回正确（涉及支付，暂无法测试，调用接口测试）'''
        url = "https://test.chebufan.cn/vcd/api/open/commission/list"
        json = {
            "data": {
                "current": 1,
                "size": 10,
                "pages": 42,
                "params": {
                    "commissionType": "12"
                },
                "total": 1
            },
            "sign": "nosign",
            "timestamp": 1650766083856
        }
        rep = requests.post(url, json=json, headers=headersvcd)
        self.assertEqual("成功",rep.json()["msg"])

    def test_2_1(self):
        u'''我的积分—积分收益—开启收益弹窗—勾选下次不再提示后选择暂不开启，不再收到弹窗提示'''
        #关闭弹窗
        url = "https://test.chebufan.cn/vcd/api/open/commission/tip"
        json = {
                    "data": {
                        "queryType": 3
                    },
                    "sign": "nosign",
                    "timestamp": 1653298489627
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        #查看弹窗状态
        json = {
                    "data": {
                        "queryType": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1653298489627
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual(False,resp.json()["data"])

    def test_2_2(self):
        u''' 我的积分—积分收益—前往领取—可开启积分收益（需定时器执行）'''
        #开启积分收益
        url = "https://test.chebufan.cn/vcd/api/open/commission/tip"
        json = {"data":{"queryType":2},"sign":"nosign","timestamp":1653363262069}
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual(True,resp.json()["data"])
        #访问积分收益详情页
        url = "https://test.chebufan.cn/vcd/api/open/commission/commissionIncome/descriptionPage"
        json = {"data":{},"sign":"nosign","timestamp":1653363263294}
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual(True,resp.json()["data"]["openIncome"])
    # def test_2_2(self):
    #     u'''我的积分—积分收益—收益明细—可收到消息模板且收益返回正确（无法测试）'''

    def test_2_3(self):
        u'''我的积分—积分明细—可查看积分详情页'''
        url = "https://test.chebufan.cn/vcd/api/open/commission/get"
        json = {
                    "data": {
                        "id": "3684"
                    },
                    "sign": "nosign",
                    "timestamp": 1657679225598
                }
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",resp.json()["msg"])
    @classmethod
    def tearDownClass(cls):
        pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
