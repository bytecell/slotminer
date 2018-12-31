from node.node import node

class node_one_or_not(node):
    def __init__(self, logger):
        node.__init__(self, logger=logger)
        self._type = '?'

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = False
        reserved = []

        #if self.num_child() != 1:
        #    self._logger.error('invalid # of children nodes for node_one_or_not')
        #    return extent, position, pass_fail, reserved

        _position = position

        if self.num_child() > 1:
            var.checkpoint()    
            _extent = extent.copy()
        else:
            _extent = extent
        
        for cnode in self._children:
            _extent, _position, _pass_fail, _reserved = \
                cnode.process(text, _extent, _position, var, add_extent)
            if not _pass_fail:
                break
        
        if not _pass_fail:
            pass_fail = True
            if self.num_child() > 1:
                var.recovery()
        else:
            if add_extent:
                extent.merge(_extent)
            position = _position
            pass_fail = True
            reserved += _reserved
        
        return extent, position, pass_fail, reserved
