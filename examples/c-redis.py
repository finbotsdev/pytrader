# encoding: utf-8

import pytrader as pt
from pytrader.log import logger
import redis
import traceback



"""
c-hello.py
---------------------
pytrader function template
"""


def main(args):
  print(args)

  try:
    logger.info('doing a thing')

    redis_host = "localhost"
    redis_port = 6379
    redis_password = "password"

    # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
    # using the default encoding utf-8.  This is client specific.
    r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)

    logger.info('set values in redis')
    r.set("msg:hello", "Hello Redis!!!")
    r.set("msg:goodbuy", "Redis was a good purchase!!!")

    logger.info('get values from redis')
    print(r.get("msg:hello"))
    print(r.get("msg:goodbuy"))

  except Exception as e:
    logger.error(e)
    print(e)
    print(traceback.format_exc())


if __name__ == '__main__':
  parser = pt.ArgumentParser()
  parser.add_argument("-v", "--verbose", action='store_true', help="verbose")
  args = parser.parse_args()

  timer = pt.Timer()
  logger.info(f'pytrader {__file__}')
  main(args)
  timer.report()
