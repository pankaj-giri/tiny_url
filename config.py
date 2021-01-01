from cassandra.cqlengine import connection
from cassandra.cluster import Cluster
import traceback


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'

#Wrap each config inside a method to create
#only the required configurations, else all config objects
#are created as soon as the file is loaded
def create_prod_cfg():
    print('Creating prod config')
    class ProductionConfig(Config):
        connection.setup(['52.207.84.19'], 'cqlengine', protocol_version=3)
        cluster = Cluster()
        session = cluster.connect()
        DEBUG = True    
    return ProductionConfig

def create_dev_cfg():
    print('Creating dev config')
    class DevelopmentConfig(Config):
        # traceback.print_stack()
        # connection.setup(['172.17.0.1'], 'cqlengine', protocol_version=3)
        connection.setup(['127.0.0.1'], 'cqlengine', protocol_version=3)
        cluster = Cluster()
        session = cluster.connect()
        DEBUG = True
    return DevelopmentConfig

def create_test_cfg():
    print('Creating test config')
    class TestingConfig(Config):
        TESTING = True
    return TestingConfig


def create_config(environment):
    if environment == 'development':
        return create_dev_cfg()
    elif environment == 'testing':
        return create_test_cfg()
    elif environment == 'production':
        return create_prod_cfg()
    else:
        return create_prod_cfg()