import logging
import random
import sys
import time
import traceback

import redis

from angeltools.StrTool import get_domain
from . import get_uri_info


class RedisConnect:
    def __init__(self, db: int = None, connect_params: dict = None):
        """
        操作本地 redis
        """
        REDIS_URI, REDIS_USER, REDIS_PASS, REDIS_HOST, REDIS_PORT, REDIS_DB = get_uri_info(
            "REDIS_URI", default_uri="redis://localhost:6379/1", uri_only=False
        )
        self.params = {
            "decode_responses": True,
            "host": REDIS_HOST,
            "port": REDIS_PORT,
            "password": REDIS_PASS,
        }
        if connect_params:
            self.params.update(connect_params)
        self.params.update({"db": db or 0})

    def cli(self):
        try:
            return redis.Redis(**self.params)
        except Exception as E:
            exc_type, exc_value, exc_obj = sys.exc_info()
            err = traceback.format_exc(limit=10)
            log = logging.Logger("MULTI_WORKER")
            log.error(f"error in connect to redis: ({str(self.params)}):\n{E}\n\n{err}")

    def del_keys(self, pattern):
        if not pattern:
            return
        cli = redis.Redis(**self.params)
        keys = cli.keys(pattern)
        if not keys:
            return
        pl = cli.pipeline()
        temp = [pl.delete(key) for key in keys]
        pl.execute()

    def del_hkeys(self, name, key_list: list):
        if not name or not key_list:
            return
        cli = self.cli()
        cli.hdel(name, *key_list)

    def keys(self, pattern):
        if not pattern:
            return
        return redis.Redis(**self.params).keys(pattern)

    def set_values(self, key_pattern, return_dic=True):
        if not key_pattern:
            return
        keys = self.keys(key_pattern)

        values = list()
        values_dic = dict()
        pipe = self.cli().pipeline()
        for key in keys:
            value = pipe.get(key)
            values.append(value)
            values_dic[key] = value
        return values if not return_dic else values_dic

    def hash_values(self, name_pattern, first=False):
        cli = self.cli()
        all_keys = cli.keys(name_pattern)

        if not first:
            res = dict()
            for k in all_keys:
                h_map = cli.hgetall(k)
                res[k] = h_map
            return res
        else:
            if all_keys:
                return cli.hgetall(all_keys[0])
            else:
                return {}

    def wait(self, url, time_range: list = None):
        """
        实现分布式等待器，用于分布式爬虫爬取等待
        :param url:
        :param time_range:  随机时间列表  [start, end]
        :return:
        """
        domain = get_domain(url)

        time_range = [10, 30] if not time_range else time_range
        wait_time = random.randint(*time_range)

        req_key = f"req_{domain}"
        cli = self.cli()
        last_req_time = cli.hget(req_key, domain)
        if last_req_time:
            while not (int(time.time()) - int(last_req_time)) >= wait_time:
                time.sleep(1)
        cli.hset(req_key, domain, str(int(time.time())))
        return True


if __name__ == "__main__":
    pass

