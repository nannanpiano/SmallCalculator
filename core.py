def simple_calculate(num1, num2, operator):
    if operator == '+':
        return num1 + num2
    if operator == '-':
        return num1 - num2
    if operator == '*':
        return num1 * num2
    if operator == '/':
        return num1 / num2

def to_num(num_str):
    try:
        return int(num_str)
    except ValueError:
        return float(num_str)

def tokenize(input_str: str) -> list:
    if input_str == '':
        return []
    if input_str[0] == ' ':
        return tokenize(input_str[1:])
    if input_str[0] in ['+', '-', '*', '/', '(', ')']:
        return [input_str[0]] + tokenize(input_str[1:])
    if input_str[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        i = 0
        while i < len(input_str) and input_str[i] != '.' and input_str[i] not in ['+', '-', '*', '/', ' ', '(', ')']:
            i += 1
        if i == len(input_str):
            return [to_num(input_str[0:i])]
        elif input_str[i] in ['+', '-', '*', '/', ' ', '(', ')']:
            return [to_num(input_str[0:i])] + tokenize(input_str[i:])
        else:
            i += 1
            while i < len(input_str) and input_str[i] not in ['+', '-', '*', '/', ' ', '(', ')']:
                i += 1
            if i == len(input_str):
                return [to_num(input_str[0:i])] 
            else:
                return [to_num(input_str[0:i])] + tokenize(input_str[i:])



def calculator(token_list: list):
    simplified_list = []
    i = 0
    while i < len(token_list):
        token = token_list[i]
        if token in ['*', '/']:
            left = simplified_list.pop()
            right = token_list[i + 1]
            simplified_list.append(simple_calculate(left, right, token))
            i += 2
        else:
            simplified_list.append(token)
            i += 1

    ret = simplified_list[0]
    i = 1
    while i < len(simplified_list):
        ret = simple_calculate(ret, simplified_list[i+1], simplified_list[i])
        i += 2
    return ret

def calculator_with_buffer(token_list: list):
    buffer_list = []
    i = 0
    while i < len(token_list) and i >= 0:
        if token_list[i] == '(':
            buffer_list.append(i)
            i += 1

        elif token_list[i] == ')':
            top = buffer_list.pop()
            token_list[top:(i+1)] = [calculator(token_list[(top+1):(i)])]
            i = top
        else:
            i += 1

    return calculator(token_list)

def run():
    input_str = input('请输入：')
    while input_str != 'quit':
        token_list = tokenize(input_str)
        final = calculator_with_buffer(token_list)
        print(final)
        input_str = input('请输入：')


if __name__ == '__main__':
    run()