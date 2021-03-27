from my_trie import my_trie
from dict_tree import dict_tree
import pdb

class trie_loader:
    def __init__(self, logger):
        self._logger = logger

    def make_trie(self, filepath):
        self._trie = my_trie(logger=self._logger)
        root_node = self._trie.get_root_node()

        dt = dict_tree()
        dt.load_from_file(filepath)

        for tag, kvs in dt.items():
            for k, vs in kvs.items():
                root_node.generate(k, tag)
                for v in vs:
                    root_node.generate(v, tag)
        return self._trie

    def load(self, filepath):
        return True

