class CalcError(Exception):
    pass

OPERATORS = ['+', '-', '*', '/']
SYMBOLS = OPERATORS + ['(', ')']
NUMBERS_CHARS = '0123456789.'

# 简单四则运算，并检测除数不为0
def simple_calculate(num1, num2, operator):
    if operator == '+':
        return num1 + num2
    if operator == '-':
        return num1 - num2
    if operator == '*':
        return num1 * num2
    if operator == '/':
        if num2 == 0:
            raise CalcError('除数不能为零')
        return num1 / num2

# 将字符转换为整数/浮点数
def to_num(num_str):
    try:
        return int(num_str)
    except ValueError:
        pass
    try:
        return float(num_str)
    except ValueError:
        raise CalcError(f'无法识别的数字：{num_str}')

'''
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
'''
# 将输入切成列表
def tokenize(input_str: str) -> list:
    if input_str == '':
        return []
    first = input_str[0]

    if first.isspace():
        return tokenize(input_str[1:])
    
    if first in SYMBOLS:
        return [first] + tokenize(input_str[1:])
    
    if first in NUMBERS_CHARS:
        i = 0
        while i < len(input_str) and input_str[i] in NUMBERS_CHARS:
            i += 1
        return [to_num(input_str[:i])] + tokenize(input_str[i:])

    if first.isalpha() or first == '_':
        i = 0
        while i < len(input_str) and (input_str[i].isalnum() or input_str[i] == '_'):
            i += 1
        return [input_str[:i]] + tokenize(input_str[i:])
    
    raise CalcError(f'非法字符：{first}')

# 计算单个括号内的内容
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

# 计算整个表达式
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

# 检查表达式是否有语法错误
def check_syntax(token_list: list):
    if not token_list:
        raise CalcError('输入为空')
    expect_number = True
    depth = 0
    for token in token_list:
        if token == '(':
            if not expect_number:
                raise CalcError('左括号前面缺少运算符')
            depth += 1
        elif token == ')':
            if expect_number:
                raise CalcError('右括号前面缺少数字')
            depth -= 1
            if depth < 0:
                raise CalcError('括号不配对：多了右括号')
        elif token in OPERATORS:
            if expect_number:
                raise CalcError(f'运算符 {token} 前面缺少数字')
            expect_number = True
        else:
            # 变量名也会走这个分支
            if not expect_number:
                raise CalcError(f'数字 {token} 前面缺少运算符')
            expect_number = False
    if expect_number:
        raise CalcError('算式不完整')
    if depth > 0:
        raise CalcError('括号不配对：缺少右括号')

# 把token_list的变量名替换成相应的值
def replace_variables(token_list: list, variables: dict) -> list:
    result = []
    for token in token_list:
        if isinstance(token, str) and token not in SYMBOLS:
            if token not in variables:
                raise CalcError(f'变量未定义：{token}')
            result.append(variables[token])
        else:
            result.append(token)
    return result

# 计算一个算式字符串
def evaluate(input_str: str, variables: dict):
    token_list = tokenize(input_str)
    check_syntax(token_list)
    token_list = replace_variables(token_list, variables)
    return calculator_with_buffer(token_list)

# 处理赋值语句，返回变量名和值
def assign(input_str: str, variables: dict):
    name, expr = input_str.split('=', 1)
    name = name.strip()
    if not name.isidentifier():
        raise CalcError(f'变量名不合法: {name}')
    value = evaluate(expr, variables)
    variables[name] = value
    return name, value



# 启动计算器
def run():
    variables = {}
    input_str = input('请输入：')
    while input_str != 'quit':
        try:
            if '=' in input_str:
                name, value = assign(input_str, variables)
                print(f'{name} = {value}')
            else:
                print(evaluate(input_str, variables))
        except CalcError as e:
            print('错误：', e)
        input_str = input('请输入：')


if __name__ == '__main__':
    run()