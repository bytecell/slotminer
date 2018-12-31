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
                self._logger.error('var name must begin with $')
            n = n[1:]
            if i >= len(values):
                self._logger.error('value not exist')
            v = values[i]
            self._attr['variables'][n] = v

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = True
        reserved = []

        no_child = False
        if self.num_child() > 1:
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
        
        
        # 각 자식노드에 대하여,
        #    결과물 얻고, 실패하면 pass_fail = False 후, 리턴
        #          성공 시, 결과물 str에 추가
        #                   (단, 그 자식노드가 refer이면 reserved 사용)
        # 모든 자식노드가 성공 시, 결과용 변수의 내용으로 var에 추가
        
        
        """
        for var_name, var_value in self._attr['variables'].items():
            if var_value and var_value[0] == '@':
                if self.num_child() != 1:
                    self._logger.error('No children for variable assignment using rule-ref')
                    return extent, position, pass_fail, reserved
                _extent, _position, _pass_fail, _reserved = \
                        self._children[0].process(text, extent, position, var, add_extent)
                if _pass_fail:
                    extent = _extent
                    position = _position
                    reserved = _reserved
                    var.add(var_name, reserved)
                else:
                    pass_fail = False
            else:
                var.add(var_name, var_value)
        reserved = None
        return extent, position, pass_fail, reserved
        """
