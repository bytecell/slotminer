from node.node import node
import pdb

class node_freq(node):
    def __init__(self, lower, upper, logger):
        node.__init__(self, logger=logger)
        self._lower = int(lower) if lower else 0
        self._upper = int(upper) if upper else None
        self._type = '{' + '{},{}'.format(lower, upper) + '}'
        self._cur = 0

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = False
        reserved = []
        if self.num_child() != 1:
            if self._logger:
                self._logger.error('invalid # of children nodes for node_freq')
            return extent, position, pass_fail, reserved

        _extent = extent.copy()
        _position = position

        while True:
            _extent, _position, _pass_fail, _reserved = \
                self._children[0].process(text, _extent, _position, var)
            if not _pass_fail:
                if self._cur < self._lower:
                    pass_fail = False
                else:
                    pass_fail = True
                    extent = _extent
                    position = _position
                    reserved += _reserved
                break
            else:
                self._cur += 1
                reserved += _reserved
                if self._upper != None and self._cur >= self._upper:
                    pass_fail = True
                    extent = _extent
                    position = _position
                    break

        self._cur = 0

        return extent, position, pass_fail, reserved
