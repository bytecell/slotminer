from node.node import node
from node.node_concat import node_concat
from collections import OrderedDict
import pdb

class node_assign(node):
    def __init__(self, vname, vvalue, logger):
        node.__init__(self, logger=logger)
        self._type = 'VAR_ASSIGN'
        
        self._attr['variables'] = OrderedDict()
        names = vname.split(',')
        values = vvalue.split(',')
        for i, n in enumerate(names):
            if n[0] != '$':
                if self._logger:
                    self._logger.error('var name must begin with $')
            n = n[1:]
            if i >= len(values):
                if self._logger:
                    self._logger.error('value not exist')
            v = values[i]
            self._attr['variables'][n] = v

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = True
        reserved = []

        no_child = False
        if self.num_child() > 1:
            if self._logger:
                self._logger.error('Invalid #children for node_assign')
            return extent, position, pass_fail, reserved
        elif self.num_child() == 0:
            no_child = True
        else:
            _extent, _position, _pass_fail, _reserved = \
                self._children[0].process(text, extent, position, var, add_extent)

        i = -1
        vars = list(self._attr['variables'].items())
        vars.reverse()
        for var_name, var_value in vars:
            if no_child:
                value = var_value
            else:
                if not _pass_fail:
                    pass_fail = False
                    return extent, position, pass_fail, reserved
                else:
                    if _reserved:
                        value = _reserved[i]
                #if isinstance(self._children[0], node_concat):
                #else:
                #    self._logger.error('Invalid children type for node_assign')
                #    return extent, position, False, reserved

            var.add(var_name, value)
            i -= 1

        if not no_child and pass_fail:
            if add_extent:
                extent.merge(_extent)
            position = _position

        return extent, position, pass_fail, reserved
