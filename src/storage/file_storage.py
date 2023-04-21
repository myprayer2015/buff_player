import codecs
import csv
from ctypes import sizeof

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
    
    def get_name_by_goods_id(self, goods_id):
        if goods_id in goods_map:
            return goods_map[goods_id]
        return 'default_name'

    def get_id_by_goods_info(self, name, exterior = 'wearcategory0', quality = 'normal'):
        for key, value in self.goods_map.items():
            if name in key and (exterior == value[3] or exterior == 'all') and (quality == value[4] or quality == 'all'):
                return value[0]
        return '-1'
    
    def get_ids_by_goods_info(self, names, exteriors, qualitys, internal_names, stattraks):
        id_list = []
        for i in range(len(names)):
            if i >= len(exteriors) or i >= len(qualitys) or i >= len(internal_names) or i >= len(stattraks):
                break
            name_items = []
            exterior_items = []
            quality_items = []
            if '&&' in names[i]:
                name_items = names[i].split('&&')
            else:
                name_items.append(names[i])
            if '&&' in exteriors[i]:
                exterior_items = exteriors[i].split('&&')
            else:
                exterior_items.append(exteriors[i])
            if '&&' in qualitys[i]:
                quality_items = qualitys[i].split('&&')
            else:
                quality_items.append(qualitys[i])
            for key, value in self.goods_map.items():
                name_match_flag = True
                exterior_match_flag = True
                quality_match_flag = True
                internal_name_match_flag = True
                stattrak_match_flag = True
                for item in name_items:
                    if item not in key and item != 'all':
                        name_match_flag = False
                        break
                for item in exterior_items:
                    if item != value[3] and item != 'all':
                        exterior_match_flag = False
                        break
                for item in quality_items:
                    if item != value[4] and item != 'all':
                        quality_match_flag = False
                        break
                if internal_names[i] not in value[2] and internal_names[i] != 'all':
                    internal_name_match_flag = False
                if stattraks[i] != value[5] and stattraks[i] != 'all':
                    stattrak_match_flag = False
                if name_match_flag and exterior_match_flag and quality_match_flag and internal_name_match_flag and stattrak_match_flag:
                    id_list.append(value[0])
        return id_list
    
    def get_id_by_price_scope(self, name, exterior = 'wearcategory0', quality = 'normal', min_price=0, max_price=10000000):
        for key, value in self.goods_map.items():
            if name in key and (exterior == value[3] or exterior == 'all') and (quality == value[4] or quality == 'all') and float(value[6]) >= min_price and float(value[6]) <= max_price:
                return value[0]
        return '-1'