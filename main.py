from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from retrying import retry


@retry(stop_max_attempt_number=15)
def sendmail(message, recipient_show, to_addrs):
    # 填写真实的发邮件服务器用户名、密码
    user = 'example@example.com'
    password = 'WeakPassw0rd'
    # 邮件内容
    msg = MIMEText(message, 'plain', _charset="utf-8")
    # 邮件主题描述
    msg["Subject"] = 'This is a test subject'
    # 发件人显示，不起实际作用
    msg["from"] = user
    # 收件人显示，不起实际作用
    msg["to"] = recipient_show
    # 抄送人显示，不起实际作用
    msg["Cc"] = ''
    with SMTP_SSL(host="smtp.example.com", port=465) as smtp:
        # 登录发邮件服务器
        smtp.login(user=user, password=password)
        # 实际发送、接收邮件配置
        smtp.sendmail(from_addr=user, to_addrs=to_addrs.split(','), msg=msg.as_string())


if __name__ == '__main__':
    # 将content.txt内的内容作为信息
    with open('content.txt', 'r', encoding='utf-8') as f:
        message = f.read()
    # 逐行读取邮件数据
    with open('emails.txt', 'r', encoding='utf-8') as f:
        emails = f.readlines()
        try:
            # 显示收件人
            sender_show = 'example@example.com'
            for i in emails:
                # 将已发送的邮箱存储在文本中方便发生错误时手动清理数据
                with open('emails_done.txt', 'a', encoding='utf-8') as f:
                    f.write(i)
                sendmail(message, i, i)
        except Exception as e:
            print("The Error happened: " + str(e))


