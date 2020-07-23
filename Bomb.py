import time
import datetime
import smtplib
import imaplib
import os,sys
import subprocess
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header
def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value
def get_header(msg):
    for header in ['From','To','Subject']:
        value = msg.get(header, '')
        if value:
            hdr, addr = parseaddr(value)
            name = decode_str(addr)
            print(header +':'+name)
        return name
def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos+8:].strip()
    return charset
def get_content(msg):
    for part in msg.walk():
        content_type = part.get_content_type()
        charset = guess_charset(part)
        if part.get_filename()!=None:
            continue
        email_content_type = ''
        content = ''
        if content_type == 'text/plain':
            email_content_type = 'text'
        elif content_type == 'text/html':
            continue 
            email_content_type = 'html'
        if charset:
            try:
                content = part.get_payload(decode=True).decode(charset)
            except AttributeError:
                print('type error')
            except LookupError:
                print("unknown encoding: utf-8")
        if email_content_type =='':
            continue
        return content.replace("&nbsp;",' ').replace("&gt;",'>')
def get_file(msg):
    for part in msg.walk():
        filename=part.get_filename()
        if filename!=None:
            filename = decode_str(filename)
            data = part.get_payload(decode = True)
            path=filename
            f = open(path, 'wb')
            f.write(data)
            f.close()
            print(filename,'download')
            return filename
def Send():
    if FileName!=None:
        result = os.popen('guile {}'.format(FileName),'r')  
        res = result.read()  
        text=res.splitlines()[-1]
    else:
        f=open('a.scm','w')
        f.write('{}'.format(get_content(msg)))
        f.close()
        result = os.popen('guile a.scm','r')  
        res = result.read()  
        text=res.splitlines()[-1]
    textApart = MIMEText('{}'.format(text))#正文
    m = MIMEMultipart()
    m.attach(textApart)
    m['From'] = Header(from_addr)
    m['To'] = Header(to_addr)
    m['Subject'] = Header('Results')
    server = smtplib.SMTP_SSL()
    server.connect(smtp_server,465)
    server.login(from_addr, password)#登录邮箱
    server.sendmail(from_addr, to_addr, m.as_string())# 发送邮件
    server.quit()
def Unseen():
    conn=imaplib.IMAP4_SSL('imap.qq.com')
    conn.login(from_addr,password)
    conn.list()
    conn.select('INBOX')
    unseen=conn.search(None,'UNSEEN')
    unseen_list=unseen[1][0].split()
    return conn,unseen_list
if __name__ == '__main__':
    while True:
        time.sleep(0.5)
        smtp_server = 'smtp.qq.com'
        from_addr='572470467@qq.com'
        password='ckffrhvgadghbcgf'
        server=poplib.POP3_SSL('pop.qq.com')
        server.user(from_addr)
        server.pass_(password)
        resp, mails, octets = server.list()
        conn,index=Unseen()
        for i in range(len(index)):
            resp, lines, octets = server.retr(index[i].decode('utf-8'))
            msg_content = b'\r\n'.join(lines).decode('utf-8','ignore')
            msg = Parser().parsestr(msg_content)
            subject=msg['Subject']
            print('Subject'+':'+subject)
            date=msg["Date"]
            to_addr=get_header(msg)
            FileName=get_file(msg)
            Send()
        for num in index:
            typ,y=conn.fetch(num,'(BODY.PEEK[])')
            conn.store(num,'+FLAGS','\Seen')    
        server.quit()
