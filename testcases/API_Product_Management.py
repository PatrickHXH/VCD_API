# -*- encoding=utf8 -*-
__author__ = "HXH"

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


class Product_Management(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global headersvcz
        headersvcz = headers_vcz(13538878368)

        global  headersadmin
        headersadmin = headers_admin()

    def test_1_1(self):
        u'''产品管理—新增产品—可新增产品并添加至产品列表'''
        url = "https://test.chebufan.cn/vcd/api/open/receiveProject/addReceiveProject"
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        null =None
        true =True
        json ={
                "data": {
                    "id": null,
                    "shopId": null,
                    "categoryCode": "7",
                    "name": "自动化"+now,
                    "price": "88",
                    "originalPrice": "20",
                    "sellerRuleType": "2",
                    "sellerRuleList": [{
                        "awardAmount": "10",
                        "salesAmount": "50"
                    }, {
                        "awardRate": 0.05,
                        "salesAmount": "100"
                    }],
                    "workerRuleList": [{
                        "awardRate": 0.01
                    }],
                    "checked": true,
                    "sellerChecked": true,
                    "receiveChannels": [{
                        "id": "1572778685300994049",
                        "shopId": 0,
                        "name": "车点点",
                        "shortName": "点",
                        "color": "#8A9366",
                        "channelSalePrice": "10",
                        "channelSettlePrice": "8",
                        "channelId": "1572778685300994049"
                    }]
                },
                "sign": "nosign",
                "timestamp": 1664242980391
            }
        addReceiveProject = requests.post(url,json=json,headers=headersvcd)
        print(addReceiveProject.text)
        id = addReceiveProject.json()["data"]
        self.assertEqual("成功",addReceiveProject.json()["msg"])
        #查询产品列表
        url = "https://test.chebufan.cn/vcd/api/open/receiveProject/pageReceiveProject"
        json = {"data":{"size":10,"current":1,"params":{"categoryCode":"7","platform":0}},"sign":"nosign","timestamp":1649648627037}
        pageReceiveProject = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual(id,pageReceiveProject.json()["data"]["records"][0]["id"])

    def test_1_2(self):
        u'''产品管理—产品云下载—可下载产品并添加至产品列表'''
        #管理端新增产品
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        url = "https://test.chebufan.cn/vcd/api/receive/receiveProject/add"
        null = None
        false = False
        json = {"timestamp":1649657731305,"sign":"nosign","data":{"id":null,"name":"管理端产品自动化"+now,"categoryCode":"4","price":50}}
        add = requests.post(url,json=json,headers=headersadmin)
        self.assertEqual("成功",add.json()["msg"])
        #查看产品云列表
        url = "https://test.chebufan.cn/vcd/api/open/receiveProject/pageReceiveProject"
        json = {"data":{"size":10,"current":1,"params":{"categoryCode":"4","platform":1}},"sign":"nosign","timestamp":1649659983147}
        pageReceiveProject = requests.post(url,json=json,headers=headersvcd)
        tmpid = pageReceiveProject.json()["data"]["records"][0]["id"]
        self.assertEqual("管理端产品自动化"+now,pageReceiveProject.json()["data"]["records"][0]["name"])
        #下载产品
        url = "https://test.chebufan.cn/vcd/api/open/receiveProject/downloadReceiveProject"
        json = {
                    "data": {
                        "projectIdList": [tmpid]
                    },
                    "sign": "nosign",
                    "timestamp": 1649663765833
                }
        download = requests.post(url,json=json,headers=headersvcd)
        id = download.json()["data"]
        #新增产品
        url = "https://test.chebufan.cn/vcd/api/open/receiveProject/addReceiveProject"
        json = {
                    "data": {
                        "id": id,
                        "shopId": null,
                        "categoryCode": "1",
                        "name": "产品云下载"+now,
                        "price": 100,
                        "originalPrice": null,
                        "sellerRuleType": 1,
                        "sellerRuleList": [],
                        "workerRuleList": [],
                        "checked": false,
                        "sellerChecked": false,
                        "receiveChannels": []
                    },
                    "sign": "nosign",
                    "timestamp": 1664243273818
                }
        add = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",add.json()["msg"])
        #删除
        url ="https://test.chebufan.cn/vcd/api/receive/receiveProject/delete"
        json = {"timestamp":1649657734685,"sign":"nosign","data":{"id":tmpid}}
        delete = requests.post(url,json=json,headers=headersadmin)
        self.assertEqual("成功",delete.json()["msg"])

    def test_1_3(self):
        u'''产品管理—编辑产品—可修改产品信息'''
        url = "https://test.chebufan.cn/vcd/api/open/receiveProject/addReceiveProject"
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        null =None
        true =True
        json ={
                "data": {
                    "id": null,
                    "shopId": null,
                    "categoryCode": "7",
                    "name": "自动化"+now,
                    "price": "88",
                    "originalPrice": "20",
                    "sellerRuleType": "2",
                    "sellerRuleList": [{
                        "awardAmount": "10",
                        "salesAmount": "50"
                    }, {
                        "awardRate": 0.05,
                        "salesAmount": "100"
                    }],
                    "workerRuleList": [{
                        "awardRate": 0.01
                    }],
                    "checked": true,
                    "sellerChecked": true,
                    "receiveChannels": [{
                        "id": "1572778685300994049",
                        "shopId": 0,
                        "name": "车点点",
                        "shortName": "点",
                        "color": "#8A9366",
                        "channelSalePrice": "10",
                        "channelSettlePrice": "8",
                        "channelId": "1572778685300994049"
                    }]
                },
                "sign": "nosign",
                "timestamp": 1664242980391
            }
        addReceiveProject = requests.post(url,json=json,headers=headersvcd)
        id = addReceiveProject.json()["data"]
        self.assertEqual("成功",addReceiveProject.json()["msg"])
        #编辑产品
        url = "https://test.chebufan.cn/vcd/api/open/receiveProject/addReceiveProject"
        json = {
                "data": {
                    "id": id,
                    "shopId": null,
                    "categoryCode": "7",
                    "name": "自动化"+now,
                    "price": "88",
                    "originalPrice": "20",
                    "sellerRuleType": "2",
                    "sellerRuleList": [{
                        "awardAmount": "10",
                        "salesAmount": "50"
                    }, {
                        "awardRate": 0.05,
                        "salesAmount": "100"
                    }],
                    "workerRuleList": [{
                        "awardRate": 0.01
                    }],
                    "checked": true,
                    "sellerChecked": true,
                    "receiveChannels": [{
                        "id": "1572778685300994049",
                        "shopId": 0,
                        "name": "车点点",
                        "shortName": "点",
                        "color": "#8A9366",
                        "channelSalePrice": "10",
                        "channelSettlePrice": "8",
                        "channelId": "1572778685300994049"
                    }]
                },
                "sign": "nosign",
                "timestamp": 1664242980391
            }
        updateproject = requests.post(url,json=json,headers=headersvcd)
        self.assertEqual("成功",updateproject.json()["msg"])

    @classmethod
    def tearDownClass(cls):
        pass



if __name__ == "__main__":
    unittest.main(verbosity=2)