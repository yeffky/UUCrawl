'''
Author: yeffky
Date: 2025-02-20 10:57:06
LastEditTime: 2025-02-20 11:24:44
'''
import smtplib
from email.mime.text import MIMEText
from email.header import Header

# 发件人邮箱账号和授权码
sender = '1225527169@qq.com'
password = 'wmjflfrfmdobhcjf'

# 收件人邮箱
receivers = '1225527169@qq.com'

# 邮件内容
message = MIMEText('小红书登录过期，请发送验证码用于登录', 'plain', 'utf-8')
message['From'] = sender
message['To'] = receivers

# 邮件主题
subject = '小红书工作流'
message['Subject'] = Header(subject, 'utf-8')

try:
    # 连接 SMTP 服务器
    smtpObj = smtplib.SMTP('smtp.qq.com', 587)
    smtpObj.starttls()
    # 登录发件人邮箱
    smtpObj.login(sender, password)
    # 发送邮件
    smtpObj.sendmail(sender, receivers, message.as_string())
    print("邮件发送成功")
except smtplib.SMTPException as e:
    print(f"邮件发送失败: {e}")
finally:
    # 关闭 SMTP 连接
    smtpObj.quit()