import csv
import sys
import os

from glob import glob
from os.path import basename

from prestigecsv.config import BATCH_SIZE, logger, LOG
from prestigecsv.settings import db_insert, db_create


def main(cmd):
    """
    Main entry point
    :param cmd: command line passed args
    :return: None
    """
    print(cmd)
    if len(cmd) == 2 and os.path.isdir(cmd[1]):
        xpath = glob(cmd[1] + '*.csv', recursive=True)
        if len(xpath) == 0:
            logger.debug('No CSV files found...')
        else:
            iter_csv(xpath)
    else:
        logger.debug('Path should be a directory and allowed one input path')


def iter_csv(csv_list):
    """
    Iterating CSV files
    :param csv_list: all csv file list in the folder
    :return:
    """
    for fl in csv_list:
        logger.debug('Parsing a file %s', fl)
        with open(fl) as csvfile:
            read_csv = csv.reader(csvfile, delimiter=',')
            count = 0
            data = []
            for row in read_csv:
                # Ignore empty fields
                data_line = list(filter(lambda elm: elm != '', row))
                # Replace commas and convert String
                data.append((str.join('|', data_line), fl))
                count += 1
                # Reset Inserting every 100 data inserting
                if count % BATCH_SIZE == 0:
                    db_insert(data)
                    data.clear()
                    count = 0

            if len(data) != 0:
                db_insert(data)


if __name__ == "__main__":
    print('LOG file is created in %s', LOG)
    logger.debug('Creating a table structure "prop_land".')
    db_create()
    args = sys.argv
    main(args)
