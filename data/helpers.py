class TestHelpers:
    @staticmethod
    def print_request(user_data):
        """Вывод данных запроса"""
        if user_data is None:
            print("Тело запроса: отсутствует")
            return
            
        print(f"Email: {user_data.get('email', 'не указан')}")
        print(f"First Name: {user_data.get('first_name', 'не указан')}")
        print(f"Phone: {user_data.get('phone_number', 'не указан')}")
    
    @staticmethod
    def handle_response(response, expected_status, check_func=None):
        """Обработка ответа"""
        print(f"\nПолучен статус: {response.status_code}")
        assert response.status_code == expected_status, \
            f"Ожидался {expected_status}, получен {response.status_code}"
        
        try:
            response_data = response.json()
            print(f"Ответ сервера: {response_data}")
            if check_func:
                check_func(response_data)
            return response_data
        except Exception as e:
            print(f"Ошибка при парсинге ответа: {e}")
            raise

    @staticmethod
    def print_test_header(test_name):
        """Вывод заголовка теста"""
        print(f"ТЕСТ: {test_name}")

    @staticmethod
    def print_test_footer():
        """Вывод подвала теста"""
        print("✅ ТЕСТ ПРОЙДЕН!")

helpers = TestHelpers()