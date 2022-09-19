class MyClass():
    list = []
    tuple = ()
    set = set()
    dict = {}
    var = [list, tuple, set, dict]
    def set_list(self, *args):
        self.list.extend(args)
    def set_tuple(self, *args):
        if self.tuple == ():
            self.tuple = args
        else:
            print('Кортеж невозможно изменить')
    def set_set(self, *args):
        self.set.update(args)
    def set_dict(self, **kwargs):
        self.dict.update(kwargs)
    def print_all(self):
        print(self.list, self.tuple, self.set, self.dict, sep = '\n')
    def find_elem(self, elem):
        for i in [self.list, self.tuple, self.set, self.dict]:
            if i == self.dict:
                if elem in self.dict.keys() or elem in self.dict.values():
                    print(i)
            elif elem in i:
                print(i)
b = MyClass()
b.set_set(1)
b.set_tuple(1)
b.set_list(1)
b.set_dict(a = 2)
b.find_elem(1)