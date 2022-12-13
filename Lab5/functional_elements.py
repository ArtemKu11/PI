from functools import reduce


def filter_foo(num: int):
    if num > 0:
        return True
    else:
        return False


def custom_sum(first: int, second: int):
    return first + second


class SomeClass:

    def __init__(self):
        self.__some_list = []
        self.__some_dict = dict()

    def __str__(self):
        if len(self.__some_list) == 0 and len(self.__some_dict) == 0:
            return "Атрибуты пусты"
        elif len(self.__some_dict) == 0:
            return f"{self.__some_list}"
        elif len(self.__some_list) == 0:
            return f"{self.__some_dict}"
        else:
            return f"{self.__some_list}\n{self.__some_dict}"

    def set_list(self, begin_index: int, end_index: int):
        self.__some_list = [x for x in range(begin_index, end_index)]

    def get_list(self):
        return self.__some_list

    def get_positive_list(self):
        if len(self.__some_list) == 0:
            print("Лист пуст")
        else:
            return list(filter(filter_foo, self.__some_list))

    def get_sum(self):
        if len(self.__some_list) == 0:
            print("Лист пуст")
        else:
            return reduce(custom_sum, self.__some_list)

    def set_dict(self, end_index: int):
        self.__some_dict = {x: x ** 2 for x in range(end_index)}


if __name__ == "__main__":
    a = SomeClass()
    a.set_list(-5, 5)
    # a.set_dict(8)
    print(a)

    lambda_set_list = lambda x, y, z: x.set_list(y, z)
    b = SomeClass()
    lambda_set_list(b, 1, 5)
    print(b)

    list_of_instances = [a, b]
    print(list(map(SomeClass.get_list, list_of_instances)))

    print(a.get_positive_list())
    print(a.get_sum())
