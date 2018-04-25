from contextlib import contextmanager
import time


@contextmanager
def retry(times=1, sleep=1):
    for i in range(times):
        try:
            yield
        except:
            if i < times - 1:
                time.sleep(sleep)
