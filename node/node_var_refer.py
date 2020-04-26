from node.node import node
from rule_process import rule_process
from extent import extent as ext
import re
import pdb

class node_var_refer(node):
    _DIGIT_ = re.compile('[0-9]+').match

    def __init__(self, var_name, var_func, logger):
        node.__init__(self, logger=logger)
        self._type = 'VAR_REFER'
        self._attr['var_name'] = var_name
        self._attr['var_func'] = var_func

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = True
        reserved = []

        name = self._attr['var_name']
        func = self._attr['var_func']
        
        if self._attr['var_func'] == None:
            func = '1'

        digit = node_var_refer._DIGIT_(func)
        if digit:
            b, e = digit.span()
            if e < len(func) or b != 0:
                if self._logger:
                    self._logger.error('Invalid var_funct = {}'.format(func))
                return extent, position, pass_fail, reserved
            digit = int(func)
            for i in range(digit):
                reserved.append(var.get(name))

        return extent, position, pass_fail, reserved
