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

        self._logger.info('현재 고려중인 놈 = {}'.format(text[position]))

        # 적용하기 (일부러 맨 뒤 규칙부터 적용)
        result = []
        rule_cands.reverse()
        for rname, rcont in rule_cands:
            self._logger.info('고려하는 규칙 = {}'.format(rname))
            pass_fail, _result, _extent, _position = rule_process._process(\
                rname, rcont, text, extent, position, variables, self._logger)
            if pass_fail:
                x = '[*] 매칭된 규칙 = {}'.format(rname)
                self._logger.info(x)
                result += _result
                break

        if not pass_fail:
            _position = position + 1
        else:
            # _position 은 이미 업데이트되어있을 것임
            pass

        if _position < len(text):
            _result, variables = self.process(text, extent, _position, variables, cur_node)
            result += _result

        return result, variables

