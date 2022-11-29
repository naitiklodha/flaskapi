

import redis



class ApplicationConfig:
    SECRET_KEY = "Lifeisbitch"


    SESSION_TYPE = "redis"
    SESSION_PERMANENT = True
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")