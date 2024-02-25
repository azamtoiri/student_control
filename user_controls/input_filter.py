from flet import InputFilter


class TextOnlyInputFilterRu(InputFilter):
    """Custom Input filter with the support Russian letter *only symbols"""

    def __init__(self):
        super().__init__("^[а-яА-Яa-zA-Z]+$")
