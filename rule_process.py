from var import var
from extent import extent
import re
import pdb

class rule_process:
    #_VAR_NAME_ = re.compile('\[.+?\]').match

    def __init__(self, rules, logger):
        self._rules = rules
        self._logger = logger

        #self._finder = dict()
        #self._finder['var_name'] = rule_process._VAR_NAME_

    def _process(rname, rcont, text, extent, position, variables=None,
            logger=None, tabs=0):
        if not variables:
            variables = var(logger)
        pass_fail = True
        result = []
        trees = rcont['condition']
        
        _extent = extent.copy()
        _position = position

        for t in trees:
            tree_opt = t.get_ext_option()
            add_extent = False if 'next' in tree_opt else True
            optional = 'opt' in tree_opt
            _tmp_extent, _position, _pass_fail, _ = \
                    t.get_root_node().process(
                        text, _extent, _position, variables, add_extent)
            if not _pass_fail and not optional:
                pass_fail = False
                break
            if add_extent:
                _extent.merge(_tmp_extent)

        if logger:
            logger.info('{}{}\t{}'.format('   ' * tabs, rname, pass_fail))
        if pass_fail:
            if logger:
                logger.info('{}{}, {}'.format('   ' * tabs, _extent, _position))
            # result 생성
            _result = dict()
            _result['extent'] = list(set(_extent) - set(extent))
            _result['extent'] = sorted(_result['extent'], key=lambda tup: tup[0])
            _result['name'] = rcont['name']
            _result['text'] = ''
            for b, e in _result['extent']:
                _result['text'] += text[b:e]
            result_dict = rcont['result']
            for result_name, result_value in result_dict.items():
                if isinstance(result_value, int):
                    pass
                else:
                    _, _, _, _reserved = result_value.process(None, _extent,
                            None, variables, add_extent)
                    if not _reserved:
                        result_value = None
                    else:
                        result_value = _reserved[-1]
                if result_value != None and 'None' not in result_value:
                    _result[result_name] = result_value
            result += [_result]
        return pass_fail, result, _extent, _position
 
    def process(self, text, extent=extent(), position=0, variables=None, cur_node=None):
        # indexing 알아보기
        rule_cands = []
        for rname, rcont in self._rules:
            rule_cands.append((rname, rcont))

        if not variables:
            variables = var(self._logger)

        if self._logger:
            self._logger.info('현재 고려중인 놈 = {}'.format(text[position]))

        matched = []

        # 적용하기 (일부러 맨 뒤 규칙부터 적용)
        result = []
        rule_cands.reverse()
        for rname, rcont in rule_cands:
            if self._logger:
                self._logger.info('고려하는 규칙 = {}'.format(rname))
            pass_fail, _result, _extent, _position = rule_process._process(\
                rname, rcont, text, extent, position, variables, self._logger)
            if pass_fail:
                if self._logger:
                    x = '[*] 매칭된 규칙 = {}, extent = {}'.format(rname, _extent)
                    self._logger.info(x)
                result += _result
                matched += [rname]
                break

        if not pass_fail:
            _position = position + 1
        else:
            # _position 은 이미 업데이트되어있을 것임
            pass

        if _position < len(text):
            _result, variables, _matched = self.process(text, extent, _position, variables, cur_node)
            result += _result
            matched += _matched

        return result, variables, matched

    def _merge_slot(slot1, slot2, text):
        ks1 = set(slot1.keys())
        ks2 = set(slot2.keys())
        for k in ks2 - ks1:
            slot1[k] = slot2[k]
        
        ext1 = extent(slot1.get('extent'))
        ext2 = slot2.get('extent')
        ext1.merge(ext2)
        i = 0
        while i < len(ext1)-1:
            left_end = ext1[i][1]
            right_begin = ext1[i+1][0]
            if right_begin - left_end == 1 and text[left_end] == ' ':
                ext1.add((left_end, left_end+1))
            i += 1
        slot1['extent'] = ext1
        
        slottxt = ''
        for b, e in ext1:
            slottxt += text[b:e]
        slot1['text'] = slottxt

    def merge_slot(self, slots, text, policy=None):
        if len(slots) < 2:
            return slots

        delidx = []
        for i in range(len(slots)-1):
            slot1 = slots[i]
            slot2 = slots[i+1]
            # extent 인접 여부
            ext_slot1 = slot1.get('extent')
            ext_slot2 = slot2.get('extent')
            if not ext_slot1 or not ext_slot2:
                continue
            is_adjacent = False
            for b1, e1 in ext_slot1:
                for b2, e2 in ext_slot2:
                    if b1 == e2 or b2 == e1:
                        is_adjacent = True
                        break
                    if b2 - e1 == 1 and text[e1] == ' ':
                        is_adjacent = True
                        break
                if is_adjacent:
                    break
            if is_adjacent:
                if policy:
                    chk_result = True
                    for plc in policy:
                        aname, acont = list(plc.items())[0]
                        if aname == 'same':
                            if slot1.get(acont) != slot2.get(acont):
                                chk_result = False
                                break
                        elif aname == 'order':
                            attr_keys = acont.split(',')
                            slot2_biggest_slotidx = None
                            for j, ak in enumerate(attr_keys):
                                if slot2.get(ak) != None:
                                    slot2_biggest_slotidx = j
                                    break
                            if slot2_biggest_slotidx != None:
                                for j in range(slot2_biggest_slotidx+1, len(attr_keys)):
                                    if slot1.get(attr_keys[j]) != None:
                                        chk_result = False
                                        break
                        else:
                            if self._logger:
                                self._logger.error('Invalid attributes key type = {}'.format(aname))
                            chk_result = False
                            break
                    if not chk_result:
                        continue
                
                rule_process._merge_slot(slot1, slot2, text)
                delidx.append(i+1)
                i += 1
        if delidx:
            delidx.reverse()
            for di in delidx:
                del(slots[di])
        return slots

