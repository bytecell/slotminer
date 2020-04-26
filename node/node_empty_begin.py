from node.node import node
import re

class node_empty_begin(node):
    def __init__(self, logger):
        node.__init__(self, logger=logger)
        self._type = 'EMPTY|BEGIN'
        self._white_space = re.compile('\s').match

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = False
        reserved = []

        if self.num_child():
            if self._logger:
                self._logger.error('empty_node must be terminal node')
            return extent, position, pass_fail, reserved

        if position >= len(text):
            pass_fail = False
        elif position == 0:
            pass_fail = True
        else:
            tmp = self._white_space(text[position-1:position])
            if tmp:
                pass_fail = True

        return extent, position, pass_fail, reserved

