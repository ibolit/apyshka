import time


def retry(fn, times=1, sleep=0):
    for i in range(times):
        try:
            return fn()
        except:
            if i == times-1:
                raise
            time.sleep(sleep)
