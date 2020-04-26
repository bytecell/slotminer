from node.node import node

class node_pass(node):
    def __init__(self, logger):
        node.__init__(self, logger=logger)
        self._type = 'PASS'

    def process(self, text, extent, position, var, add_extent=True):
        if self.num_child() != 1:
            if self._logger:
                self._logger.error('invalid # of children for node_pass')
            _extent = extent
            _position = position
            reserved = []
            pass_fail = False
        else:
            _extent, _position, pass_fail, reserved = self._children[0].process(text, extent, position, var)
        return _extent, _position, pass_fail, reserved

