import requests
import os
import datetime
import yaml
from email.mime.text import MIMEText
import  smtplib
from email.mime.multipart import MIMEMultipart
from email.header import Header

#获取当前路径
file_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
#配置文件路径
config_dir = os.path.join(file_dir+"\config\config_vcd_test.yaml")
with open(config_dir,encoding='utf-8') as f:
    config = yaml.load(f)

#上传图片,返回图片路径
def upload_pic(pic_dir,ss=None):
    url = "https://test.chebufan.cn/vcd/api/open/misc/attachment/upload"
    files = {"file": open(pic_dir, "rb")}
    upload = requests.post(url, files=files)
    pic_url = upload.json()["data"]
    return pic_url


# 取最新测试报告
def new_file(test_dir):
    list = os.listdir(test_dir)
    file_name_path = os.path.join(test_dir,list[-1])
    return  file_name_path

# 发送邮件
def send_email(reportfile):
    file_name = reportfile.split("\\")[-1]
    with open(reportfile, "rb") as f:
        mail_body = f.read()
    now=datetime.datetime.now().strftime("%Y-%m-%d %H%M%S")
    #邮箱发送的服务器、邮箱账号密码、发送人、收件人、主题
    smtpserver = config["smtpserver"]
    user = config["user"]
    password = config["password"]
    sender = config["sender"]
    receiver = config['receiver']
    subject = config["subject"]+now

    # 邮件类型
    msg = MIMEMultipart('mixed')

    #添加邮件正文到msg对象
    msg_html1 = MIMEText(mail_body, 'html', 'utf-8')
    msg.attach(msg_html1)
    #添加邮件附件到msg对象
    msg_html2 = MIMEText(mail_body, 'html', 'utf-8')
    msg_html2.add_header("Content-Disposition","attachment", filename=("utf-8","",file_name))
    # msg_html2['Content-Type'] = 'application/octet-stream'
    # msg_html2['Content-Disposition'] = "attachment; filename='%s'"%(reportfile)
    msg.attach(msg_html2)
    #将发送人添加到msg对象
    msg['From'] = config["msg_from"]
    #将收件人添加到msg对象
    msg['To'] = ";".join(receiver)
    # msg['Date'] = '2021-7-18'
    #将主题添加到msg对象
    msg['Subject'] = Header(subject, 'utf-8')

    # 连接发送邮件
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver, 25)
    smtp.login(user, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()