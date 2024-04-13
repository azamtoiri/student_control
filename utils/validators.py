import re


class PasswordStrengthChecker:
    def __init__(self, password):
        self.password = password
        self.common_passwords = ["password", "1234", "admin", "qwerty"]
        self.complexity_regex = re.compile(
            r"(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])"
        )

    def length_check(self):
        length = len(self.password)
        if 0 < length < 8:
            return 0
        elif 8 <= length < 12:
            return 1
        elif 12 <= length < 16:
            return 2
        elif length >= 16:
            return 3

    def character_check(self):
        characters = set(self.password)
        lower_case = set("abcdefghijklmnopqrstuvwxyz")
        upper_case = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        digits = set("0123456789")
        special_characters = set("!@#$%^&*()_+-=[]{};:,.<>/?`~")

        score = 0
        if any(char in lower_case for char in characters):
            score += 1
        if any(char in upper_case for char in characters):
            score += 1
        if any(char in digits for char in characters):
            score += 1
        if any(char in special_characters for char in characters):
            score += 1

        if score == 1:
            return 0
        elif score == 2:
            return 1
        elif score == 3:
            return 2
        elif score == 4:
            return 3

    def repeat_check(self):
        if len(self.password) == 0:
            return 2
        else:
            for i in range(len(self.password) - 2):
                if self.password[i] == self.password[i + 1] == self.password[i + 2]:
                    return 0
            return 1

    def sequential_check(self):
        if len(self.password) == 0:
            return 2
        else:
            for i in range(len(self.password) - 2):
                if (
                        self.password[i: i + 3].isdigit()
                        or self.password[i: i + 3].islower()
                        or self.password[i: i + 3].isupper()
                ):
                    return 0
            return 1


class EmailValidator:
    def __init__(self, email):
        self.email = email

    def validate(self) -> bool:
        # Регулярное выражение для валидации email-адреса
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if re.match(pattern, self.email):
            return True  # Валидация прошла успешно
        else:
            return False
