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
                var_name = lexer.get_token()
                if lexer.get_token() == '=':
                    value = ''.join(lexer)
                    content.update({var_name: value})
        return content

    def update(self, file_path, data={}):
        import in_place
        if len(data) == 0:
            return

        with in_place.InPlace(file_path) as file:
            for line in file:
                for var_name, value in data.items():
                    # print("looking for {} in {}".format(var_name, line))
                    if line.startswith(var_name):
                        file.write("{}={}\n".format(var_name, value))
                    else:
                        file.write(line)