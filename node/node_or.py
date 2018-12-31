from node.node import node

class node_or(node):
    def __init__(self, logger):
        node.__init__(self, logger=logger)
        self._type = 'OR'

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = False
        reserved = []
        for cnode in self._children:
            _extent, _position, _pass_fail, _reserved = cnode.process(text, extent, position, var)
            if _pass_fail:
                if add_extent:
                    extent.merge(_extent)
                position = _position
                pass_fail = True
                reserved += _reserved
                break
        return extent, position, pass_fail, reserved
