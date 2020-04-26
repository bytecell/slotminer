from node.node import node
import pdb

class node_match_text(node):
    def __init__(self, target_text, logger):
        node.__init__(self, logger=logger)
        self._type = 'MATCH_TEXT'
        self._attr['target_text'] = target_text

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = False
        reserved = []

        # 결과물 만드는 경우,
        if text == None:
            return extent, position, True, [self._attr['target_text']]

        if self.num_child():
            if self._logger:
                self._logger.error('match_text_node must be terminal node')
            return extent, position, pass_fail, reserved
        if not self._attr.get('target_text'):
            if self._logger:
                self._logger.error('empty target_text')
            return extent, position, pass_fail, reserved

        if position >= len(text):
            return extent, position, pass_fail, reserved

        target_text = self._attr['target_text']
        pos_begin = position
        pos_end = position + len(target_text)

        # overlap check with extent
        if add_extent and extent.is_overlap((pos_begin, pos_end)):
            return extent, position, pass_fail, reserved

        if text[pos_begin:pos_end].lower() == target_text:
            position = pos_end
            _extent = extent.copy()
            if add_extent:
                _extent.add((pos_begin, pos_end))
            pass_fail = True
            reserved += [text[pos_begin:pos_end]]
            return _extent, position, pass_fail, reserved

        return extent, position, pass_fail, reserved

