class SomeClass:

    def __init__(self):
        self.data_list = []

    def __init__(self, *args):
        self.data_list = []
        self.data_list.extend(args)

    def __add__(self, other):
        if not isinstance(other, SomeClass):
            print("Нельзя сложить")
            return False
        c = SomeClass()
        for i in self.data_list:
            c.set_list(i)
        for i in other.data_list:
            c.set_list(i)
        return c

    def __lt__(self, other):  # <
        if not isinstance(other, SomeClass):
            print("Нельзя сравнить")
            return False
        return sum(self.data_list) < sum(other.data_list)

    def __le__(self, other):  # <=
        if not isinstance(other, SomeClass):
            print("Нельзя сравнить")
            return False
        return sum(self.data_list) <= sum(other.data_list)

    def __eq__(self, other):  # ==
        if not isinstance(other, SomeClass):
            print("Нельзя сравнить")
            return False
        return sum(self.data_list) == sum(other.data_list)

    def __gt__(self, other):  # >
        if not isinstance(other, SomeClass):
            print("Нельзя сравнить")
            return False
        return sum(self.data_list) > sum(other.data_list)

    def __ge__(self, other):  # >=
        if not isinstance(other, SomeClass):
            print("Нельзя сравнить")
            return False
        return sum(self.data_list) >= sum(other.data_list)

    def set_list(self, *args):
        self.data_list.extend(args)

    def print_list(self):
        print(self.data_list)


if __name__ == "__main__":
    a = SomeClass()
    a.set_list(1, 2, 3, 4)

    b = SomeClass(1, 2, 3, 4)
    b.set_list(1, 2, 3, 4)

    d = SomeClass(1, 2, 3, 4)

    a.print_list()
    b.print_list()

    c = a + b
    c.print_list()

    print(a > b, a < b, a > d, a >= d, a == d)
