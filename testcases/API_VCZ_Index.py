# -*- encoding=utf8 -*-
__author__ = "HXH"

import random
import unittest
import requests
import string
import os
import sys
path1 = os.path.abspath('API_VCZ_Index')
print(path1)
sys.path.append(path1+"/config/")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
COMMON_DIR = os.path.join(BASE_DIR,"config")
sys.path.append(COMMON_DIR)
from common import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_cxgj,headers_admin_formdata,vpt_header

class Index(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global headersvcz
        headersvcz = headers_vcz(13538878368)


    def test_01(self):
        u'''首页—门店图片—公众号门店端可修改名称/时间/业务/地址/图片'''
        url_update = "https://test.chebufan.cn/vcd/api/open/shop/updateToVpt"
        json = {
                        "data": {
                            "shopName": "hxh_autotest001",
                            "shopUserName": "黄测试",
                            "shopType": 1,
                            "saleIds": "0,7,4,1",
                            "provinceName": "广东省",
                            "cityName": "广州市",
                            "areaName": "增城区",
                            "addressDetail": "中山大道西293号2222",
                            "workTimeStart": "10:03",
                            "workTimeEnd": "21:30",
                            "wifiName": "JXguest3-5G111",
                            "wifiPassword": "Joysim201999",
                            "shopImages": ["https://test.chebufan.cn/vcdfile/modelName/0/434c11e8b02543fb8520fc25d4043b63.jpg"],
                            "workDay": "1,2,3,4,5,6,7",
                            "id": 1361,
                            "shopUserId": 1297,
                            "lat": "23.128488",
                            "lon": "113.370534",
                            "contactPhone": "13538878368",
                            "majorImg": "https://test.chebufan.cn/vcdfile/modelName/0/434c11e8b02543fb8520fc25d4043b63.jpg",
                            "state": 1
                        },
                        "sign": "nosign",
                        "timestamp": 1673405335120
                    }
        update = requests.post(url_update,json=json,headers=headersvcd)
        self.assertIn("成功",update.json()["msg"])

        url_getShopInfo = "http://test.chebufan.cn/vcd/api/cz/shop/getShopInfo"
        getShopInfo = requests.post(url_getShopInfo,json=json,headers=headersvcz)
        self.assertIn("成功",getShopInfo.json()["msg"])


    def test_03(self):
        u'''首页—门店预约—门店可收到预约短信和车主收到微信通知'''

    def test_04(self):
        u'''首页—救援搭电—门店可收到救援短信'''

    def test_05(self):
        u'''首页—门店wifi—可连接门店wifi'''
        url = "https://test.chebufan.cn/vcd/api/cz/shop/ycxRepairWifi/getByShopId"
        json= {"data":{"repairId":"1315"},"sign":"nosign","timestamp":1653529690540}
        resp = requests.post(url,json=json,headers=headersvcz)
        self.assertEqual("成功",resp.json()["msg"])

    def test_06(self):
        u'''首页—分享门店—点击可绑定门店'''
        url = "https://test.chebufan.cn/vcd/api/cz/czuser/czAccountShopRel/bind"
        json = {"data":{"id":"1361"},"sign":"nosign","timestamp":1653531019083}
        resp = requests.post(url,json=json,headers=headersvcz)
        self.assertEqual("成功",resp.json()["msg"])

    def test_07(self):
        u'''首页—导航—可导航（验证接口返回坐标测试）'''
        url = "https://test.chebufan.cn/vcd/api/cz/czuser/czAccountShopRel/getLastShop"
        json = {"data":{"appId":"wx467d93d7f179a217","openId":""},"sign":"nosign","timestamp":1653531652341}
        resp = requests.post(url,json=json,headers=headersvcz)
        print(resp.text)
        self.assertIsNot(None,resp.json()["data"]["longitude"])
        self.assertIsNot(None, resp.json()["data"]["latitude"])
        self.assertIsNot(None, resp.json()["data"]["contactNumber"])

    # def test_08(self):
    #     u'''首页—电话—可拨打电话'''


    @classmethod
    def tearDownClass(cls):
        pass



if __name__ == "__main__":
    unittest.main(verbosity=2)