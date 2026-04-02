import random

class FirstNameTestCases:
    """Тестовые данные для имени пользователя"""
    
    @staticmethod
    def get_format_valid():
        """Валидные имена по формату"""
        return [
            ("Заглавные английские буквы", "IVAN"),
            ("Строчные английские буквы", "ivan"),
            ("Имя с заглавной буквы", "Ivan"),
            ("Имя с дефисом", "Анна-Мария"),
            ("Имя с апострофом", "Д'Артаньян"),
            ("Двойное имя с пробелом", "Анна Мария"),
            ("Имя с точкой", "C. Джонсон"),
            ("Заглавные русские буквы", "ИВАН"),
            ("Строчные русские буквы", "иван"),
            ("Имя с цифрами", "Ivan123"),
        ]
    
    @staticmethod
    def get_format_invalid():
        """Невалидные имена по формату"""
        return [
            ("Имя со спецсимволами", "Iva$#n"),
            ("Пробел в начале строки", " Иван"),
            ("Пробел в конце строки", "Иван "),
            ("Имя с иероглифами", "山田"),
            ("Имя с арабскими символами", "محمد"),
        ]
    
    @staticmethod
    def get_length_valid():
        """Валидные имена по длине"""
        return [
            ("Минимальная длина (2 символа)", "Ян"),
            ("Максимальная длина (50 символов)", "Иван" * 12 + "Ив"),
        ]
    
    @staticmethod
    def get_length_invalid():
        """Невалидные имена по длине"""
        return [
            ("Пустая строка", ""),
            ("Только пробелы", "   "),
            ("Более максимального (51 символ)", "Иван" * 12 + "Ива"),
        ]
    
    @staticmethod
    def get_required_valid():
        """Валидные имена по обязательности"""
        return [
            ("Поле заполнено", "Иван"),
        ]
    
    @staticmethod
    def get_required_invalid():
        """Невалидные имена по обязательности"""
        return [
            ("Пустой ввод", ""),
            ("Только пробелы", "   "),
            ("None значение", None),
        ]
    
    @staticmethod
    def get_all_valid():
        """Все валидные имена из всех категорий (только значения)"""
        valid = []
        for category in [
            FirstNameTestCases.get_format_valid(),
            FirstNameTestCases.get_length_valid(),
            FirstNameTestCases.get_required_valid()
        ]:
            for _, name in category:
                if name is not None and name not in valid:
                    valid.append(name)
        return valid
    
    @staticmethod
    def get_all_invalid():
        """Все невалидные имена из всех категорий (только значения)"""
        invalid = []
        for category in [
            FirstNameTestCases.get_format_invalid(),
            FirstNameTestCases.get_length_invalid(),
            FirstNameTestCases.get_required_invalid()
        ]:
            for _, name in category:
                if name is not None and name not in invalid:
                    invalid.append(name)
        return invalid
    
    @staticmethod
    def get_all_cases():
        """Все тестовые кейсы с ожидаемыми результатами"""
        cases = []
        for desc, name in FirstNameTestCases.get_format_valid():
            cases.append((desc, name, True))
        for desc, name in FirstNameTestCases.get_length_valid():
            cases.append((desc, name, True))
        for desc, name in FirstNameTestCases.get_required_valid():
            cases.append((desc, name, True))
        
        for desc, name in FirstNameTestCases.get_format_invalid():
            cases.append((desc, name, False))
        for desc, name in FirstNameTestCases.get_length_invalid():
            cases.append((desc, name, False))
        for desc, name in FirstNameTestCases.get_required_invalid():
            cases.append((desc, name, False))
        
        return cases
    
    @staticmethod
    def get_valid_name():
        """Получить случайное валидное имя"""
        return random.choice(FirstNameTestCases.get_all_valid())
    
    @staticmethod
    def get_invalid_name():
        """Получить случайное невалидное имя"""
        return random.choice(FirstNameTestCases.get_all_invalid())
    
    @staticmethod
    def get_by_category(category_name, validity=None):
        """Получить кейсы по категории"""
        category_map = {
            'format': (FirstNameTestCases.get_format_valid, FirstNameTestCases.get_format_invalid),
            'length': (FirstNameTestCases.get_length_valid, FirstNameTestCases.get_length_invalid),
            'required': (FirstNameTestCases.get_required_valid, FirstNameTestCases.get_required_invalid),
        }
        
        if category_name not in category_map:
            return []
        
        valid_func, invalid_func = category_map[category_name]
        
        if validity == 'valid':
            return valid_func()
        elif validity == 'invalid':
            return invalid_func()
        else:
            return valid_func() + invalid_func()

first_name_test_cases = FirstNameTestCases()