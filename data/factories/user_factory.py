import random
import uuid
from datetime import datetime

from faker import Faker

fake = Faker()


class UserFactory:
    """Фабрика для создания тестовых пользователей"""

    @staticmethod
    def get_valid_email():
        """Получить случайный валидный email"""
        unique_id = f"{datetime.now().strftime('%H%M%S%f')}_{uuid.uuid4().hex[:6]}"
        return f"test_{unique_id}@test.ru"

    @staticmethod
    def get_valid_first_name():
        """Получить случайное валидное имя"""
        return fake.first_name()

    @staticmethod
    def get_valid_phone():
        """Получить случайный валидный телефон"""
        random_part = str(random.randint(1000000, 9999999))
        time_part = datetime.now().strftime('%H%M%S')[:3]
        return f"7{random_part}{time_part}"[:11]

    @staticmethod
    def create_user(**kwargs):
        """Создает пользователя с возможностью переопределения полей"""
        user = {
            'email': UserFactory.get_valid_email(),
            'first_name': UserFactory.get_valid_first_name(),
            'phone_number': UserFactory.get_valid_phone()
        }

        for key in ['email', 'first_name', 'phone_number']:
            if key in kwargs:
                user[key] = kwargs[key]

        return user

    @staticmethod
    def create_empty_user(**kwargs):
        """Создает пользователя с пустыми полями"""
        user = {
            'email': kwargs.get('email', ''),
            'first_name': kwargs.get('first_name', ''),
            'phone_number': kwargs.get('phone_number', '')
        }
        return user


user_factory = UserFactory()
