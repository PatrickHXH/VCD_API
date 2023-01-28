import pymysql
import requests
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
COMMON_DIR = os.path.join(BASE_DIR,"config")
sys.path.append(COMMON_DIR)
from common import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_cxgj,headers_admin_formdata,vpt_header

headersvcd = headers_vcd(13538878368)

class closeprofit:
    # 连接数据库
    conn = pymysql.connect(host="121.201.18.86", port=3325, user="root", passwd="Joysim!@#832727", db="cbf")
    # 创建游标
    cur = conn.cursor()
    sql = "SELECT sku_id FROM tb_profit_sku_stall WHERE shop_id=1361"
    # 执行游标
    cur.execute(sql)
    obj = cur.fetchall()
    print(len(obj))

    for i in range(0,len(obj)):
        id = obj[i][0]
        print(id)
        #关闭摊位
        url_updateProfitSkuStall = "https://test.chebufan.cn/vcd/api/open/profit/sku/updateProfitSkuStall"
        json = {"data": {"skuId": id, "stall": 3, "state": 0}, "sign": "nosign", "timestamp": 1634697550119}
        updateProfitSkuStall = requests.post(url_updateProfitSkuStall, json=json, headers=headersvcd)
        print(updateProfitSkuStall.text)


print(".....关闭所有活动摊位.....")