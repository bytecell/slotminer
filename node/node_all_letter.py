from node.node import node
import re

class node_all_letter(node):
    def __init__(self, logger):
        node.__init__(self, logger=logger)
        self._type = 'ALL_LETTER'

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = False
        reserved = []
        if self.num_child():
            if self._logger:
                self._logger.error('all_letter_node must be terminal node')
            return extent, position, pass_fail, reserved

        if position >= len(text):
            return extent, position, pass_fail, reserved
        
        if add_extent and extent.is_overlap((position, position+1)):
            return extent, position, pass_fail, reserved

        pass_fail = True
        if add_extent:
            _extent = extent.copy()
            _extent.add((position, position+1))
            extent = _extent
            position += 1
            if position < len(text):
                reserved += [text[position]]

        return extent, position, pass_fail, reserved

