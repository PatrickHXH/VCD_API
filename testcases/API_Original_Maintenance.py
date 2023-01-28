# -*- encoding=utf8 -*-
__author__ = "HXH"

import unittest
import requests
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
COMMON_DIR = os.path.join(BASE_DIR,"config")
sys.path.append(COMMON_DIR)
from common import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_cxgj,headers_admin_formdata,vpt_header


class Original_Maintenance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global headersvcz
        headersvcz = headers_vcz(13538878368)

    def test_01(self):
        u''' 原厂保养—识别—可手动或拍照识别vin码'''
        #上传图片
        url = "https://test.chebufan.cn/vcd/api/open/misc/attachment/upload"
        file_dir = os.path.abspath(os.path.dirname((os.path.dirname(__file__))))
        pic_dir = os.path.join(file_dir + "\\testdata\VIN.jpg")
        files = {"file": open(pic_dir,"rb") }
        upload = requests.post(url, files=files)
        pic_url = upload.json()["data"]
        #识别vin
        url = "https://test.chebufan.cn/vcd/api/open/misc/ocr/vin"
        json = {"data":{"imgPath":pic_url},"sign":"nosign","timestamp":1652693508386}
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertIn("成功",resp.json()["msg"])

    def test_02(self):
        u''' 原厂保养—查询—可查询车型数据和保养手册且正确'''
        url_model= "http://test.chebufan.cn/vcd/api/open/car/maintenance/model"
        json = {"data":{"vinCode":"WBA8X310XHG836526","type":1},"sign":"nosign","timestamp":1634784527945}
        model = requests.post(url_model,json=json,headers=headersvcd)
        try:
            self.assertIn("成功",model.json()["msg"])
        except AssertionError:
            self.assertEqual("未找到车型数据", model.json()["msg"])

    def test_03(self):
        u''' 原厂保养—查询—保养建议—可查询保养建议且正确（待完善）'''
        url_suggest = "http://test.chebufan.cn/vcd/api/open/car/maintenance/suggest"
        json = {"data":{"vin":"WBA8X310XHG836526","vehicleId":"AP_4028b2b65754f3ce0157a2dfce955214","mileage":"666"},"sign":"nosign","timestamp":1634788062211}
        suggest = requests.post(url_suggest,json=json,headers=headersvcd)
        print(suggest.text)
        try:
            self.assertIn("成功",suggest.json()["msg"])
        except AssertionError:
            self.assertEqual("暂无该车保养信息", resp.json()["msg"])


    def test_04(self):
        u''' 原厂保养—列表—显示近期查询且正确'''
        url_page = "http://test.chebufan.cn/vcd/api/open/car/carMaintenanceLog/page"
        json = {"data":{"current":1,"size":10,"params":{},"total":1},"sign":"nosign","timestamp":1634784540193}
        page = requests.post(url_page,json=json,headers=headersvcd)
        self.assertEqual(str(1460164047535812609),page.json()["data"]["records"][0]["id"])

    def test_05(self):
        u''' 原厂保养—列表—全部—显示全部查询记录且正确'''
        url_carMaintenanceLog_page = "https://test.chebufan.cn/vcd/api/open/sys/sysUser/shopUser"
        json = {"data":{"shopId":"1361"},"sign":"nosign","timestamp":1639972218228}
        carMaintenanceLog_page = requests.post(url_carMaintenanceLog_page,json=json,headers=headersvcd)
        # print(carMaintenanceLog_page.text)
        self.assertIn("成功",carMaintenanceLog_page.json()["msg"])

    def test_06(self):
        u''' 原厂保养—套餐购买—可购买套餐（测试调起支付接口）'''
        #获取套餐id
        url = "https://test.chebufan.cn/vcd/api/shop/shopVipCombo/list"
        json = {"data":{},"sign":"nosign","timestamp":1652778864451}
        resp = requests.post(url,json=json,headers=headersvcd)
        id = resp.json()["data"][0]["id"]
        #调起支付
        url = "https://test.chebufan.cn/vcd/api/open/shop/shopVip/pay"
        json = {"data":{"payMoney":0.01,"months":1,"comboName":"1个月","comboId":id},"sign":"nosign","timestamp":1652778867143}
        resp = requests.post(url,json=json,headers=headersvcd)
        self.assertIn("成功", resp.json()["msg"])



    def test_07(self):
        u''' 原厂保养—套餐购买—记录—可查看购买记录'''
        url_paylist = "http://test.chebufan.cn/vcd/api/open/shop/shopVipPayment/page"
        json = {"data":{"current":1,"size":10,"params":{},"total":1},"sign":"nosign","timestamp":1634795989811}
        paylist = requests.post(url_paylist,json=json,headers=headersvcd)
        self.assertIn("成功",paylist.json()["msg"])

    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == "__main__":
    unittest.main(verbosity=2)