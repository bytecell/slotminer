from dict_tree import dict_tree
from tree import tree
from node.node_or import node_or
from node.node_ordered_or import node_ordered_or
from node.node_and import node_and
from node.node_pass import node_pass
from node.node_assign import node_assign
from node.node_rule_refer import node_rule_refer
from node.node_var_refer import node_var_refer
from node.node_white_space import node_white_space
from node.node_all_letter import node_all_letter
from node.node_match_text import node_match_text
from node.node_plus import node_plus
from node.node_not_match_text import node_not_match_text
from node.node_one_or_not import node_one_or_not
from node.node_freq import node_freq
from node.node_concat import node_concat
from node.node_var_condition import node_var_condition
from node.node_empty_begin import node_empty_begin
from node.node_empty_end import node_empty_end
from node.node_sm_int import node_sm_int
from node.node_sm_float import node_sm_float
from node.node_sm_cardinal_int import node_sm_cardinal_int
import re
import pdb

class rule_loader:
    def __init__(self, logger):
        self._R = dict_tree()
        self._P = None
        self._I = dict()
        self._logger = logger

        def find_ors(text):
            ors = []
            ordered_ors = []
            opened = 0
            i = 0
            while i < len(text):
                if text[i] == '(':
                    opened += 1
                elif text[i] == ')':
                    opened -= 1
                elif text[i] == '|' and opened == 0:
                    if i+1 < len(text) and text[i+1] == '|':
                        ordered_ors.append(i)
                        i += 1
                    else:
                        ors.append(i)                  
                i += 1
            return ors, ordered_ors
        def find_right_term(text):
            x = text.find('(')
            if x < 0:
                x = text.find('[')
            if x < 0:
                x = text.find('@')
            if x < 0:
                x = text.find('$')
            return x
        def find_small_paren(text):
            b = text.find('(')
            num_b = 1
            idx = b+1
            while num_b:
                if idx >= len(text):
                    return b, -1
                if text[idx] == '(':
                    num_b += 1
                elif text[idx] == ')':
                    num_b -= 1
                idx += 1
            e = idx
            return b, e
        def find_middle_paren(text):
            b = text.find('{')
            e = text.find('}', b+1)
            return b, e
        def find_big_paren(text):
            b = text.find('[')
            num_b = 1
            idx = b+1
            while num_b:
                if idx >= len(text):
                    return b, -1
                if text[idx] == '[':
                    num_b += 1
                elif text[idx] == ']':
                    num_b -= 1
                idx += 1
            e = idx
            return b, e
        def find_specials(text):
            i1 = text.find('(')
            i2 = text.find('[')
            result_i = i1
            if result_i < 0:
                result_i = i2
            elif i2 >= 0 and i2 < result_i:
                result_i = i2
            return result_i
        def find_split_terms(text, delim):
            ret = []
            tmp = ''
            i = 0
            small_appear = 0
            big_appear = 0
            while i < len(text):
                t = text[i:i+len(delim)]
                if t == delim:
                    i += len(delim)
                    if small_appear == 0 and big_appear == 0:
                        ret.append(tmp)
                        tmp = ''
                    else:
                        tmp += t
                    continue
                t = text[i]
                if t == '[':
                    big_appear += 1
                    tmp += t
                elif t == '(':
                    small_appear += 1
                    tmp += t
                elif t == ')':
                    small_appear -= 1
                    tmp += t
                elif t == ']':
                    big_appear -= 1
                    tmp += t
                else:
                    tmp += t
                i += 1
            if tmp:
                ret.append(tmp)
            return ret

        self._finder = dict()
        self._finder['small_paren'] = find_small_paren
        self._finder['middle_paren'] = find_middle_paren
        self._finder['big_paren'] = find_big_paren
        self._finder['rule_refer'] = re.compile('@.+(\.[a-zA-Z0-9_]+)?').match
        self._finder['var_refer'] = re.compile('\$[sq][a-zA-Z0-9_]*(\.[a-zA-Z0-9_]+)?').match
        self._finder['specials'] = find_specials
        self._finder['split_terms'] = find_split_terms
        self._finder['ors'] = find_ors
        self._finder['white_space'] = re.compile('\s').match
        self._finder['right_term'] = find_right_term 
    
    def make_tree(self, rule_phrase, ext, cur_node=None):
        result_tree = None
        if not cur_node:
            result_tree = tree(ext=ext, root_node=None, logger=self._logger)
            cur_node = result_tree.get_root_node()

        small_paren = self._finder['small_paren'](rule_phrase)
        big_paren = self._finder['big_paren'](rule_phrase)
        rule_refer = self._finder['rule_refer'](rule_phrase)
        var_refer = self._finder['var_refer'](rule_phrase)
        specials = self._finder['specials'](rule_phrase)
        white_space = self._finder['white_space'](rule_phrase)
        remain_txt = None
        new_node = None

        # 소괄호
        if small_paren[0] == 0:
            b, e = small_paren
            if e < 0:
                if self._logger:
                    self._logger.error('small paren is not paired')
                return None
            cur_txt = rule_phrase[b+1:e-1]
            idx_for_middle_paren = self._finder['middle_paren'](rule_phrase[e:])

            # 소괄호는 무조건 일단 and 노드로 시작하도록 함
            #and_node = node_and(self._logger)
            #cur_node.add_child(and_node)
            #cur_node = and_node

            # + 체크
            if e < len(rule_phrase) and rule_phrase[e] == '+':
                new_node = node_plus(self._logger)
                cur_node.add_child(new_node)
                self.make_tree(rule_phrase[b:e], ext, new_node)
                if len(rule_phrase) > e+1:
                    remain_txt = rule_phrase[e+1:]
                else:
                    remain_txt = None
            # ! 체크
            elif e < len(rule_phrase) and rule_phrase[e] == '!':
                new_node = node_not_match_text(rule_phrase[b+1:e-1], self._logger)
                cur_node.add_child(new_node)
                #self.make_tree(rule_phrase[b:e], ext, new_node)
                if len(rule_phrase) > e+1:
                    remain_txt = rule_phrase[e+1:]
                else:
                    remain_txt = None
            # ? 체크
            elif e < len(rule_phrase) and rule_phrase[e] == '?':
                new_node = node_one_or_not(self._logger)
                cur_node.add_child(new_node)
                self.make_tree(rule_phrase[b:e], ext, new_node)
                if len(rule_phrase) > e+1:
                    remain_txt = rule_phrase[e+1:]
                else:
                    remain_txt = None
            # {} 체크
            elif idx_for_middle_paren[0] == 0 and idx_for_middle_paren[1] > 0:
                mb, me = e + 1 + idx_for_middle_paren[0], e + idx_for_middle_paren[1]
                mphrase = rule_phrase[mb:me]
                if ',' in mphrase:
                    lower, upper = mphrase.split(',')
                else:
                    lower = mphrase
                    upper = lower
                new_node = node_freq(lower, upper, self._logger)
                cur_node.add_child(new_node)
                self.make_tree(rule_phrase[b:e], ext, new_node)
                if len(rule_phrase) > me:
                    remain_txt = rule_phrase[me+1:]
                else:
                    remain_txt = None
            else:
                idx_ors, idx_ordered_ors = self._finder['ors'](cur_txt)
                if idx_ors and idx_ordered_ors:
                    if self._logger:
                        self._logger.error('|| and | appear concurrently = {}'.format(cur_txt))
                    return None
                # | 처리
                if idx_ors:
                    new_node = node_or(self._logger)
                    cur_node.add_child(new_node)

                    terms = self._finder['split_terms'](cur_txt, '|')
                    for term in terms:
                        #term = term.strip()
                        and_node = node_and(self._logger)
                        new_node.add_child(and_node)
                        self.make_tree(term, ext, and_node)

                    remain_txt = rule_phrase[e:]
                # || 처리
                elif idx_ordered_ors:
                    new_node = node_ordered_or(self._logger)
                    cur_node.add_child(new_node)

                    terms = self._finder['split_terms'](cur_txt, '||')
                    for term in terms:
                        and_node = node_and(self._logger)
                        new_node.add_child(and_node)
                        self.make_tree(term, ext, and_node)

                    remain_txt = rule_phrase[e:]
                # 그 외 경우,
                else:
                    self.make_tree(cur_txt, ext, cur_node)
                    new_node = cur_node
                    remain_txt = rule_phrase[e:]
        # 대괄호
        elif big_paren[0] == 0:
            b, e = big_paren
            cur_txt = rule_phrase[b+1:e-1]
            
            # 대괄호는 무조건 일단 and 노드로 시작하도록 함
            #and_node = node_and(self._logger)
            #cur_node.add_child(and_node)
            #cur_node = and_node
            
            var_comp = node_var_condition.check_var_condition(cur_txt)

            # Variable comparison
            if var_comp and var_comp[0]:
                operand = var_comp[1]
                left, right = cur_txt.split(var_comp[0])
                new_node = node_var_condition(left, operand, right, self._logger)
                cur_node.add_child(new_node)
            # Variable assignment
            elif '=' in cur_txt:
                var_name, var_value = cur_txt.split('=')
                new_node = node_assign(var_name, var_value, self._logger)
                cur_node.add_child(new_node)
                if var_value and self._finder['right_term'](var_value) >= 0:
                    if ',' not in var_name:
                        right_node = node_concat(self._logger)
                        new_node.add_child(right_node)
                    else:
                        right_node = new_node
                    self.make_tree(var_value, ext, right_node)
            # Rule refer
            elif cur_txt and cur_txt[0] == '@':
                self.make_tree(cur_txt, ext, cur_node)
                new_node = cur_node
            # var refer
            elif cur_txt and cur_txt[0] == '$':
                self.make_tree(cur_txt, ext, cur_node)
                new_node = cur_node
            # All-letter(.)
            elif cur_txt == '.':
                new_node = node_all_letter(self._logger)
                cur_node.add_child(new_node)
            # white space
            elif cur_txt == ' ':
                new_node = node_white_space(self._logger)
                cur_node.add_child(new_node)
            # empty-begin
            elif cur_txt == '<':
                new_node = node_empty_begin(self._logger)
                cur_node.add_child(new_node)
            # empty-end
            elif cur_txt == '>':
                new_node = node_empty_end(self._logger)
                cur_node.add_child(new_node)
            else:
                if self._logger:
                    self._logger.error('invalid syntax for [ ] = {}'.format(rule_phrase))
            remain_txt = rule_phrase[e:]
        # 변수 언급
        elif var_refer and var_refer.span()[0] == 0:
            b, e = var_refer.span()
            cur_txt = rule_phrase[b+1:e]
            if '.' in cur_txt:
                var_name, var_func = cur_txt.split('.')
            else:
                var_name = cur_txt
                var_func = None
            new_node = node_var_refer(var_name, var_func, self._logger)
            cur_node.add_child(new_node)

            remain_txt = rule_phrase[e:]
        # 타 규칙 언급 (내장 규칙 포함)
        elif rule_refer and rule_refer.span()[0] == 0:
            b, e = rule_refer.span()
            cur_txt = rule_phrase[b+1:e]
            if '.' in cur_txt:
                rule_name, result_names = cur_txt.split('.')
            else:
                rule_name = cur_txt
                result_names = None

            if rule_name[:2] == '__' and rule_name[-2:] == '__':
                rule_name = 'SM_' + rule_name[2:-2]
                if rule_name == 'SM_INT':
                    new_node = node_sm_int(self._logger)
                elif rule_name == 'SM_FLOAT':
                    new_node = node_sm_float(self._logger)
                elif rule_name == 'SM_CARDINAL_INT':
                    new_node = node_sm_cardinal_int(self._logger)
                cur_node.add_child(new_node)
            else:
                new_node = node_rule_refer(rule_name, result_names, self._logger)
                cur_node.add_child(new_node)
            
                if rule_name:
                    if self._R.get(rule_name):
                        new_node2 = self._R.get(rule_name)
                        new_node.add_child(new_node2)
                    else:
                        if self._logger:
                            self._logger.error('non-existing rule-name for rule refer = {}'.format(rule_phrase))
                else:
                    if self._logger:
                        self._logger.error('rule-name is empty in {}'.format(cur_txt))

            remain_txt = rule_phrase[e:]
        # white-space
        elif white_space and white_space.span()[0] == 0:
            if self._logger:
                self._logger.error('Invalid white-space = {}'.format(rule_phrase))
            return None
        # 그외 (일반 text로 취급)
        else:
            e = specials
            if e >= 0:
                cur_txt = rule_phrase[:e]
                remain_txt = rule_phrase[e:]
                if not isinstance(cur_node, node_and) and \
                    not isinstance(cur_node, node_concat):
                    new_node = node_and(self._logger)
                    cur_node.add_child(new_node)
                else:
                    new_node = cur_node
                self.make_tree(cur_txt, ext, new_node)
                self.make_tree(remain_txt, ext, new_node)
                remain_txt = None
            else:
                cur_txt = rule_phrase
                new_node = node_match_text(cur_txt, self._logger)
                cur_node.add_child(new_node)
                remain_txt = None

        # 나머지 text가 있는지 체크하여 재귀호출
        if not new_node and remain_txt:
            if self._logger:
                self._logger.error('no valid child node is generated: {}'.format(rule_phrase))
        elif remain_txt:
            self.make_tree(rule_phrase=remain_txt, ext=ext, cur_node=cur_node)

        return result_tree

    def get_policy(self):
        return self._P

    def get_rules(self):
        return self._R.items()

    def generate_rules(self):
        if len(self._R) <= 0:
            return False

        items = list(self._R.items()).copy()
        for rname, rcont in items:
            # attributes 에 대한 처리
            if rname == 'attributes':
                self._P = rcont.copy()
                del(self._R[rname])
                continue
            # result 부분
            result = rcont.get('result')
            if not result:
                if self._logger:
                    self._logger.error('No result in rule {}'.format(rname))
                return False
            for rst_name, rst_cont in result.items():
                if isinstance(rst_cont, int):
                    result[rst_name] = rst_cont
                else:
                    result_root_node = node_concat(self._logger)
                    result[rst_name] = result_root_node
                    self.make_tree(rst_cont, 'next', result_root_node)
            # 여기부터는 condition 부분
            conds = rcont.get('condition')
            if not conds:
                if self._logger:
                    self._logger.error('No condition in rule {}'.format(rname))
                return False
            trees = []
            for cond in conds:
                k = list(cond.keys())
                k = k[0]
                if 'next' not in k and 'ext' not in k:
                    if self._logger:
                        self._logger.error('Invalid condition type = {}'.format(cond))
                    return False
                c = cond.get(k)
                c = c.strip()
                if not c:
                    if self._logger:
                        self._logger.error('Only white-spaces in condition = {}'.format(cond))
                    return False
                t = self.make_tree(c, k)
                if not t:
                    if self._logger:
                        self._logger.error('Tree generation failed')
                    return False
                trees.append(t)
            rcont['condition'] = trees
        return True

    def print_rules(self):
        for rname, rcont in self._R.items():
            print('* Rule {}'.format(rname))
            for rk, rv in rcont.items():
                if rk == 'condition':
                    print('\t-{}: ['.format(rk))
                    for c in rv:
                        c.str(tabs=4)
                    print(']')
                elif rk == 'result':
                    print('\t-{}: '.format(rk))
                    for rst_k, rst_v in rv.items():
                        if isinstance(rst_v, int):
                            print('\t  {}={}'.format(rst_k, rst_v))
                        else:
                            print('\t  {}='.format(rst_k))
                            rst_v.str(tabs=4)
                else:
                    print('\t-{}: {}'.format(rk, rv))

    def load(self, filepath):
        tmp_tree = dict_tree()
        tmp_tree.load_from_file(filepath)

        tmp_keys = set(tmp_tree.keys())
        cur_keys = set(self._R.keys())
        common_keys = tmp_keys & cur_keys
        if len(common_keys) > 0:
            return False

        self._R.update(tmp_tree)
        return True

