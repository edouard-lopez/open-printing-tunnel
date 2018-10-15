import shlex

import in_place


class ConfigEditor:
    def __init__(self):
        self.config = {}

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
                content.update(self.drop_keyword(line))
        return content

    def update(self, file_path, data={}):
        if len(data) == 0:
            return

        with in_place.InPlace(file_path) as file:
            for line in file:
                for var_name, value in data.items():
                    if '{}='.format(var_name) in line:
                        file.write("{}={}\n".format(var_name, value))  # /!\ remove 'declare --'
                    else:
                        file.write(line)

    def drop_keyword(self, line):
        bash_declaration_keyword = 'declare'  # e.g.: declare -- FOO="bar"

        assert len(line) > 0, 'Line should not be empty'

        parsed_line = list(shlex.shlex(line))
        if parsed_line[0] == bash_declaration_keyword:
            parsed_line = parsed_line[3:]

        lexer = shlex.shlex(''.join(parsed_line))

        var_name = lexer.get_token()
        drop_equal = lexer.get_token()

        if var_name == 'ForwardPort':  # special treat for arrays
            value = ''.join(lexer).replace('"[', '" [')
        else:
            value = ' '.join(lexer)

        return dict({var_name: value})
