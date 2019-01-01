import pdb

class extent(list):
    def __init__(self, x=None):
        list.__init__(self)
        if x and type(x) == list:
            for xitem in x:
                self.add(xitem)
    def is_overlap(self, pair):
        for b, e in self:
            if b <= pair[0] and pair[0] < e:
                return True
            if b < pair[1] and pair[1] <= e:
                return True
            if pair[0] <= b and e <= pair[1]:
                return True
        return False
    def is_adjacent(self, pair):
        for b, e in self:
            if b == pair[1] or e == pair[0]:
                return True
        return False
    def copy(self):
        ret = extent()
        ret += self
        return ret
    def merge(self, other):
        for x in other:
            self.add(x)
    def bias(self, v):
        new = self.copy()
        self.clear()
        for x in new:
            self.append((x[0] + v, x[1] + v))
    def add(self, pair):
        self.append(pair)
        sorted_extent = sorted(self, key=lambda tup: tup[0])
        
        self.clear()
        for higher in sorted_extent:
            if len(self) <= 0:
                self.append(higher)
            else:
                lower = self[-1]
                # test for intersection between lower and higher:
                # we know via sorting that lower[0] <= higher[0]
                if higher[0] <= lower[1]:
                    upper_bound = max(lower[1], higher[1])
                    self[-1] = (lower[0], upper_bound)  # replace by merged interval
                else:
                    self.append(higher)

