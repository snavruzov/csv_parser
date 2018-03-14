import logging
from configparser import ConfigParser

# Batch size to bulk inserting data into DB
BATCH_SIZE = 100
# Log file location
LOG = '/tmp/parser.log'
logging.basicConfig(filename=LOG, filemode="w", level=logging.DEBUG)
logger = logging.getLogger(__name__)


def config(filename='database.ini', section='mysql'):
    """
    Database connection configuration properties, gets from INI file
    :param filename: INI file name
    :param section: DB conf tagged section
    :return: Dictionary value
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to mysql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db
