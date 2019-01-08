from sm_stack import stack
from sm_queue import queue
import copy
import pdb

class var:
    _MAXSIZE_ = 100

    def __init__(self, logger):
        self._stack = dict()
        self._queue = dict()
        self._checkpoint = None
        self._logger = logger

    def add(self, varname, varvalue):
        if varname[0] == 's':
            n = self._stack.get(varname)
            if not n:
                self._stack[varname] = stack(maxsize=var._MAXSIZE_)
            self._stack[varname].put(varvalue)
        elif varname[0] == 'q':
            n = self._queue.get(varname)
            if not n:
                self._queue[varname] = queue(maxsize=var._MAXSIZE_)
            self._queue[varname].put(varvalue)
        else:
            return None

    def checkpoint(self):
        if self._checkpoint:
            self._checkpoint['stack'].append(copy.deepcopy(self._stack))
            self._checkpoint['queue'].append(copy.deepcopy(self._queue))
        else:
            self._checkpoint = dict()
            self._checkpoint['stack'] = [copy.deepcopy(self._stack)]
            self._checkpoint['queue'] = [copy.deepcopy(self._queue)]

    def clear_checkpoint(self):
        if self._checkpoint:
            del(self._checkpoint)
        self._checkpoint = None

    def recovery(self):
        if not self._checkpoint:
            if self._logger:
                self._logger.error('no checkpoint for recovery')
            return False
        self._stack = self._checkpoint['stack'][-1]
        self._queue = self._checkpoint['queue'][-1]
        del(self._checkpoint['stack'][-1])
        del(self._checkpoint['queue'][-1])
        return True

    def glance(self, varname):
        if varname[0] == 's' and self._stack.get(varname):
            return self._stack[varname].glance()
        elif varname[0] == 'q' and self._queue.get(varname):
            return self._queue[varname].glance()
        return None

    def get(self, varname):
        if varname[0] == 's' and self._stack.get(varname):
            return self._stack[varname].get()
        elif varname[0] == 'q' and self._queue.get(varname):
            return self._queue[varname].get()
        return None

    def str(self):
        print('[stack]')
        for i, x in self._stack.items():
            print('\t{}:\t'.format(i), end='')
            x.str()
        print('[queue]')
        for i, x in self._queue.items():
            print('\t{}:'.format(i), end='')
            x.str()

