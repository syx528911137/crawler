import redis
import ipproj.settings as settings
r=redis.Redis(host=settings.REDIS_HOST,port=settings.REDIS_PORT)