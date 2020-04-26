from node.node import node
import pdb

class node_plus(node):
    def __init__(self, logger):
        node.__init__(self, logger=logger)
        self._type = '+'

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = False
        reserved = []
        if self.num_child() != 1:
            if self._logger:
                self._logger.error('invalid # of children nodes for node_plus')
            return extent, position, pass_fail, reserved

        _extent, _position, _pass_fail, _reserved = \
                self._children[0].process(text, extent, position, var)
       
        if not _pass_fail:
            return extent, position, pass_fail, reserved
            
        while _pass_fail:
            _extent, _position, _pass_fail, tmp_reserved = \
                self._children[0].process(text, _extent, _position, var)
            if tmp_reserved: _reserved += tmp_reserved
            
        extent = _extent
        position = _position
        pass_fail = True
        reserved += _reserved
        
        return extent, position, pass_fail, reserved
