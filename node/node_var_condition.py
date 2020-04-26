from node.node import node
from rule_process import rule_process
from extent import extent as ext
import re
import pdb

class node_var_condition(node):
    _CHK_DICT_ = {
        '==': list.__eq__,
        '>=': list.__ge__,
        '<=': list.__le__,
        '>': list.__gt__,
        '<': list.__lt__,
        '!=': list.__ne__
    }

    def check_var_condition(txt):
        for x in node_var_condition._CHK_DICT_.keys():
            if x in txt and txt.find(x) != 0:
                return x, node_var_condition._CHK_DICT_[x]
        return None, None

    def __init__(self, left, operator, right, logger):
        node.__init__(self, logger=logger)
        self._type = 'VAR_CONDITION'
        self._attr['left'] = left.split(',')
        self._attr['operator'] = operator
        self._attr['right'] = right.split(',')

        if len(self._attr['left']) != len(self._attr['right']):
            if self._logger:
                self._logger.error('Inconsistent # of operands for node_var_condition = {}, {}'.format(left, right))

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = False
        reserved = []

        left = self._attr['left']
        right = self._attr['right']

        left_val = []
        right_val = []

        for l, r in zip(left, right):
            if l and l[0] == '$':
                l = var.glance(l[1:])
            if r and r[0] == '$':
                r = var.glance(r[1:])
            left_val.append(l)
            right_val.append(r)

        if self._attr['operator'](left_val, right_val):
            pass_fail = True

        return extent, position, pass_fail, reserved
