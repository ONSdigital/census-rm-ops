import os


class Config:
    PORT = os.getenv('PORT')  # This is not used in run.py which isn't used in cloudfoundry
    SERVICE_DOMAIN_SUFFIX = os.getenv("SERVICE_DOMAIN_SUFFIX")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")


class CIConfig(Config):
    SERVICE_DOMAIN_SUFFIX = os.getenv("SERVICE_DOMAIN_SUFFIX")


class K8SDevelopmentConfig(Config):
    PORT = os.getenv("PORT", 80)
    USERNAME = os.getenv('USERNAME', "admin")
    PASSWORD = os.getenv('USERNAME', "secret")
    ACTION_SERVICE = os.getenv('ACTION_SERVICE')
    RABBITMQ_HOST = os.getenv('RABBITMQ_SERVICE_HOST')
    RABBITMQ_PORT = os.getenv('RABBITMQ_SERVICE_PORT')
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')
    RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'exampleInboundQueue')
    RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', '')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')


class DevelopmentConfig(Config):
    PORT = os.getenv("PORT", 8003)
    USERNAME = "admin"
    PASSWORD = "secret"
    ACTION_SERVICE = 'http://localhost:8301'
    RABBITMQ_HOST = os.getenv('RABBITMQ_SERVICE_HOST', 'localhost')
    RABBITMQ_PORT = os.getenv('RABBITMQ_SERVICE_PORT', '6672')
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')
    RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'exampleInboundQueue')
    RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', '')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')


class DockerConfig(DevelopmentConfig):
    PORT = 80
    ACTION_SERVICE = 'http://actionscheduler:8301'
    RABBITMQ_HOST = os.getenv('RABBITMQ_SERVICE_HOST', 'rabbitmq')
    RABBITMQ_PORT = os.getenv('RABBITMQ_SERVICE_PORT', '5672')
    RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST', '/')
    RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'exampleInboundQueue')
    RABBITMQ_EXCHANGE = os.getenv('RABBITMQ_EXCHANGE', '')
    RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')


class UnitTestConfig(DevelopmentConfig):
    ACTION_SERVICE = 'http://test'
    RABBITMQ_EXCHANGE = 'test_exchange'
    RABBITMQ_HOST = 'test_host'
    RABBITMQ_PASSWORD = 'test_pass'
    RABBITMQ_PORT = 'test_port'
    RABBITMQ_QUEUE = 'test_queue'
    RABBITMQ_USER = 'test_user'
    RABBITMQ_VHOST = 'test_vhost'
