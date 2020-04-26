from node.node import node
from rule_process import rule_process
from extent import extent as ext
import pdb

class node_rule_refer(node):
    def __init__(self, rule_name, result_names, logger):
        node.__init__(self, logger=logger)
        self._type = 'RULE_REFER'
        self._attr['rule_name'] = rule_name
        self._attr['result_name'] = result_names.split(',')

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = True
        reserved = []
        if self.num_child() != 1:
            if self._logger:
                self._logger.error('invalid # of children in node_rule_refer')
        else:
            # 해당 rule의 dict_tree
            rname, rcont = self._attr['rule_name'], self._children[0]
            _pass_fail, _result, _extent, _position = \
                    rule_process._process(
                        rname, rcont, text, extent, position, None,
                        self._logger, 1)
            if _pass_fail:
                #_extent.bias(position) 
                #_extent.merge(extent)
                extent.merge(_extent)
                position = _position #position += _position
                if _result and self._attr['result_name']:
                    for x in self._attr['result_name']:
                        reserved += [_result[0].get(x)]
            else:
                pass_fail = False

        return extent, position, pass_fail, reserved
