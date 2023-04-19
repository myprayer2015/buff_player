import codecs
import csv

from .storage import Storage

class FileStorage(Storage):
    goods_map = {}
    def __init__(self):
        pass

    def connect(self):
        with codecs.open('data/goods_info.csv', 'r', 'gbk', 'ignore') as csvfile:
            csv_reader = csv.reader(csvfile)

            for line in csv_reader:
                self.goods_map[line[1]] = line

    def reload(self):
        with codecs.open('data/goods_info.csv', 'r', 'gbk', 'ignore') as csvfile:
            csv_reader = csv.reader(csvfile)

            for line in csv_reader:
                self.goods_map[line[1]] = line

    def get_id_by_goods_info(self, name, exterior = 'wearcategory0', quality = 'normal'):
        for key, value in self.goods_map.items():
            if name in key and exterior == value[3] and quality == value[4]:
                return value[0]
        return -1