class Constraints:
    def __init__(self):
        pass

    def censor(self, config, keep=[]):        
        return dict((key, config[key]) for key in keep if key in config)

