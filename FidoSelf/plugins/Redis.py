import redis

DB = redis.Redis('127.0.0.1', 6379, decode_responses=True)
