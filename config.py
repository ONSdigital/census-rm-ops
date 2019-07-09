import os


class Config:
    PORT = os.getenv('PORT')  # This is not used in run.py which isn't used in cloudfoundry
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    ACTION_SERVICE = os.getenv('ACTION_SERVICE')
    RABBITMQ_HOST = os.getenv('RABBITMQ_SERVICE_HOST')
    RABBITMQ_PORT = os.getenv('RABBITMQ_SERVICE_PORT')
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST')
    RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE')
    RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
    RABBITMQ_UNADDRESSED_QID_QUEUE = os.getenv('RABBITMQ_UNADDRESSED_QID_QUEUE')


class K8SDevelopmentConfig(Config):
    PORT = os.getenv("PORT", 80)
    USERNAME = os.getenv('USERNAME', "admin")
    PASSWORD = os.getenv('USERNAME', "secret")
    ACTION_SERVICE = os.getenv('ACTION_SERVICE')
    RABBITMQ_HOST = os.getenv('RABBITMQ_SERVICE_HOST', 'localhost')
    RABBITMQ_PORT = os.getenv('RABBITMQ_SERVICE_PORT', '6672')
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')
    RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'case.sample.inbound')
    RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', '')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
    RABBITMQ_UNADDRESSED_QID_QUEUE = os.getenv('RABBITMQ_UNADDRESSED_QID_QUEUE', 'unaddressedRequestQueue')


class DevelopmentConfig(Config):
    PORT = os.getenv("PORT", 8003)
    USERNAME = "admin"
    PASSWORD = "secret"
    ACTION_SERVICE = 'http://localhost:8301'
    RABBITMQ_HOST = os.getenv('RABBITMQ_SERVICE_HOST', 'localhost')
    RABBITMQ_PORT = os.getenv('RABBITMQ_SERVICE_PORT', '6672')
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')
    RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'case.sample.inbound')
    RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', '')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
    RABBITMQ_UNADDRESSED_QID_QUEUE = os.getenv('RABBITMQ_UNADDRESSED_QID_QUEUE', 'unaddressedRequestQueue')


class DockerConfig(DevelopmentConfig):
    PORT = 80
    ACTION_SERVICE = 'http://actionscheduler:8301'
    RABBITMQ_HOST = os.getenv('RABBITMQ_SERVICE_HOST', 'rabbitmq')
    RABBITMQ_PORT = os.getenv('RABBITMQ_SERVICE_PORT', '5672')


class UnitTestConfig(DevelopmentConfig):
    ACTION_SERVICE = 'http://test'
    RABBITMQ_EXCHANGE = 'test_exchange'
    RABBITMQ_HOST = 'test_host'
    RABBITMQ_PASSWORD = 'test_pass'
    RABBITMQ_PORT = 'test_port'
    RABBITMQ_QUEUE = 'test_queue'
    RABBITMQ_USER = 'test_user'
    RABBITMQ_VHOST = 'test_vhost'
    RABBITMQ_UNADDRESSED_QID_QUEUE = 'testUnaddressedRequestQueue'
