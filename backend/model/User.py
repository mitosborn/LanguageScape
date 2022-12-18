class User:
    username: str
    email_address: str
    languages: set
    learn_sets: set

    def __init__(self, username: str, email_address: str, languages: set, learn_sets: set):
        self.username = username
        self.email_address = email_address
        self.languages = languages
        self.learn_sets = learn_sets

    @staticmethod
    def from_dict(user_dict: dict):
        return User(username=user_dict['username'], email_address=user_dict['email_address'],
                    languages=set(user_dict['languages']), learn_sets=set(user_dict['learn_sets']))
