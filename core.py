def calculate(num1, num2, operator):
    if operator == '+':
        return num1 + num2
    if operator == '-':
        return num1 - num2
    if operator == '*':
        return num1 * num2
    if operator == '/':
        return num1 / num2

def parser(input_str: str):
    input_split_list = input_str.split()
    num1, num2 = int(input_split_list[0]), int(input_split_list[2])
    return num1, num2, input_split_list[1]

def run():
    input_str = input('请输入：')
    while input_str != 'quit':
        num1, num2, operator = parser(input_str)
        final = calculate(num1, num2, operator)
        print(final)
        input_str = input('请输入：')

if __name__ == '__main__':
    run()