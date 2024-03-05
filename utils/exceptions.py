class RequiredField(Exception):
    def __init__(self, field: str):
        self.field = field
        super().__init__(f'Это поле является обязательным')


class AlreadyRegistered(Exception):
    def __init__(self, field: str):
        self.field = field
        super().__init__(f'Извините, {self.field} уже занято.')


class NotRegistered(Exception):
    def __init__(self, field: str):
        self.field = field
        super().__init__(f'Неправильный логин или пароль')


class NotAuthed(Exception):
    def __init__(self):
        super().__init__('Ошибка авторизации')


class PasswordDontMatching(Exception):
    def __init__(self, field: str):
        self.field = field
        super().__init__(f'Пароли не совпадают')
