from yaml import load, SafeLoader
from sys import stdin, exit

s = ''


def rec_parse(element, indent, key=''):
    global s

    def add_string(string):
        global s
        s += ' ' * 4 * indent
        if key:
            s += f'{key} => '
        s += string
        s += '\n'

    if isinstance(element, str):
        add_string(f'"{element}"')

    elif isinstance(element, int) or isinstance(element, float):
        add_string(str(element))

    elif isinstance(element, list):
        add_string("'(")
        for el in element:
            rec_parse(el, indent + 1)
        s += ' ' * 4 * indent
        s += ')\n'

    elif isinstance(element, dict):
        add_string('{')
        comas = len(element) - 1
        for key, value in element.items():
            rec_parse(value, indent + 1, key)
            if comas > 0:
                s = s[:-1] + ',\n'
                comas -= 1

        s += ' ' * 4 * indent
        s += '}\n'


def load_yaml(text):
    try:
        data = load(text, Loader=SafeLoader)
    except:
        print('Некорректный ввод, присутствуют запрещенные символы')
        return
    if data == text:
        print('Некорректный ввод, отсутствуют структурированные данные')
        return
    return data


def main(data):
    try:
        rec_parse(data, 0)
    except:
        print('Что-то пошло не так')
        return
    print(s)


if __name__ == '__main__':
    std_input = stdin.read()
    yaml_data = load_yaml(std_input)
    main(yaml_data)
