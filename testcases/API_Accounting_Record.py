# -*- encoding=utf8 -*-
__author__ = "HXH"

import base64
import csv
import random
import unittest
import requests
import pymysql
import datetime
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
COMMON_DIR = os.path.join(BASE_DIR,"config")
sys.path.append(COMMON_DIR)
from common import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_cxgj,headers_admin_formdata,vpt_header

import xlrd
import openpyxl

class Accounting_Record(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global headersvcz
        headersvcz = headers_vcz(13538878368)

        global headersadmin
        headersadmin = headers_admin()

        global headers_admin_formdata
        headers_admin_formdata = headers_admin_formdata()

        global headersgzh
        headersgzh = cookies_headers_gzh(13538878368, 123456)

        global headerscxgj
        headerscxgj = headers_cxgj()

    def test_01(self):
        u'''对账结算—手动生成—可手动导入账单并推送至门店'''
        #读取文件
        file_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        data_dir = os.path.join(file_dir,"testdata","test_data_accounting_record.xlsx")
        test_file = open(data_dir, "rb")
        print("文件路径：",data_dir)
        url = "https://test.chebufan.cn/vcd/api/eticket/eticketBill/importBillExcel"
        # 导入账单
        files = {
            'itemType': (None, '5'),
            'beginDay': (None, '2022-01-01'),
            'endDay': (None, '2022-12-31'),
            'file':  open(data_dir, "rb")}
        importbill = requests.post(url,files=files,headers=headers_admin_formdata)
        print(importbill.text)
        #断言是否导入成功
        self.assertEqual("成功",importbill.json()['msg'])
        #获取导入记录id,导入明细id
        recordId = importbill.json()['data']['recordId']

        url ="https://test.chebufan.cn/vcd/api/eticket/eticketBillImportRecord/detail/page"
        json = {"timestamp":1657616972279,"sign":"nosign","data":{"params":{"shopName":"","billStatus":"","recordId":recordId}}}
        resp = requests.post(url,json=json,headers=headersadmin)
        global recordListId
        recordListId = resp.json()['data']['records'][0]["id"]
        print("导入门店账单id：",recordListId)
        #推送账单
        url = "https://test.chebufan.cn/vcd/api/eticket/eticketBill/pushBillRecord"
        json = {"timestamp":1650435318211,"sign":"nosign","data":{"billIdList":[recordListId]}}
        push = requests.post(url,json=json,headers=headersadmin)
        print(push.text)
        self.assertEqual("成功",push.json()['msg'])
        #断言车店端账单列表，10为待核对
        url = "https://test.chebufan.cn/vcd/api/open/eticket/eticketBills/getEticketBillList"
        json ={
                    "data": {
                        "current": 1,
                        "size": 5,
                        "pages": 0,
                        "params": {
                            "stateList": [10]
                        },
                        "total": 1
                    },
                    "sign": "nosign",
                    "timestamp": 1650437046233
                }
        list = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual(10,list.json()["data"]["records"][0]["state"])

    def test_02(self):
        u'''对账结算—待核对—财务审核中—已入账'''
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

        self.test_01()
        #核对账单
        url = "https://test.chebufan.cn/vcd/api/open/eticket/eticketBills/settleEticketBill"
        json =  {
                    "data": {
                        "eticketBillId": recordListId
                    },
                    "sign": "nosign",
                    "timestamp": 1650437888920
                }
        settle = requests.post(url,json=json,headers=headersvcd)
        #断言账单状态 ,25为财务审核中
        url = "https://test.chebufan.cn/vcd/api/open/eticket/eticketBills/getEticketBillDetail"
        json = {"data":{"eticketBillId":recordListId},"sign":"nosign","timestamp":1650438564161}
        detail = requests.post(url,json=json,headers=headersvcd)
        state = detail.json()["data"]["state"]
        self.assertEqual(25,state)
        #管理端推已入账
        url = "https://test.chebufan.cn/vcd/api/eticket/eticketBill/points-credited"
        json = {"timestamp":1650439078433,"sign":"nosign","data":{"id":recordListId}}
        confirm = requests.post(url,json=json,headers=headersadmin)
        #断言账单状态 ,35为已入账
        url = "https://test.chebufan.cn/vcd/api/open/eticket/eticketBills/getEticketBillDetail"
        json = {"data": {"eticketBillId": recordListId}, "sign": "nosign", "timestamp": 1650438564161}
        detail = requests.post(url, json=json, headers=headersvcd)
        state = detail.json()["data"]["state"]
        self.assertEqual(35, state)
        #断言账单能否下载
        url = "https://test.chebufan.cn/vcd/api/open/eticket/eticketBills/exportBillExcel"
        json = {"data":{"eticketBillId":recordListId},"sign":"nosign","timestamp":1650439892102}
        exportBillExcel = requests.post(url,json=json,headers=headersadmin)
        self.assertEqual(200,exportBillExcel.status_code)

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
        print("入账后的门店积分：",repairTotalCommission2)
        self.assertEqual(float(repairTotalCommission1) + 110, float(repairTotalCommission2))

    def test_03(self):
        u'''对账结算—待核对—待结算—已结算'''
        # 连接数据库
        conn = pymysql.connect(host="121.201.18.86", port=3325, user="root", passwd="Joysim!@#832727", db="cbf")
        # 创建游标
        cur = conn.cursor()
        sql = "UPDATE ycx_repair set eticket_invoice_status = 1 WHERE id = 1361"
        # 执行游标
        cur.execute(sql)
        conn.commit()

        self.test_01()

        #核对账单
        url = "https://test.chebufan.cn/vcd/api/open/eticket/eticketBills/settleEticketBill"
        json =  {
                    "data": {
                        "eticketBillId": recordListId
                    },
                    "sign": "nosign",
                    "timestamp": 1650437888920
                }
        settle = requests.post(url,json=json,headers=headersvcd)
        #断言账单状态 ,20为待结算
        url = "https://test.chebufan.cn/vcd/api/open/eticket/eticketBills/getEticketBillDetail"
        json = {"data":{"eticketBillId":recordListId},"sign":"nosign","timestamp":1650438564161}
        detail = requests.post(url,json=json,headers=headersvcd)
        state = detail.json()["data"]["state"]
        self.assertEqual(20,state)

        #上传图片
        url = "https://test.chebufan.cn/vcd/api/open/misc/attachment/upload"
        file_dir = os.path.abspath(os.path.dirname((os.path.dirname(__file__))))
        pic_dir = os.path.join(file_dir + "\\testdata\picture.jpg")
        files = {"file": open(pic_dir,"rb") }
        upload = requests.post(url, files=files)
        pic_url = upload.json()["data"]
        print("图片路径：",upload.json()["data"])

        #管理端推已结算
        url = "https://test.chebufan.cn/vcd/api/eticket/eticketBill/settle-account"
        json = {"timestamp":1650444259032,"sign":"nosign","data":{"imageUrl":pic_url,"id":recordListId}}
        confirm = requests.post(url, json=json, headers=headersadmin)

        #断言账单状态 ,30为已结算
        url = "https://test.chebufan.cn/vcd/api/open/eticket/eticketBills/getEticketBillDetail"
        json = {"data": {"eticketBillId": recordListId}, "sign": "nosign", "timestamp": 1650438564161}
        detail = requests.post(url, json=json, headers=headersvcd)
        state = detail.json()["data"]["state"]
        self.assertEqual(30, state)

    # def test_04(self):
    #     u''' 对账结算—系统生成—可系统生成账单并推送至门店'''

    @classmethod
    def tearDownClass(cls):
        #连接数据库
        conn = pymysql.connect(host="121.201.18.86",port=3325,user="root",passwd="Joysim!@#832727",db="cbf")
        #创建游标
        cur = conn.cursor()
        sql = "UPDATE ycx_repair set eticket_invoice_status = 0 WHERE id = 1361"
        #执行游标
        cur.execute(sql)
        conn.commit()



if __name__ == "__main__":
    unittest.main(verbosity=2)