from node.node_trie import node_trie
import pdb

class my_trie:
    def __init__(self, root_node=None, logger=None):
        self._logger = logger
        if root_node:
            self._root_node = root_node
        else:
            self._root_node = node_trie(self._logger)

    def set_root_node(self, rnode):
        self._root_node = rnode

    def get_root_node(self):
        return self._root_node

    def _process(self, text, position):
        results, pass_fail, reserved = self._root_node.process(
            text, None, position, None)
        tags = []
        texts = []
        if pass_fail:
            tags += results
            tmp_txt = ''.join(reserved).strip()
            texts += [tmp_txt]
        return tags, texts
    
    def process(self, text, to_skip=[' '], longest=False):
        results = []
        for position in range(len(text)):
            if text[position] in to_skip:
                continue
            _tags, _texts = self._process(text, position)
            for i in range(len(_tags)):
                results += [(_tags[i],
                    _texts[i],
                    (position, position+len(_texts[i])))]
        if len(results) >= 2 and longest:
            pass
        return results

    def str(self, tabs=0):
        self._root_node.str('ROOT', tabs)

