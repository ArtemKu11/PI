def foo():
    print("foo text")


def decorator(foo_to_decorate):
    def decorated_foo():
        print("before foo text")
        foo_to_decorate()
        print("after foo text")

    return decorated_foo


@decorator
def foo2():
    print("foo2 text")


if __name__ == "__main__":
    foo()
    print()
    foo = decorator(foo)
    foo()
    print()
    foo2()
