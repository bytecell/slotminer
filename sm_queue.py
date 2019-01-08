
class queue:
    def __init__(self, maxsize=20):
        self._items = []
    def put(self, x):
        self._items.append(x)
    def get(self):
        if not self._items:
            return None
        ret = self._items[0]
        del(self._items[0])
        return ret
    def glance(self):
        if not self._items:
            return None
        return self._items[0]
    def str(self):
        print('<front>', self._items, '<end>')
