import pymysql
from prestigecsv.config import config, logger


def db_insert(sql_vals):
    """
    Connecting to the MySQL database server
    """
    conn = None
    try:
        # connect to the MySQL server
        logger.debug("Connecting to the MySQL database...")
        conn = db_connect()
        # create a cursor
        cur = conn.cursor()
        # execute a statement
        sql = 'INSERT INTO prop_land (line, file_name) VALUES (%s, %s)'
        cur.executemany(sql, sql_vals)
        # close the communication with the MySQL
        conn.commit()
        logger.debug('Data inserted in DB...')
        cur.close()
    except (Exception, pymysql.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            logger.error('Database connection closed.')


def db_create():
    """
    Creating a table
    :return:
    """
    conn = None
    try:
        # connect to the MySQL server
        conn = db_connect()
        # create a cursor
        cur = conn.cursor()
        # execute a statement to create a table
        sql = """CREATE TABLE IF NOT EXISTS `prop_land` (
              `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
              `line` VARCHAR(1000) NULL,
              `file_name` VARCHAR(250)  NOT NULL default '',
               PRIMARY KEY  (`id`)
            );"""
        cur.execute(sql)
        cur.close()
    except (Exception, pymysql.DatabaseError) as error:
        print("Error in DB", error)
    finally:
        if conn is not None:
            conn.close()
            logger.error('Database connection closed.')


def db_connect():
    """
    Connecting to the MySQL database server
    """
    # read connection parameters
    params = config()
    # connect to the MySQL server
    logger.debug("Connecting to the MySQL database...")
    conn = pymysql.connect(**params)

    return conn
