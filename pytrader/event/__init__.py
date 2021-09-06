# encoding: utf-8

import config as cfg
import smtplib
import ssl

print(cfg)

def notify_email(event: str, messages: list, send_from: str = cfg.SMTP['to'], send_to: list = cfg.SMTP['from']):

  msg_body = f'subject: pytrader {event} \n'
  msg_body += "\n\n".join(messages)

  print(msg_body)

  context = ssl.SSLContext(ssl.PROTOCOL_TLS)

  with smtplib.SMTP(cfg.SMTP['host'], cfg.SMTP['port']) as server:
      server.ehlo()
      server.starttls(context=context)
      server.ehlo()
      server.login(cfg.SMTP['user'], cfg.SMTP['password'])
      server.sendmail(send_from, send_to, msg_body)

  # if using gmail to send you will need to enable less secure app access
