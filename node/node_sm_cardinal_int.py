from node.node import node
import re
import pdb

class node_sm_cardinal_int(node):
    def __init__(self, logger):
        node.__init__(self, logger=logger)
        self._type = 'SM_CARDINAL_INT'
        self._pattern1 = {
            re.compile("열"): (10, True),
            re.compile("스무"): (20, False),
            re.compile("스물"): (20, True),
            re.compile("서른"): (30, True),
            re.compile("마흔"): (40, True),
            re.compile("쉰"): (50, True),
            re.compile("예순"): (60, True),
            re.compile("일흔"): (70, True),
            re.compile("여든"): (80, True),
            re.compile("아흔"): (90, True)
        }
        self._pattern2 = {
            re.compile("한"): 1,
            re.compile("두"): 2,
            re.compile("세"): 3,
            re.compile("네"): 4,
            re.compile("다섯"): 5,
            re.compile("여섯"): 6,
            re.compile("일곱"): 7,
            re.compile("여덟"): 8,
            re.compile("아홉"): 9
        }
 
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

        value = 0
        _position = position
        matched1 = None
        for p, (v, n) in self._pattern1.items():
            matched1 = p.match(text[position:])
            if matched1:
                pos_begin, pos_end = matched1.span()
                pos_begin, pos_end = pos_begin + position, pos_end + position
                _position = pos_end
                value += v
                break
        matched2 = None
        if not matched1 or (matched1 and n):
            for p, v in self._pattern2.items():
                matched2 = p.match(text[_position:])
                if matched2:
                    pos_begin2, pos_end2 = matched2.span()
                    pos_begin2, pos_end2 = pos_begin2 + _position, pos_end2 + _position
                    value += v
                    break
        if matched1:
            if matched2:
                pos_end = pos_end2
        else:
            if matched2:
                pos_begin, pos_end = pos_begin2, pos_end2
        
        if matched1 or matched2:
            # overlap check with extent
            if add_extent and extent.is_overlap((pos_begin, pos_end)):
                return extent, position, pass_fail, reserved

            position = pos_end
            _extent = extent.copy()
            if add_extent:
                _extent.add((pos_begin, pos_end))
            pass_fail = True
            reserved += [str(value)]
            return _extent, position, pass_fail, reserved

        return extent, position, pass_fail, reserved

