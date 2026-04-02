class Settings:
    "Настройки для тестов авторизации"
    
    # Базовый URL
    BASE_URL = "https://api.dev.ads.ktsf.ru"
    
    # Эндпоинты авторизации
    AUTH_ENDPOINTS = {
        'register': '/api/registration/',      # Регистрация
        'login': '/api/login/',                 # Авторизация
        'logout': '/api/logout/',                # Выход
        'refresh': '/api/refresh-token/',        # Обновление токена
        'send_code': '/api/send_code/'           # Создание кода подтверждения
    }
    
    TIMEOUT = 10
settings = Settings()