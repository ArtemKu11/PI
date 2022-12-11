import near_script
import folder.script as from_folder_script
import another_folder as from_folder


def print_global():
    print(f"from print_global: {a}")


def print_local():
    a = 2
    print(f"from print_local: {a}")


def change_global_in_local():
    global a
    a = 5
    print(f"from change_global_in_local: {a}")


def change_local_in_inner_local():
    a = 2
    print(f"from change_local_in_inner_local: {a}")

    def inner_local():
        nonlocal a
        a += 1
        print(f"from change_local_in_inner_local.inner_local: {a}")

    inner_local()
    print(f"from change_local_in_inner_local: {a}")


def change_global_in_inner_local():
    global a
    print(f"from change_global_in_inner_local: {a}")

    def inner_local():
        global a
        a += 1
        print(f"from change_global_in_inner_local.inner_local: {a}")

    inner_local()
    print(f"from change_global_in_inner_local: {a}")
    a += 1
    print(f"from change_global_in_inner_local: {a}")


if __name__ == "__main__":
    near_script.who_i_am()
    from_folder_script.who_i_am()
    from_folder.who_i_am()
    print()
    a = 1
    print_global()
    print_local()
    print(f"from global: {a}")
    change_global_in_local()
    print(f"from global: {a}")
    change_local_in_inner_local()
    change_global_in_inner_local()
    print(f"from global: {a}")
