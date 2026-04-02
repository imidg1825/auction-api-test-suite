import requests

from config.settings import settings

class AuthClient:
    def __init__(self):
        self.base_url = settings.BASE_URL
        self.endpoints = settings.AUTH_ENDPOINTS
        self.token = None

    def register(self, user_data):
        url = f"{self.base_url}{self.endpoints['register']}"

        print(f"POST {url} " + "Данные: {user_data}")

        try:
            response = requests.post(
                url,
                json=user_data,
                timeout=settings.TIMEOUT
            )

            print(f"Статус: {response.status_code}")
            if response.status_code in [200, 201]:
                print(f"Ответ: {response.json()}")
            elif response.status_code == 409:
                print(f"Ошибка 409: {response.text}")
            else:
                print(f"Ошибка: {response.text}")

            return response

        except requests.exceptions.ConnectionError:
            print(f"Ошибка подключения к {url}")
            print("Убедитесь что сервер запущен!")
            raise
        except Exception as e:
            print(f"Ошибка: {e}")
            raise


auth_client = AuthClient()
