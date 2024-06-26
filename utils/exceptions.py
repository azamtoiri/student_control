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


class DontHaveGrades(Exception):
    ...


class UserAlreadySubscribed(Exception):
    ...


class UserDontHaveGrade(Exception):
    ...


class PasswordLengthIsWeak(Exception):
    def __init__(self, field: str):
        self.field = field
        super().__init__(f'Пароль должен иметь больше 8 символов')


class PasswordCharacterIsWeak(Exception):
    def __init__(self, field: str):
        self.field = field
        super().__init__(f'Пароль должен один специальный символ')


class WrongEmail(Exception):
    def __init__(self, field: str):
        self.field = field
        super().__init__(f'Не корректный формат email адреса')
