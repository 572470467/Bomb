import time
import smtplib
import os,sys
import subprocess
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
from_addr = 'lm00609_yy0724@163.com'#发件邮箱
password = 'KADUXJSFRPQPSPHL'#stmp服务密码
to_addr = 'lm00609_yy0724@163.com'#收件邮箱
smtp_server = 'smtp.163.com'#发件服务器
def Send():
    textApart = MIMEText('send by python')#正文
    imageApart = MIMEImage(open('a.scm', 'rb').read(), 'a.scm'.split('.')[-1])
    imageApart.add_header('Content-Disposition', 'attachment', filename='a.scm')
    msg = MIMEMultipart()
    msg.attach(textApart)
    msg.attach(imageApart)
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header('python test')
    server = smtplib.SMTP_SSL()
    server.connect(smtp_server,465)
    server.login(from_addr, password)#登录邮箱
    server.sendmail(from_addr, to_addr, msg.as_string())# 发送邮件
    server.quit()
    print('发送成功')
def Receive():
    result = os.popen('petite a.scm','r')  
    res = result.read()  
    text=res.splitlines()[-1]
    textApart = MIMEText('{}'.format(text))#正文
    msg = MIMEMultipart()
    msg.attach(textApart)
    msg['From'] = Header(from_addr)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header('python test')
    server = smtplib.SMTP_SSL()
    server.connect(smtp_server,465)
    server.login(from_addr, password)#登录邮箱
    server.sendmail(from_addr, to_addr, msg.as_string())# 发送邮件
    server.quit()
    f=open('a.scm','w')
    f.write('(begin(display {})(exit))'.format(text))
    f.close()
    print('接收成功')
if __name__ == '__main__':
    while True:
        time.sleep(0.5)
        Send()
        Receive()
