from node.node import node
from node.node_rule_refer import node_rule_refer
import pdb

class node_concat(node):
    def __init__(self, logger):
        node.__init__(self, logger=logger)
        self._type = 'CONCAT'

    def process(self, text, extent, position, var, add_extent=True):
        reserved = []
        pass_fail = True

        _extent = extent.copy()
        _position = position

        value = ''
        for cnode in self._children:
            _extent, _position, _pass_fail, _reserved = \
                    cnode.process(text, _extent, _position, var)
            if not _pass_fail:
                pass_fail = False
                break
            #if isinstance(cnode, node_rule_refer):
            for x in _reserved:
                value += str(x)
            #else:
            #    new_extent = list(set(_extent) - set(extent))
            #    if new_extent:
            #        for b, e in new_extent:
            #            value += text[b:e]

        if pass_fail:
            if add_extent:
                extent.merge(_extent)
            position = _position
            reserved += [value]
        else:
            reserved = []

        return extent, position, pass_fail, reserved

