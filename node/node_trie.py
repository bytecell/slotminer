from node.node import node
import pdb

class node_trie(node,dict):
    def __init__(self, logger):
        node.__init__(self, logger=logger)
        self._freq = 0
        self._output = []

    def generate(self, text, output, freq=1):
        self._freq += freq
        
        if len(text) <= 0:
            self._output += [output]
            return 0

        i = 0
        while i < len(text) and text[i] == ' ':
            i += 1
        if i >= len(text):
            self._output += [output]
            return 0
    
        the_letter = text[i]
        if self.get(the_letter) == None:
            new_child = node_trie(self._logger)
            self[the_letter] = new_child

        return 1 + self[the_letter].generate(text[i+1:], output)

    def process(self, text, extent, position, var, add_extent=True):
        pass_fail = False
        reserved = []
        results = []

        if position >= len(text):
            if self._output:
                results += self._output
                pass_fail = True
            return results, pass_fail, reserved

        the_term = text[position]

        # 빈 칸이면,
        if the_term == ' ':
            _results, _pass_fail, _reserved = \
                self.process(text, extent, position+1, var, add_extent)
            results += _results
            reserved += [the_term] + _reserved
            return results, _pass_fail, reserved

        # 현재 position 글자가 매칭되면, 해당 child node의 결과를 받아서 리턴
        if self.get(the_term) != None:
            _results, _pass_fail, _reserved = \
                    self[the_term].process(text, extent, position+1, var, add_extent)
            results += _results
            reserved += [the_term] + _reserved
            return results, _pass_fail, reserved

        # 매칭 안 된 경우
        #pass_fail = len(self._output) > 0
        if self._output:
            results += self._output
            pass_fail = True
        return results, pass_fail, reserved

    def str(self, key_text, tabs=0):
        tag = self._output if self._output else ''
        me = '{}[{}] {} {}'.format(' ' * tabs, key_text, self._freq, tag)
        print(me)
        for c in self.keys():
            self[c].str(c, tabs+1)

        
