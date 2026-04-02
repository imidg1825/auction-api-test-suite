import random

class PhoneNumberTestCases:
    """Тестовые данные для номера телефона"""
    
    @staticmethod
    def get_format_valid():
        """Валидные номера по формату"""
        return [
            ("Российский номер с 7", "71234567890"),
            ("Международный формат", "12345678901"),
        ]
    
    @staticmethod
    def get_format_invalid():
        """Невалидные номера по формату"""
        return [
            ("Номер без кода страны", "9234567890"),
            ("Российский номер с 8", "81234567890"),
            ("Российский номер с +7", "+71234567890"),
            ("Буквы в номере", "7123456abcd"),
            ("Спецсимволы", "7123456!@#$"),
            ("Пробелы в номере", "712 345 678 90"),
            ("Дефисы в номере", "712-345-678-90"),
            ("Скобки в номере", "7(123)4567890"),
            ("Начинается не с цифры или +", "a1234567890"),
        ]
    
    @staticmethod
    def get_length_valid():
        """Валидные номера по длине"""
        return [
            ("Минимальная длина (10 цифр)", "1234567890"),
            ("Максимальная длина (15 цифр)", "123456789012345"),
        ]
    
    @staticmethod
    def get_length_invalid():
        """Невалидные номера по длине"""
        return [
            ("Меньше 10 цифр", "123456789"),
            ("Больше 15 цифр", "1234567890123456"),
            ("Пустая строка", ""),
            ("Только пробелы", "          "),
        ]
    
    @staticmethod
    def get_required_valid():
        """Валидные номера по обязательности"""
        return [
            ("Заполнено", "71234567890"),
        ]
    
    @staticmethod
    def get_required_invalid():
        """Невалидные номера по обязательности"""
        return [
            ("Пустой ввод", ""),
            ("Только пробелы", "   "),
            ("None значение", None),
        ]
    
    @staticmethod
    def get_all_valid():
        """Все валидные номера (только значения)"""
        valid = []
        for category in [
            PhoneNumberTestCases.get_format_valid(),
            PhoneNumberTestCases.get_length_valid(),
            PhoneNumberTestCases.get_required_valid()
        ]:
            for _, phone in category:
                if phone is not None and phone not in valid:
                    valid.append(phone)
        return valid
    
    @staticmethod
    def get_all_invalid():
        """Все невалидные номера (только значения)"""
        invalid = []
        for category in [
            PhoneNumberTestCases.get_format_invalid(),
            PhoneNumberTestCases.get_length_invalid(),
            PhoneNumberTestCases.get_required_invalid()
        ]:
            for _, phone in category:
                if phone is not None and phone not in invalid:
                    invalid.append(phone)
        return invalid
    
    @staticmethod
    def get_all_cases():
        """Все тестовые кейсы с ожидаемыми результатами"""
        cases = []
        # Валидные
        for desc, phone in PhoneNumberTestCases.get_format_valid():
            cases.append((desc, phone, True))
        for desc, phone in PhoneNumberTestCases.get_length_valid():
            cases.append((desc, phone, True))
        for desc, phone in PhoneNumberTestCases.get_required_valid():
            cases.append((desc, phone, True))
        
        # Невалидные
        for desc, phone in PhoneNumberTestCases.get_format_invalid():
            cases.append((desc, phone, False))
        for desc, phone in PhoneNumberTestCases.get_length_invalid():
            cases.append((desc, phone, False))
        for desc, phone in PhoneNumberTestCases.get_required_invalid():
            cases.append((desc, phone, False))
        
        return cases
    
    @staticmethod
    def get_valid_phone():
        """Получить случайный валидный номер"""
        return random.choice(PhoneNumberTestCases.get_all_valid())
    
    @staticmethod
    def get_invalid_phone():
        """Получить случайный невалидный номер"""
        return random.choice(PhoneNumberTestCases.get_all_invalid())
    
    @staticmethod
    def get_by_description(description):
        """Найти номер по описанию"""
        for desc, phone, _ in PhoneNumberTestCases.get_all_cases():
            if desc == description:
                return phone
        return None

phone_number_test_cases = PhoneNumberTestCases()