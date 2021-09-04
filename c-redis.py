import pytrader as pt
import pytrader.log as log
import redis

timer = pt.Timer()

logger = log.logging
log.config_root_logger()

redis_host = "localhost"
redis_port = 6379
redis_password = "password"

def hello_redis():
    """Example Hello Redis Program"""

    try:
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
        print(e)


if __name__ == '__main__':
    hello_redis()

timer.report()
