from node.node import node
import pdb

class node_and(node):
    def __init__(self, logger):
        node.__init__(self, logger=logger)
        self._type = 'AND'

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = True
        var.checkpoint()

        _extent = extent.copy()
        _position = position

        reserved = []
        for cnode in self._children:
            while _position < len(text) and text[_position] == ' ':
                _position += 1
            _extent, _position, _pass_fail, _reserved = cnode.process(text,
                    _extent, _position, var, add_extent)
            if not _pass_fail:
                pass_fail = False
                break

        if not pass_fail:
            var.recovery()
        else:
            position = _position
            if add_extent:
                extent.merge(_extent)
            reserved += _reserved

        return extent, position, pass_fail, reserved
