import csv
import os

from common.recordlog import logs
from conf.setting import DIR_BASE


def read_csv_data(file_name):
    """
    读取csv文件数据
    :param file_name:
    :return:
    """
    try:
        with open(os.path.join(DIR_BASE, 'data', file_name), 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            for value in csv_reader:
                print(value)
            # return csv_reader
    except Exception as e:
        logs.error(e)


if __name__ == '__main__':
    print(read_csv_data('test_data.csv'))
