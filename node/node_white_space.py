from node.node import node
import re
import pdb

class node_white_space(node):
    def __init__(self, logger):
        node.__init__(self, logger=logger)
        self._type = 'WHITE_SPACE'
        self._white_space = re.compile('\s').match

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = False
        reserved = []
        if self.num_child():
            if self._logger:
                self._logger.error('white_space_node must be terminal node')
            return extent, position, pass_fail, reserved

        tmp = self._white_space(text[position:])

        # extent 겹치면 False
        if add_extent and extent.is_overlap((position, position+1)):
            return extent, position, pass_fail, reserved
        
        # white-space 이면 True
        if tmp:
            pass_fail = True
            b, e = tmp.span()
            b, e = b + position, e + position
            if add_extent:
                _extent = extent.copy()
                _extent.add((b, e))
                extent = _extent
            position = e
            #reserved += [text[b:e]]

        return extent, position, pass_fail, reserved

