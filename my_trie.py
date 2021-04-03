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
        length_dict = {}
        for position in range(len(text)):
            if text[position] in to_skip:
                continue
            _tags, _texts = self._process(text, position)
            for i in range(len(_tags)):
                _tag, _text, _extent = _tags[i], _texts[i], (position, position+len(_texts[i]))
                length = _extent[1] - _extent[0]
                this_result = (_tag, _text, _extent)
                results += [this_result]

                if length_dict.get(length) == None:
                    length_dict[length] = [this_result]
                else:
                    length_dict[length] += [this_result]
        if len(results) >= 2 and longest:
            new_results = []
            occupied = [False] * len(text)
            lengths = list(length_dict.keys())
            lengths.sort(reverse=True)
            for l in lengths:
                for r in length_dict[l]:
                    b, e = r[2]
                    if True in occupied[b:e]:
                        continue
                    occupied[b:e] = [True] * (e-b)
                    inserted = False
                    for i, _r in enumerate(new_results):
                        if _r[2][1] > r[2][1]:
                            new_results.insert(i, r)
                            inserted = True
                            break
                    if not inserted:
                        new_results += [r]
            results = new_results
        return results

    def str(self, tabs=0):
        self._root_node.str('ROOT', tabs)

