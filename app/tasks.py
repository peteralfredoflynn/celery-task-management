import time

from flask import current_app

from .application import celery


@celery.task(name="say_hello", autoretry_for=(Exception,), retry_backoff=True)
def say_hello(word):
    # if random.choice([1, 0]):
    #     raise Exception("IT BROKE YO!!!")
    current_app.logger.info(f"Hello {word}!")
    time.sleep(10)
    current_app.logger.info(f"Goodbye 10 seconds later")
