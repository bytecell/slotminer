from node.node import node
import re
import pdb

class node_sm_float(node):
    def __init__(self, logger):
        node.__init__(self, logger=logger)
        self._type = 'SM_FLOAT'
        self._pattern = re.compile('[0-9.,]+')
        #self._attr['target_text'] = target_text

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = False
        reserved = []

        # 결과물 만드는 경우,
        if text == None:
            return extent, position, True, reserved #[self._attr['target_text']]

        if self.num_child():
            if self._logger:
                self._logger.error('this must be terminal node')
            return extent, position, pass_fail, reserved

        if position >= len(text):
            return extent, position, pass_fail, reserved

        matched = self._pattern.match(text[position:])
        if matched:
            pos_begin, pos_end = matched.span()
            pos_begin, pos_end = pos_begin + position, pos_end + position

            # overlap check with extent
            if add_extent and extent.is_overlap((pos_begin, pos_end)):
                return extent, position, pass_fail, reserved

            position = pos_end
            _extent = extent.copy()
            if add_extent:
                _extent.add((pos_begin, pos_end))
            pass_fail = True
            reserved += [text[pos_begin:pos_end]]
            return _extent, position, pass_fail, reserved

        return extent, position, pass_fail, reserved

