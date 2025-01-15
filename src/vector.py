import math
import collections


def extend(values, idx):
    if idx >= len(values):
        values.extend([0] * (idx + 1 - len(values)))


class Vec(object):
    def __init__(self, *args, **kwargs):
        """ Create a vector, example: v = Vector(1,2) """

        self.values = []
        for arg in args:
            if isinstance(arg, Vec):
                self.values.extend(arg.values)
            elif hasattr(arg, "__iter__"):
                if isinstance(arg, tuple) and len(arg) == 2:
                    self.set_values(pair=arg)
                elif isinstance(arg, collections.abc.Mapping):
                    self.set_values(dict=arg)
                else:
                    self.set_values(seq=arg)
            elif isinstance(arg, int):
                self.set_values(int_val=arg)
            else:
                print('Unsupported type {}'.format(type(arg)))
        self.dim = len(self.values)
        lengths = [self.dim] + [kwargs[key] for key in ['dim', 'size', 'length', 'len'] if key in kwargs.keys()]
        self.dim = max(lengths)
        extend(self.values, self.dim - 1)

    def set_values(self, int_val=None, seq=None, dict=None, pair=None):
        '''
        extending values for: int, seq, pair
        dict - extending or replacing depending on whether index is within size of values
        '''
        if int_val:
            self.values.extend([int_val])
        if seq:
            self.values.extend(list(seq))
        if dict:
            for k, v in dict.items():
                extend(self.values, k)
                self.values[k] = v
        if pair:
            value = pair[1]
            indices = pair[0]
            for idx in indices:
                extend(self.values, idx)
                self.values[idx] = value
        return self

    def norm(self, sqrt=True):
        """ Returns the norm (length, magnitude) of the vector """
        tmp = sum(x * x for x in self)
        if sqrt:
            return math.sqrt(tmp)
        else:
            return tmp

    def HW(self, idxs=None):
        if idxs != None:
            values = [self.values[i] for i in idxs]
        else:
            values = self.values
        return sum(map(lambda x: x != 0, values))

    def slice(self, idxs):
        return self.__class__([self.values[i] for i in idxs])

    def permute(self, idxs):
        return self.__class__([self.values[i] for i in idxs])

    def wt(self, idxs=None):
        return self.HW(idxs)

    def HW_dist(self, other):
        tmp = (self.__sub__(other) % 2)
        return tmp.wt()

    def Euclid_dist(self, other):
        tmp = (self.__sub__(other))
        return tmp.norm()

    def L1_norm(self):
        return sum(abs(x) for x in self)

    def L1_dist(self, other):
        return sum(abs(x) for x in self - other)

    def inner(self, other):
        """ Returns the dot product (inner product) of self and another vector
        """
        if issubclass(type(other), Vec):
            raise ValueError('The dot product requires another vector')
        return sum(a * b for a, b in zip(self, other))

    def __xor__(self, other):
        """ Returns the vector addition of self and other """
        if issubclass(type(other), Vec):
            xored = tuple(a ^ b for a, b in zip(self, other))
        elif isinstance(other, int):
            xored = tuple(a ^ other for a in self)
        else:
            raise ValueError("Addition with type {} not supported".format(type(other)))
        return self.__class__(xored)

    def __mul__(self, other):
        """ Returns the dot product of self and other if multiplied
            by another Vector.  If multiplied by an int or float,
            multiplies each component by other.
        """
        if issubclass(type(other), Vec):
            return self.__class__(tuple(a * b for a, b in zip(self, other)))
        elif isinstance(other, (int, float)):
            product = tuple(a * other for a in self)
            return self.__class__(product)
        else:
            raise ValueError("Multiplication with type {} not supported".format(type(other)))

    def __rmul__(self, other):
        """ Called if 4 * self for instance """
        return self.__mul__(other)

    def __truediv__(self, other):
        if issubclass(type(other), Vec):
            divided = tuple(self[i] / other[i] for i in range(len(self)))
        elif isinstance(other, (int, float)):
            divided = tuple(a / other for a in self)
        else:
            raise ValueError("Division with type {} not supported".format(type(other)))

        return self.__class__(divided)

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __floordiv__(self, other):
        if issubclass(type(other), Vec):
            divided = tuple(self[i] // other[i] for i in range(len(self)))
        elif isinstance(other, int):
            divided = tuple(a // other for a in self)
        else:
            raise ValueError("Division with type {} not supported".format(type(other)))
        return self.__class__(divided)

    def __rfloordiv__(self, other):
        return self.__truediv__(other)

    def __add__(self, other):
        """ Returns the vector addition of self and other """
        if issubclass(type(other), Vec):
            added = tuple(a + b for a, b in zip(self, other))
        elif isinstance(other, (int, float)):
            added = tuple(a + other for a in self)
        else:
            raise ValueError("Addition with type {} not supported".format(type(other)))

        return self.__class__(added)

    def __radd__(self, other):
        """ Called if 4 + self for instance """
        return self.__add__(other)

    def __sub__(self, other):
        """ Returns the vector difference of self and other """
        if issubclass(type(other), Vec):
            subbed = tuple(a - b for a, b in zip(self, other))
        elif isinstance(other, (int, float)):
            subbed = tuple(a - other for a in self)
        else:
            raise ValueError("Subtraction with type {} not supported".format(type(other)))

        return self.__class__(subbed)

    def __rsub__(self, other):
        """ Called if 4 - self for instance """
        return self.__sub__(other)

    def __iter__(self):
        return self.values.__iter__()

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __repr__(self):
        return ' '.join(map(str, self.values))

    def __mod__(self, other):
        """ Returns the vector modulo of self and other """
        if issubclass(type(other), Vec):
            remainder = tuple(a % b for a, b in zip(self, other))
        elif isinstance(other, int):
            remainder = tuple(a % other for a in self)
        elif isinstance(other, float):
            # TODO
            pass
        else:
            raise ValueError("Addition with type {} not supported".format(type(other)))

        return self.__class__(remainder)

    def __rmod__(self, other):
        return self.__mod__(other)

    def abs(self):
        return self.__class__([abs(a) for a in self])

    def __le__(self, other):
        return all([a <= b for a, b in zip(self, other)])

    def __lt__(self, other):
        return all([a < b for a, b in zip(self, other)])

    def __gt__(self, other):
        return all([a > b for a, b in zip(self, other)])

    def __ge__(self, other):
        return all([a >= b for a, b in zip(self, other)])

    def __eq__(self, other):
        return all([a == b for a, b in zip(self, other)])

    def __neq__(self, other):
        return all([a != b for a, b in zip(self, other)])

    def __lshift__(self, other):
        extend(self.values, other)
        self.dim = len(self.values)
        return self

    def __ilshift__(self, other):
        return self.__lshift__(other)

    def __rshift__(self, other):
        self.values = self.values[-other:]
        self.dim = len(self.values)
        return self

    def __irshift__(self, other):
        return self.__rshift__(other)

    def print(self, grouping=1, sep=','):
        tmp = self.values
        tmp = [''.join(map(str, tmp[i:i + grouping])) for i in range(0, len(tmp), grouping)]
        print(sep.join(tmp))




# if __name__ == "__main__":
#     vec1 = Vec(1,[2, 3], ([4, 5], 9), {7: 7, 8: 7})
#     vec2 = Vec(vec1, {1:0})
#     print(vec1, vec2, sep='\n')
#     print(vec1 ^ vec2)
#     print(vec1 % 2)
#     print(vec1 * vec2)
#     print(vec1.inner(vec2))


