
import redis

class RedisCache(object):

    redis_con = redis.StrictRedis(host='localhost', port=6379, db=0)

    @classmethod
    def openConnection(cls):
        cls.redis_con = redis.StrictRedis(host='localhost', port=6379, db=0)

    @classmethod
    def setVal(cls, key, val):
        try:
            if cls.redis_con is not None:
                cls.redis_con.set(key,val)
            return True
        except:
            cls.openConnection()
            return False

    @classmethod
    def getVal(cls, key):
        try:
            if cls.redis_con is not None:
                return cls.redis_con.get(key)
        except:
            cls.openConnection()
            return False

    @classmethod
    def setExpiry(cls,key,time):
        try:
            if cls.redis_con is not None:
                return cls.redis_con.expiry(key,time)
        except:
            cls.openConnection()
            return False

    @classmethod
    def incrVal(cls,key):
        try:
            if cls.redis_con is not None:
                return cls.redis_con.incr(key)
        except:
            cls.openConnection()
            return False



