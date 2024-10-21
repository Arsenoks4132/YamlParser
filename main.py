import yaml
from pprint import pprint

s = ''


def rec_parse(element, indent, key=''):
    global s
    key_used = False

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


with open('test.yaml', 'r') as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)

rec_parse(data, 0)

print(s)
