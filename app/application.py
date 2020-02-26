import os

from celery import Celery
from flask import Flask

celery = Celery()


def create_flask_app():
    app = Flask(__name__)
    _set_configuration(app)
    _set_routes(app)
    make_celery(app)
    return app


def make_celery(app=None):
    """
    Configuration
    https://docs.celeryproject.org/en/stable/userguide/configuration.html
    :param app:
    :return:
    """
    app = app or create_flask_app()
    celery.conf.update(
        dict(
            broker_url=app.config["CELERY_BROKER_URL"],
            backend=app.config["CELERY_BACKEND"],
            task_routes={
                "tasks.say_hello": {"queue": "celery"},
            },
            task_annotations={"*": {"rate_limit": "1/s"}},
            imports=(
                "app.tasks",
            ),
            # worker_hijack_root_logger=False,
            # don't store results, as not to clog redis db
            task_ignore_result=True,
        )
    )
    celery.conf.update(app.config)

    # https://flask.palletsprojects.com/en/1.1.x/patterns/celery/
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask

    return celery


def _set_configuration(app):
    # Redis
    app.config['REDIS_HOST'] = os.environ.get("REDIS_HOST", "localhost")
    app.config['REDIS_PORT'] = os.environ.get("REDIS_PORT", "6379")
    # RabbitMQ
    app.config['RABBIT_USER'] = os.environ.get("RABBIT_USER", "guest")
    app.config['RABBIT_PASSWORD'] = os.environ.get("RABBIT_PASSWORD", "guest")
    app.config['RABBIT_HOST'] = os.environ.get("RABBIT_HOST", "localhost")
    app.config['RABBIT_PORT'] = os.environ.get("RABBIT_PORT", "5672")
    app.config['RABBIT_VHOST'] = os.environ.get("RABBIT_VHOST", "/")
    # Celery
    app.config['CELERY_BACKEND_REDIS_DB'] = os.environ.get("CELERY_BACKEND_REDIS_DB", 1)
    app.config[
        'CELERY_BROKER_URL'] = f"amqp://{app.config['RABBIT_USER']}:{app.config['RABBIT_PASSWORD']}@{app.config['RABBIT_HOST']}:{app.config['RABBIT_PORT']}/{app.config['RABBIT_VHOST']}"
    app.config[
        'CELERY_BACKEND'] = f"redis://{app.config['REDIS_HOST']}:{app.config['REDIS_PORT']}/{app.config['CELERY_BACKEND_REDIS_DB']}"
    return app


def _set_routes(app):
    @app.route('/')
    def hello_world():
        return "Hello Worlds"

    @app.route('/redis')
    def hello_redis():
        from flask import current_app
        import redis
        redis_cache = redis.Redis(
            host=current_app.config["CACHE_REDIS_HOST"], port=current_app.config["CACHE_REDIS_PORT"]
        )
        value = redis_cache.incr("hits")
        current_app.logger.info("HELLO")
        return "Hello Redis Visitor {}".format(value)

    @app.route('/task')
    def task():
        from .tasks import say_hello
        from flask import current_app
        current_app.logger.info("TEST TEST TEST")
        result = say_hello.delay("BOBO")
        return "Task Fired {}".format(result)

    return app
