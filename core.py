def get_input_and_print():
    a = input('请输入:')
    if a == 'quit':
        return 0
    print(a)
    return 1



if __name__ == '__main__':
    get_input_and_print()
    while get_input_and_print():
        pass