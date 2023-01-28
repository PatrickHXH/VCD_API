import  unittest
import HTMLTestRunner
import  HTMLTestReportCN
import  datetime
import  os
import sys
import  yaml
# from HwTestReport import HTMLTestReport
from XTestRunner import HTMLTestRunner
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
CONFIG_DIR = os.path.join(BASE_DIR,"config")
sys.path.append(CONFIG_DIR)
from PublicMethod import send_email

#获取当前路径
file_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
#测试报告路径
report_dir = os.path.join(file_dir,"reportfile"+"\\")
#测试脚本路径
testcases_dir = os.path.join(file_dir,"testcases")


if __name__ == '__main__':
    #存放测试文件夹的路径
    case_path = testcases_dir
    #创建测试套件
    suite = unittest.TestSuite()
    case_list = []
    #遍历测试文件夹，查找带.py结尾的文件，添加至列表
    for dirpath,dirname,filename in os.walk(case_path):
        for file in filename:
            if file.endswith(".py") and not file.startswith("__") and  file.startswith("API"):
                print(file)
                case_list.append(file)
    for case in case_list:
        discover = unittest.defaultTestLoader.discover(start_dir=case_path, pattern=case)
        suite.addTest(discover)
    # 测试时间
    now = datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")
    reportfile = report_dir+"VCD_API_testReport.html"
    print(reportfile)
    file = open(reportfile,'wb')
    # runner = HTMLTestReport(stream=file,title='车不凡接口测试报告',description='主功能流程接口测试',tester='黄侠瀚')
    runner = HTMLTestRunner(stream=file,title='V车店API接口测试报告',description='主功能流程接口测试',tester='黄侠瀚',language='zh-CN')
    runner.run(suite,rerun=3,save_last_run=True)
    file.close()
    #发送邮件
    send_email(reportfile)
    #清空活动摊位
    obj = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(obj, "testcases", "CLOSE_PROFIT_SKU.py")
    os.system(f'python {path}')



