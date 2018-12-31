# -*- coding: utf-8 -*-

import json
from collections import OrderedDict
import os
import re
import pdb
from node.node import node

class dict_tree(OrderedDict):

    def __init__(self):
        pass

    def get_json(self):
        return dict(self)
    
    def get_string(self):
        return json.dumps(self, ensure_ascii=False, indent='\t')

    def loads(self, rawText):
        od = json.loads(rawText, object_pairs_hook=OrderedDict)
        for x in od:
            self[x] = od[x]
    
    def load_from_file(self, filepath):
        rawLines = ''
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            while True:
                r = f.readline()
                if not r:
                    break
                if r and r[0] == '#':
                    continue
                rawLines += r
        self.loads(rawLines)
    
    def save_to_file(self, filepath):
        with open(filepath, 'w', encoding='utf-8-sig') as f:
            f.write(self.getString())

