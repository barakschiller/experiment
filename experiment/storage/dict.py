from experiment.storage import ItemAlreadyExistsException

class DictStorage(object):
    def __init__(self):
        self.content = {}
        self.next_id = 0

    def store(self, key, dict_value):
        if key in self.content:
            raise ItemAlreadyExistsException(key)

        self.content[key] = dict_value

    def update(self, key, dict_value):
        if key not in self.content:
            raise ValueError('Item does not exists')
        self.content[key] = dict_value

    def get(self, key):
        if key not in self.content:
            return None
        return self.content[key]

    def delete(self, item_id):
        del self.content[item_id]
