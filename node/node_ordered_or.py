from node.node import node

class node_ordered_or(node):
    def __init__(self, logger):
        node.__init__(self, logger=logger)
        self._type = 'ORDERED_OR'
        self._prev_accepted_cnode_idx = -1

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = False
        reserved = []
        i = self._prev_accepted_cnode_idx + 1
        while True:
            if i >= self.num_child():
                pass_fail = False
                break
            _extent, _position, _pass_fail, _reserved = \
                    self._children[i].process(text, extent, position, var)
            if _pass_fail:
                if add_extent:
                    extent.merge(_extent)
                position = _position
                pass_fail = True
                reserved += _reserved
                self._prev_accepted_cnode_idx = -1 if i == self.num_child() - 1 else i
                break
            i += 1
        # 만족하지 못한 경우,
        if not pass_fail:
            self._prev_accepted_cnode_idx = -1

        return extent, position, pass_fail, reserved
