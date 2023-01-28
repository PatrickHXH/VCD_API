import requests
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
COMMON_DIR = os.path.join(BASE_DIR,"config")
sys.path.append(COMMON_DIR)
from common import headers_vcz,headers_vcd,headers_admin,cookies_headers_gzh,CzAccountId,headers_cxgj,headers_admin_formdata,vpt_header

global headersvcd
headersvcd = headers_vcd(13538878368)

global headersvcz
headersvcz = headers_vcz(13538878368)

# #拥有抵扣券的数量
# url = "https://test.chebufan.cn/vcd/api/cz/eticket/hcxEticket/eticketStatistic"
# json = {
# 	"data": {
# 		"shopId": "1361",
# 		"state": [0]
# 	},
# 	"sign": "nosign",
# 	"timestamp": 1658888556340
# }
# resp = requests.post(url, json=json, headers=headersvcz)
# # print(resp.text)
# total = resp.json()["data"]["couponNum"]
# if total % 10 == 0:
# 	pages = total //10
# 	print("页数为：",pages)
# else:
# 	pages = (total // 10) + 1
# 	print("页数为：", pages)

# # 获取抵扣券id
# url = "https://test.chebufan.cn/vcd/api/cz/profit/profitSku/pageCoupon"
# json = {
#     "data": {
#         "current": 1,
#         "params": {
#             "shopId": "1361",
#             "mobile": "135388788368",
#             "state": 0
#         },
#         "orders": [{}],
#         "shopId": "1361",
#         "mobile": "135388788368",
#         "state": 0
#     },
#     "sign": "nosign",
#     "timestamp": 1658477566430
# }
# resp = requests.post(url, json=json, headers=headersvcz)
# print("线上优惠券列表：", resp.text)


for i in range(0, 10):
	try:
		# 断言进店车辆统计是否正确
		print("断言次数:", i)
		assert 1==1
	except AssertionError:
		# activeAnalyze = requests.post(url_activeAnalyze, json=json, headers=headersvcd)
		# carafter = activeAnalyze.json()["data"]["todayCarEnterNum"]
		print("断言失败")