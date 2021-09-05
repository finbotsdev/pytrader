import config as cfg
import smtplib
import ssl

print(cfg)

def notify_email(event: str, messages: list, send_from: str = cfg.SMTP_SEND_FROM, send_to: list = cfg.SMTP_SEND_TO):

  msg_body = f'subject: pytrader {event} \n'
  msg_body += "\n\n".join(messages)

  print(msg_body)

  context = ssl.SSLContext(ssl.PROTOCOL_TLS)

  with smtplib.SMTP(cfg.SMTP_HOST, cfg.SMTP_PORT) as server:
      server.ehlo()
      server.starttls(context=context)
      server.ehlo()
      server.login(cfg.SMTP_USER, cfg.SMTP_PASS)
      server.sendmail(send_from, send_to, msg_body)

  # if using gmail to send you will need to enable less secure app access
