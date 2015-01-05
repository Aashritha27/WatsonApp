import smtplib

def send_mail(usr,pss,fromaddr, toaddr, msg):
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.ehlo()
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddr, msg)
    server.quit()

if __name__ == "__main__":
    fromaddr = 'patentfoxibm@gmail.com'
    toaddr  = 'oski@berkeley.edu'
    msg = "\r\n".join([
      "Subject: Patent Fox Team",
      "",
      "Hello email world"
      ])

    username = 'patentfoxibm@gmail.com'
    password = 'patentfox123'
    send_mail(username,password,fromaddr,toaddr,msg)

"""
Allow secure access
https://support.google.com/accounts/answer/6010255
"""
