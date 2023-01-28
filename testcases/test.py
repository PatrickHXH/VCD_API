import paramiko
import sys

hostname = ""  # 业务主机ip
username = ""
password = ""

blip = ""  # 堡垒机ip
bluser = ""
blpasswd = ""

port = 8080
login = 'login: '  # telnet 登陆输入用户名
passinfo = 'Password: '  # 登陆输入密码时的前缀
paramiko.util.log_to_file('syslogin.log')   # 将信息放到日志中

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname="121.201.18.86", username="huangxiahan", password="Q123!@#0Oo")  # 堡垒机连接

# new session
channel = ssh.invoke_shell()
channel.settimeout(20)

buff = ''
resp = ''
channel.sendall('telnet ' + hostname + '\n')  # 发送ssh root@192.168.5.45
while not buff.endswith(login):  # 是否以字符串 'login' 结尾
    try:
        resp = channel.recv(9999)
    except Exception as e:
        print('Error info:%s 连接超时.' % (str(e)))
        channel.close()
        ssh.close()
        sys.exit()
    buff += resp.decode()
channel.send('root' + '\n')  # 发送用户名
buff = ''
while not buff.endswith(passinfo):  # 是否以字符串 'password 结尾
    try:
        resp = channel.recv(9999)  #
    except Exception as e:
        print('Error info:%s 连接超时.' % (str(e)))
        channel.close()
        ssh.close()
        sys.exit()
    buff += resp.decode()   # 获取的resp是bytes类型，测试的时候一直报错，最后才发现这个原因
    if not buff.find('yes/no') == -1:  # 模拟登陆是输入yes
        channel.sendall('yes\n')
        buff = ''
channel.send('123456' + '\n')  # 发送密码

buff = ''
while not buff.endswith('# '):
    resp = channel.recv(9999)
    if not resp.decode().find(passinfo) == -1:
        print('Error info: 认证失败.')
        channel.close()
        ssh.close()
        sys.exit()
    buff += resp.decode()
# 通过循环实现连续输入
while True:
    ml = input('请输入命令:')
    channel.sendall(ml + '\n')  # 发送测试命令
    buff = ''
    try:
        while buff.find('# ') == -1:
            resp = channel.recv(9999)
            buff += resp.decode()
    except Exception as e:
        print("错误:" + str(e))
    print(buff)
channel.close()
ssh.close()