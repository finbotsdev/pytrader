# encoding: utf-8

import json
import pytrader.config as cfg
import smtplib
import ssl

print(cfg)

SMTP = {
  'host': cfg.get('SMTP_HOST'),
  'password': cfg.get('SMTP_PASS'),
  'port': cfg.get('SMTP_PORT'),
  'user': cfg.get('SMTP_USER'),
  'from': cfg.get('SMTP_SEND_FROM'),
  'to': json.loads(cfg.get('SMTP_SEND_TO')),
}

def notify_email(event: str, messages: list, send_from: str = SMTP['to'], send_to: list = SMTP['from']):

  msg_body = f'subject: pytrader {event} \n'
  msg_body += "\n\n".join(messages)

  print(msg_body)

  context = ssl.SSLContext(ssl.PROTOCOL_TLS)

  with smtplib.SMTP(SMTP['host'], SMTP['port']) as server:
      server.ehlo()
      server.starttls(context=context)
      server.ehlo()
      server.login(SMTP['user'], SMTP['password'])
      server.sendmail(send_from, send_to, msg_body)

  # if using gmail to send you will need to enable less secure app access
