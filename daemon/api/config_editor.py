import re
import shlex

import in_place


class ConfigEditor:
    def __init__(self):
        self.config = {}
        self.BASH_INTEGER_DECLARATION = '-i'
        self.BASH_STRING_DECLARATION = '--'
        self.BASH_ARRAY_DECLARATION = '-a'

    def load(self, file_path):
        """
            Warning:
            * multilines vlexariable like array aren't parse correctly
            * assignation statement are parse despite invalid syntax (spaces between equal sign) 
        """
        content = {}

        with open(file_path) as file:
            for line in file:
                line = line.strip().replace('\n', '')
                if line.startswith('#') or len(line) == 0:
                    continue
                content.update(self.parse(line))
        return content

    def update(self, file_path, data={}):
        if len(data) == 0:
            return

        with in_place.InPlace(file_path) as file:
            for line in file:
                for name, value in data.items():
                    if '{}='.format(name) in line:
                        file.write('{}\n'.format(self.edit(line, name, value)))
                    else:
                        file.write(line)

    def edit(self, line, name, value):
        declaration = re.compile(r'(declare\s+(-[ia-]))\s+').match(line)
        declare = declaration.group(1) if declaration else ''
        declared_as = declaration.group(2) if declaration else self.BASH_STRING_DECLARATION

        value = self.cast(value, declared_as)

        return "{declare} {name}={value}".format(declare=declare, name=name, value=value)

    def parse(self, line):
        bash_declaration_keyword = 'declare'  # e.g.: declare -- FOO="bar"

        assert len(line) > 0, 'Line should not be empty'

        parsed_line = list(shlex.shlex(line))
        declaration = self.BASH_STRING_DECLARATION
        if parsed_line[0] == bash_declaration_keyword:
            declaration = ''.join(parsed_line[1:3])
            parsed_line = parsed_line[3:]

        lexer = shlex.shlex(''.join(parsed_line))
        var_name = lexer.get_token()
        drop_equal = lexer.get_token()

        if var_name == 'ForwardPort':  # special treat for arrays
            value = ''.join(lexer).replace('"[', '" [')
        else:
            value = self.cast(' '.join(lexer), declaration)

        return dict({var_name: value})

    def cast(self, value, declared_as):
        if declared_as == self.BASH_INTEGER_DECLARATION:
            value = self.cast_to_int(value)
        elif declared_as == self.BASH_STRING_DECLARATION:
            value = value.replace('"', '') if isinstance(value, str) else value

        return value

    def cast_to_int(self, value):
        if isinstance(value, str):
            return int(float(value.replace('"', '') or 0))

        return value
