class Storage:
    def __init__(self):
        pass

    def connect(self):
        pass

    def reload(self):
        pass

    def get_name_by_goods_id(self, goods_id):
        pass

    def get_id_by_goods_info(self, name, exterior = 'wearcategory0', quality = 'normal'):
        pass
    
    def get_ids_by_goods_info(self, names, exterior, quality):
        pass

    def get_id_by_price_scope(self, name, exterior = 'wearcategory0', quality = 'normal', min_price=0, max_price=10000000):
        pass