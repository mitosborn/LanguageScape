from model.Translation import Translation


class InvalidTranslationException(Exception):

    def __init__(self, translation: Translation):
        self.message = f"Answer not in original text \nOriginal text: {translation.original_text}\nAnswer: {translation.choices[translation.answer]}\n"
        super().__init__(self.message)
