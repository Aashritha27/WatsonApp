import smtplib
fromaddr = 'patentfoxibm@gmail.com'
toaddrs  = 'patentfoxibm@gmail.com'
msg = "\r\n".join([
  "Subject: Patent Fox Team",
  "",
  "Hello email world"
  ])
username = 'patentfoxibm@gmail.com'
password = 'patentfox123'
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(username,password)
server.sendmail(fromaddr, toaddrs, msg)
server.quit()

"""
Allow secure access
https://support.google.com/accounts/answer/6010255
"""