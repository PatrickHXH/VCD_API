# -*- encoding=utf8 -*-
__author__ = "HXH"

import unittest
import requests
import  time
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
COMMON_DIR = os.path.join(BASE_DIR,"config")
sys.path.append(COMMON_DIR)
from common import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_cxgj,headers_admin_formdata,vpt_header

class Poster_Sharing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global headersvcd
        headersvcd = headers_vcd(13538878368)

        global headersvcz
        headersvcz = headers_vcz(13538878368)
    def test_01(self):
        u'''朋友圈助手—管理端新增海报—v车店可查看'''
        #上传图片
        url = "https://test.chebufan.cn/vcd/api/open/misc/attachment/upload"
        file_dir = os.path.abspath(os.path.dirname((os.path.dirname(__file__))))
        pic_dir = os.path.join(file_dir + "\\testdata\picture.jpg")
        files = {"file": open(pic_dir,"rb") }
        upload = requests.post(url, files=files)
        pic_url = upload.json()["data"]
        type = pic_url.split(".")[-1]
        print("图片路径：",upload.json()["data"])

        #保存海报
        null = None
        url_add = "http://test.chebufan.cn/vcd/api/material/materials/add"
        json  = {
                    "timestamp":1631867067317,
                    "sign":"nosign",
                    "data":{
                        "id":null,
                        "materialName":"自动化测试",
                        "imageUrl":upload.json()["data"],
                        "showOrder":"9999999",
                        "type":0
                    }
                }
        add = requests.post(url_add,json=json,headers=headers_admin())

        #v车店查看朋友圈海报
        url_page = "https://test.chebufan.cn/vcd/api/open/material/materials/page"
        json  = {"data":{"current":1,"size":10,"params":{"types":[0]}},"sign":"nosign","timestamp":1631868626975}
        page = requests.post(url_page,json=json,headers=headersvcd)
        self.assertIn("自动化测试",page.json()["data"]["records"][0]["materialName"])
        self.assertIn("0",str(page.json()["data"]["records"][0]["type"]))

    def test_02(self):
        u'''朋友圈助手—管理端新增海报—筛选—可筛选海报类型'''
        #v车店查看朋友圈海报
        for i in range(1,5):
            url_page = "http://test.chebufan.cn/vcd/api/open/material/materials/page"
            json  = {"data":{"current":1,"size":10,"params":{"types":[i]}},"sign":"nosign","timestamp":1631868626975}
            page = requests.post(url_page,json=json,headers=headersvcd)
            self.assertIn(str(i),str(page.json()["data"]["params"]["types"][0]))

    # def test_03(self):
    #     u'''朋友圈助手—管理端新增海报—保存—可保存海报'''
    #     pass

    # def test_04(self):
    #     u'''朋友圈助手—管理端新增海报—识别—可识别海报小程序并绑定过门店'''
    #     pass
    @classmethod
    def tearDownClass(cls):
        # 删除海报
        null = None
        url_page = "http://test.chebufan.cn/vcd/api/material/materials/page"
        json = {"timestamp":1631869642691,"sign":"nosign","data":{"size":10,"current":1,"params":{"materialName":null,"createTimeStart":null,"createTimeEnd":null},"orders":[]}}
        page = requests.post(url_page,json=json,headers=headers_admin())
        id = page.json()["data"]["records"][0]["id"]

        url_delete = "http://test.chebufan.cn/vcd/api/material/materials/delete"
        json = {"timestamp":1631869642497,"sign":"nosign","data":{"id":id}}
        delete = requests.post(url_delete,json=json,headers=headers_admin())
        # cls.assertEqual("成功",delete.json()["msg"])

if __name__ == "__main__":
    time.sleep(3)
    unittest.main(verbosity=2)