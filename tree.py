from node.node_and import node_and

class tree:
    def __init__(self, ext, root_node=None, logger=None):
        self._logger = logger
        self._ext = ext
        if root_node:
            self._root_node = root_node
        else:
            self._root_node = node_and(self._logger)

    def get_ext_option(self):
        return self._ext

    def set_root_node(self, rnode):
        self._root_node = rnode

    def get_root_node(self):
        return self._root_node

    def str(self, tabs=0):
        print('{}{}'.format('  ' * tabs, self._ext))
        self._root_node.str(tabs)

