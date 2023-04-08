class InvalidTranslation(Exception):

    def __init__(self, action, param):
        Exception.__init__(self)
        self.message = f'{action} missing parameter: {param}'

    def to_dict(self):
        rv = dict()
        rv['message'] = self.message
        return rv
