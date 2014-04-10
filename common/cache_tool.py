# coding=utf-8
import os
### 创建一个cache
### 其中cache_id，cache_addr，api_key， secret_key均需通过管理控制台获取
### doc:http://pythondoc.duapp.com/cache.html#id1
from blog import settings
cache = None

class CacheInterface:
    '''
    在开发环境中替代BAE的缓存接口
    '''
    def get(self, key):
        return None
    def set(self, key, val, num=0, other=0):
        return True

def get_cache():
    global cache
    try:
        if os.environ['IN_DJANGO_DEV_MODE']:
            if not cache:
                cache = CacheInterface()
    except:
        pass
    if not cache:
        from bae_memcache import BaeMemcache
        cache_id = ""
        cache_addr = ""
        api_key = ""
        secret_key = ""
        cache = BaeMemcache(cache_id, cache_addr, api_key, secret_key)
    return cache

