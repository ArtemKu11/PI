class Logics:
    __lie = {0: 1,
             1: 0}
    __conj = {(0, 0): 0,
              (0, 1): 0,
              (1, 0): 0,
              (1, 1): 1}
    __disj = {(0, 0): 0,
              (0, 1): 1,
              (1, 0): 1,
              (1, 1): 1}
    __impl = {(0, 0): 1,
              (0, 1): 1,
              (1, 0): 0,
              (1, 1): 1}
    __eq = {(0, 0): 1,
            (0, 1): 0,
            (1, 0): 0,
            (1, 1): 1}
    __ineq = {(0, 0): 0,
              (0, 1): 1,
              (1, 0): 1,
              (1, 1): 0}
    __sch = {(0, 0): 1,
             (0, 1): 1,
             (1, 0): 1,
             (1, 1): 0}
    __pirs = {(0, 0): 1,
              (0, 1): 0,
              (1, 0): 0,
              (1, 1): 0}

    def lie(self, x):
        return self.__lie[x]

    def conj(self, x, y):
        return self.__conj[(x, y)]

    def disj(self, x, y):
        return self.__disj[(x, y)]

    def impl(self, x, y):  # ->
        return self.__impl[(x, y)]

    def eq(self, x, y):  # ~
        return self.__eq[(x, y)]

    def ineq(self, x, y):  # +
        return self.__ineq[(x, y)]

    def sch(self, x, y):  # |
        return self.__sch[(x, y)]

    def pirs(self, x, y):
        return self.__pirs[(x, y)]


def print_table(do_return=False):
    c = Logics()
    result = {}
    for x in range(0, 2):
        for y in range(0, 2):
            for z in range(0, 2):
                # -> c.impl
                # ~ c.eq
                # + c.ineq
                # | c.sch
                # |v c.pirs
                # c.impl(c.ineq(c.eq(x, y), z), x)
                # c.disj(c.impl(c.sch(x, y), c.pirs(y, z)), c.lie(c.impl(c.lie(x), c.lie(z))))
                # c.ineq(c.eq(x, y), c.eq(x, z))
                # c.eq(c.pirs(x, y), c.ineq(x, z))
                result[(x, y, z)] = c.disj(c.ineq(x, y), c.impl(x, c.lie(z)))  # Формулу вписывать сюда
    if not do_return:
        for key, value in result.items():
            print(f'{key} = {value}')
    else:
        return result


def make_sdnf():
    result = print_table(True)
    for key, value in result.items():
        print(f'{key} = {value}')
    sdnf = []
    dict = {0: 'X',
            1: 'Y',
            2: 'Z'}
    for key, value in result.items():
        if value == 1:
            for i in range(len(key)):
                if key[i] == 1:
                    sdnf.append(dict[i])
                else:
                    sdnf.append(f'(-{dict[i]})')
            sdnf.append(' v ')
    sdnf.pop()
    s = "".join(sdnf)
    print(f'СДНФ = {s}')


def make_sknf():
    result = print_table(True)
    sknf = []
    dict = {0: 'X',
            1: 'Y',
            2: 'Z'}
    for key, value in result.items():
        if value == 0:
            for i in range(len(key)):
                if key[i] == 1:
                    sknf.append(f'(-{dict[i]})')
                else:
                    sknf.append(dict[i])
                sknf.append('v')
            sknf.pop()
            sknf.append(' * ')
    sknf.pop()
    s = "".join(sknf)
    print(f'СКНФ = {s}')


if __name__ == "__main__":
    make_sdnf()
    make_sknf()
