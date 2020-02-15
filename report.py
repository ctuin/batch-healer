# -*- coding: UTF-8 -*-
# ======== Ctuin ========
# Author: SkEy & Xiao_Jin

import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # 设置服务器
mail_user = "xxxxxxxx"  # 用户名
mail_pass = "xxxxxxxx"  # 密码

sender = '自己填'
receivers = ['自己填']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

mail_msg = """
<h2 style="text-align: center">您的节点不再可用</h2>
<p>节点名称：%s</p>
"""
message = MIMEText(mail_msg, 'html', 'utf-8')
message['From'] = Header("Batch-Healer", 'utf-8')
message['To'] = Header("您", 'utf-8')

subject = '您的节点不再可用'
message['Subject'] = Header(subject, 'utf-8')

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
    smtpObj.login(mail_user, mail_pass)
    smtpObj.sendmail(sender, receivers, message.as_string())
    print ("邮件发送成功")
except smtplib.SMTPException:
    print ("Error: 无法发送邮件")

