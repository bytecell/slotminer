import pdb

class node:
    def __init__(self, logger):
        self._indexing_keys = set()
        self._children = []
        self._attr = dict()
        self._type = None
        self._logger = logger
    
    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = True
        reserved = []
        return extent, position, pass_fail, reserved

    def add_child(self, new_node):
        self._children += [new_node]

    def num_child(self):
        return len(self._children)

    def get_type(self):
        return self._type

    def str(self, tabs=0):
        attrs = ''
        for k, v in self._attr.items():
            attrs += ('{}={} '.format(k, v))
        me = '{}[{}] {}'.format('   ' * tabs, self._type, attrs)
        print(me)
        for c in self._children:
            if isinstance(c, node):
                c.str(tabs+1)
                
