import time
from functools import wraps

from loguru import logger
from psycopg2 import InterfaceError, OperationalError


def pg_backoff(start_sleep_time=0.1, factor=2, border_sleep_time=10):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (OperationalError, InterfaceError):
                logger.error('Connection lost. Trying to connect...')
                time_to_sleep = start_sleep_time
                is_connected = False
                n = 1
                while not is_connected:
                    try:
                        time.sleep(time_to_sleep)
                        value = func(*args, **kwargs)
                        is_connected = True
                        logger.debug('Connected to DB!')
                        return value
                    except (OperationalError, InterfaceError):
                        logger.error(f'Connection lost. Trying to connect a {n} time.')
                        time_to_sleep = start_sleep_time * factor ** n
                        if time_to_sleep > border_sleep_time:
                            time_to_sleep = border_sleep_time
                        n += 1

        return inner

    return func_wrapper
