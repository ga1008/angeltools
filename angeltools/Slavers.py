import logging
import os
import sys
import threading
import traceback
from multiprocessing import Pool as Mpp
from multiprocessing.dummy import Pool as ThreadPool

import tqdm
from tqdm.contrib.concurrent import process_map, thread_map


class MWT(threading.Thread):
    def __init__(self, function, params):
        threading.Thread.__init__(self)
        self.func = function
        self.params = params

    def run(self):
        try:
            return self.func(**self.params)
        except Exception as E:
            exc_type, exc_value, exc_obj = sys.exc_info()
            err = traceback.format_exc(limit=10)
            log = logging.Logger('MULTI_WORKER')
            log.error(f"error in running thread: ({str(self.func)}):\n{E}\n\n{err}")


class FakeSlaves:
    """
    for 循环执行任务，作为Slaves或BigSlaves的临时替代
    """
    timespan = 0

    def __init__(self, workers=None, with_tq=False, name=None):
        self.workers = workers
        self.with_tq = with_tq
        self.name = name

    def _say_name(self, func_name=None):
        if self.name:
            if isinstance(self.name, str):
                mission_name = self.name
            else:
                mission_name = func_name
            print(f"FakeSlaves start working: {mission_name}")

    def work(self, func, params_list: list, default=None, list_flat=False, remove_item_if_empty=False):
        start_time = time.time()
        func_name = func.__name__
        self._say_name(func_name=func_name)
        try:
            if self.with_tq:
                tq = tqdm.tqdm(total=len(params_list))
                res_data = self.map_list(func, params_list, tq=tq)
                tq.close()
            else:
                res_data = self.map_list(func, params_list)

            if list_flat and isinstance(res_data, list) and isinstance(res_data[0], list):
                if remove_item_if_empty:
                    res_data = [item for sublist in res_data for item in sublist if item]
                else:
                    res_data = [item for sublist in res_data for item in sublist]

            end_time = time.time()
            self.timespan = round(end_time - start_time, 2)
            return res_data

        except Exception as E:
            exc_type, exc_value, exc_obj = sys.exc_info()
            err = traceback.format_exc(limit=10)
            log = logging.Logger('FakeSlaves')
            log.error(f"error in FakeSlaves: ({str(func)}):\n{E}\n\n{err}")

            end_time = time.time()
            self.timespan = round(end_time - start_time, 2)
            return default

    def map_list(self, func, params_list: list, tq=None):
        func_name = func.__name__
        res_list = list()
        for data in params_list:
            try:
                res_list.append(func(data))
                if tq:
                    tq.update()
            except Exception as E:
                exc_type, exc_value, exc_obj = sys.exc_info()
                err = traceback.format_exc(limit=10)
                log = logging.Logger('FakeSlaves')
                log.error(f"error in FakeSlaves: ({func_name}):\n{E}\n\n{err}")
                res_list.append(E)
        return res_list


class Slaves:
    """
    多线程工具
    """
    timespan = 0

    def __init__(self, workers=None, with_tq=False, name=None):
        """
        :param workers:     线程数
        :param with_tq:     使用tqdm
        :param name:        任务名称
        """
        self.pool = ThreadPool(workers if workers else 10)
        self.with_tq = with_tq
        self.workers = workers
        self.name = name

    def _say_name(self, func_name=None):
        if self.name:
            if isinstance(self.name, str):
                mission_name = self.name
            else:
                mission_name = func_name
            print(f"Slaves start working: {mission_name}")

    def work(self, func, params_list: list, default=None, list_flat=False, remove_item_if_empty=False):
        start_time = time.time()
        func_name = func.__name__
        self._say_name(func_name=func_name)
        try:

            if self.with_tq:
                res_data = thread_map(func, params_list, max_workers=self.workers)
            else:
                res_data = self.pool.map(func, params_list)
            if list_flat and isinstance(res_data, list) and isinstance(res_data[0], list):
                if remove_item_if_empty:
                    res_data = [item for sublist in res_data for item in sublist if item]
                else:
                    res_data = [item for sublist in res_data for item in sublist]

            end_time = time.time()
            self.timespan = round(end_time - start_time, 2)
            return res_data

        except Exception as E:
            exc_type, exc_value, exc_obj = sys.exc_info()
            err = traceback.format_exc(limit=10)
            log = logging.Logger('Slaves')
            log.error(f"error in Slaves: ({func_name}):\n{E}\n\n{err}")

            end_time = time.time()
            self.timespan = round(end_time - start_time, 2)
            return default


class BigSlaves:
    """
    多进程工具
    """
    timespan = 0

    def __init__(self, workers=None, with_tq=False, name=None):
        """
        :param workers:     进程数，默认可用进程-1
        :param with_tq:     使用 tqdm
        :param name:        任务名
        """
        ava_sys_cpu = os.cpu_count() - 1
        workers = workers if workers else ava_sys_cpu
        if workers > ava_sys_cpu:
            workers = ava_sys_cpu

        self.with_tq = with_tq
        self.workers = workers
        self.name = name

    def _say_name(self, func_name=None):
        if self.name:
            if isinstance(self.name, str):
                mission_name = self.name
            else:
                mission_name = func_name
            print(f"BigSlaves start working: {mission_name}")

    def work(self, func, params_list: list, default=None, list_flat=False, remove_item_if_empty=False):
        start_time = time.time()
        func_name = func.__name__
        self._say_name(func_name=func_name)

        try:
            if self.with_tq:
                res_data = process_map(func, params_list, max_workers=self.workers, chunksize=1000)
            else:
                pool = Mpp(self.workers)
                res_data = pool.map(func, params_list)

            if list_flat and isinstance(res_data, list) and isinstance(res_data[0], list):
                if remove_item_if_empty:
                    res_data = [item for sublist in res_data for item in sublist if item]
                else:
                    res_data = [item for sublist in res_data for item in sublist]

            end_time = time.time()
            self.timespan = round(end_time - start_time, 2)
            return res_data

        except Exception as E:
            exc_type, exc_value, exc_obj = sys.exc_info()
            err = traceback.format_exc(limit=10)
            log = logging.Logger('BigSlaves')
            log.error(f"error in BigSlaves: ({func_name}):\n{E}\n\n{err}")

            end_time = time.time()
            self.timespan = round(end_time - start_time, 2)
            return default


def test(num):
    return num * num


def test_main():
    import time
    t0 = time.time()
    test_list = list(range(100))
    result = Slaves(4).work(test, test_list)
    t1 = time.time()
    print(result)
    print(t1 - t0)

    t2 = time.time()
    tl = []
    tl_append = tl.append
    for i in test_list:
        tl_append(i * i)
    t3 = time.time()
    print(tl)
    print(t3 - t2)


if __name__ == '__main__':
    import time
    import random

    def do_add(args):
        x, y = args
        time.sleep(random.randint(1, 2))
        return [x + y]

    test_data = [[x0, y0] for x0, y0 in zip(range(10, 20), range(1, 10))]
    ts = time.time()
    test_slave = Slaves()
    results = test_slave.work(do_add, params_list=test_data, list_flat=True)
    print(results, test_slave.timespan, round(time.time() - ts, 2))
