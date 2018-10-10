import shlex 
 
class ConfigEditor:
    def __init__(self):
        self.config = {}

    def load(self, file_path):
        """
            Warning:
            * multilines variable like array aren't parse correctly
            * assignation statement are parse despite invalid syntax (spaces between equal sign) 
        """
        content = {}

        with open(file_path) as file:
            for line in file:
                lexer = shlex.shlex(line)
                varname = lexer.get_token()
                if lexer.get_token() == '=':
                    value = ''.join(lexer)
                    content.update({varname: value})
        return content
