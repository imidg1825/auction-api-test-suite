import re
import random


class EmailTestCases:
    @staticmethod
    def get_named_valid():
        """Валидные email по названию/формату"""
        return [
            ("Заглавные английские буквы", "TEST@mail.ru"),
            ("Строчные английские буквы", "test@mail.ru"),
            ("Цифры в имени", "Test1@mail.ru"),
            ("Цифры в домене", "Test@mail1.ru"),
            ("Точка в имени", "Test.test@mail.ru"),
            ("Точка в домене", "Test@mail.mail.ru"),
            ("Подчеркивание в имени", "Test_Test@mail.ru"),
            ("Тире в имени", "Test-Test@mail.ru"),
            ("Тире в домене", "Test@mail-mail.ru"),
            ("Плюс в имени", "test+test@mail.ru"),  # Некоторые API разрешают
        ]

    @staticmethod
    def get_named_invalid():
        """Невалидные email по названию/формату"""
        return [
            ("Заглавные русские буквы", "ТЕСТ@mail.ru"),
            ("Строчные русские буквы", "тест@mail.ru"),
            ("Подчеркивание в домене", "Test@mail_mail.ru"),
            ("Пробел в имени", "Test test@mail.ru"),
            ("Пробел в домене", "Test@mail mail.ru"),
            ("Иероглифы в имени", "福@mail.ru"),
            ("Без точки в домене", "Test@mailru"),
            ("Без имени", "@mail.ru"),
            ("Без домена", "Test@"),
            ("Домен 1 буква", "Test@mail.r"),
            ("Отсутствие @", "Testmail.ru"),
            ("Апостроф в имени", "test'test@mail.ru"),
            ("Кавычки в имени", '"test"@mail.ru'),
            ("Две точки подряд", "test..test@mail.ru"),
            ("Точка в начале", ".test@mail.ru"),
            ("Точка в конце имени", "test.@mail.ru"),
            ("Несколько @", "test@mail@ru"),
            ("Спецсимволы", "test!#$%&'*@mail.ru"),
            ("Домен с дефисом в начале", "test@-mail.ru"),
            ("Домен с дефисом в конце", "test@mail-.ru"),
            ("Две @@ из документации", ".@@.ru"),
            ("Арабские символы", "اختبار@mail.ru"),
        ]

    @staticmethod
    def get_length_valid():
        """Валидные email по длине"""
        return [
            ("Минимальная длина (6 символов)", "a@b.ru"),
            ("254 символа (макс)", "a" * 246 + "@mail.ru"),
            ("Минимальная локальная часть (1 символ)", "a@mail.ru"),
            ("Минимальный домен (1 символ)", "test@a.ru"),
            ("Максимальная локальная часть (64 символа)", "a" * 64 + "@mail.ru"),
            ("Максимальный домен (249 символов)", "a@" + "a" * 249 + ".ru"),
            (
                "Максимальная общая длина (254 символа)",
                "a" * 63 + "@" + "b" * 187 + ".co",
            ),
            ("Локальная часть 63 + домен 187", "a" * 63 + "@" + "b" * 187 + ".ru"),
            ("Локальная часть 64 + домен 186", "a" * 64 + "@" + "b" * 186 + ".co"),
        ]

    @staticmethod
    def get_length_invalid():
        """Невалидные email по длине"""
        return [
            ("Менее 6 символов", "a@b.c"),
            ("Более 254 символов", "a" * 247 + "@mail.ru"),
            ("Пустая строка", ""),
            ("Локальная часть 65 символов (превышение)", "a" * 65 + "@mail.ru"),
            ("Домен 250 символов + превышение", "test@" + "a" * 250 + ".ru"),
            ("Общая длина 255 символов (превышение)", "a" * 64 + "@" + "b" * 190),
            ("Пустая локальная часть", "@mail.ru"),
            ("Пустой домен", "test@"),
            ("Отсутствует @", "testmail.ru"),
            ("Домен без точки", "test@mailru"),
            ("Точка в конце домена", "test@mail.ru."),
            ("Домен начинается с точки", "test@.mail.ru"),
            ("Домен заканчивается дефисом", "test@mail-.ru"),
            ("Домен начинается с дефиса", "test@-mail.ru"),
            ("Точка в начале локальной части", ".test@mail.ru"),
            ("Точка в конце локальной части", "test.@mail.ru"),
            ("Две точки подряд в локальной части", "test..test@mail.ru"),
        ]

    @staticmethod
    def get_required_valid():
        """Валидные email по обязательности"""
        return [
            ("Заполнено", "Test@mail.ru"),
        ]

    @staticmethod
    def get_required_invalid():
        """Невалидные email по обязательности"""
        return [
            ("Пустой ввод", ""),
            ("Только пробелы", "   "),
            ("None значение", None),
        ]

    @staticmethod
    def get_all_valid():
        """Все валидные email из всех категорий (только значения)"""
        valid = []
        for category in [
            EmailTestCases.get_named_valid(),
            EmailTestCases.get_length_valid(),
            EmailTestCases.get_required_valid(),
        ]:
            for _, email in category:
                if email is not None and email not in valid:
                    valid.append(email)
        return valid

    @staticmethod
    def get_all_invalid():
        """Все невалидные email из всех категорий (только значения)"""
        invalid = []
        for category in [
            EmailTestCases.get_named_invalid(),
            EmailTestCases.get_length_invalid(),
            EmailTestCases.get_required_invalid(),
        ]:
            for _, email in category:
                if email is not None and email not in invalid:
                    invalid.append(email)
        return invalid

    @staticmethod
    def get_all_cases():
        """Все тестовые кейсы с ожидаемыми результатами"""
        cases = []
        cases.extend(EmailTestCases.get_named_valid())
        cases.extend(EmailTestCases.get_named_invalid())
        cases.extend(EmailTestCases.get_length_valid())
        cases.extend(EmailTestCases.get_length_invalid())
        cases.extend(EmailTestCases.get_required_valid())
        cases.extend(EmailTestCases.get_required_invalid())
        return cases

    @staticmethod
    def get_valid_email():
        """Получить валидный email"""
        return random.choice(EmailTestCases.get_all_valid())

    @staticmethod
    def get_invalid_email():
        """Получить невалидный email"""
        return random.choice(EmailTestCases.get_all_invalid())

    @staticmethod
    def get_by_category_email(category_name, validity=None):
        """Получить кейсы по категории"""
        category_map = {
            "named": (EmailTestCases.get_named_valid, EmailTestCases.get_named_invalid),
            "length": (
                EmailTestCases.get_length_valid,
                EmailTestCases.get_length_invalid,
            ),
            "required": (
                EmailTestCases.get_required_valid,
                EmailTestCases.get_required_invalid,
            ),
        }

        if category_name not in category_map:
            return []

        valid_func, invalid_func = category_map[category_name]

        if validity == "valid":
            return valid_func()
        elif validity == "invalid":
            return invalid_func()
        else:
            return valid_func() + invalid_func()


email_test_cases = EmailTestCases()
