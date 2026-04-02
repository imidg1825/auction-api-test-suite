import json
from http import HTTPStatus

import allure
import pytest

from data.error_messages import ErrorMessages
from data.factories.user_factory import user_factory
from data.helpers import helpers
from data.test_cases.first_name_test_cases import first_name_test_cases
from data.test_cases.phone_number_test_cases import phone_number_test_cases
from data.test_cases.email_test_cases import EmailTestCases
from services.auth_service import auth_client

class TestRegistration:
    """
    Тесты регистрации пользователя /api/registration/
    """

    @allure.epic("Registration")
    @allure.feature("Auth API")
    @allure.story("Successful registration")
    @allure.title("Успешная регистрация нового пользователя")
    def test_registration_success(self):
        """Тест: Успешная регистрация нового пользователя"""
        helpers.print_test_header("Успешная регистрация")

        with allure.step("Подготовка тестовых данных"):
            user_data = user_factory.create_user()
            helpers.print_request(user_data)

        print("\nОтправляем POST запрос на /api/registration/")
        with allure.step("Отправка POST запроса на /api/registration/"):
            response = auth_client.register(user_data)

        def check_response(data):
            assert 'email' in data, "В ответе нет email"
            assert data['email'] == user_data['email'], "Email не совпадает"
            assert 'first_name' in data, "В ответе нет first_name"
            assert data['first_name'] == user_data['first_name'], "first_name не совпадает"
            assert 'phone_number' in data, "В ответе нет phone_number"
            assert data['phone_number'] == user_data['phone_number'], "phone_number не совпадает"

        with allure.step("Проверка статуса ответа"):
            print(f"\nПолучен статус: {response.status_code}")
            allure.attach(
                json.dumps(user_data, ensure_ascii=False, indent=2),
                name="request body",
                attachment_type=allure.attachment_type.JSON,
            )
            allure.attach(
                str(response.status_code),
                name="status code",
                attachment_type=allure.attachment_type.TEXT,
            )
            try:
                allure.attach(
                    json.dumps(response.json(), ensure_ascii=False, indent=2),
                    name="response body",
                    attachment_type=allure.attachment_type.JSON,
                )
            except Exception:
                allure.attach(
                    response.text,
                    name="response body",
                    attachment_type=allure.attachment_type.TEXT,
                )
            assert response.status_code == HTTPStatus.CREATED, \
                f"Ожидался {HTTPStatus.CREATED}, получен {response.status_code}"

        with allure.step("Проверка тела ответа"):
            try:
                response_data = response.json()
                print(f"Ответ сервера: {response_data}")
                check_response(response_data)
            except Exception as e:
                print(f"Ошибка при парсинге ответа: {e}")
                raise

        helpers.print_test_footer()

    @allure.epic("Registration")
    @allure.feature("Auth API")
    @allure.story("Duplicate user registration")
    @allure.title("Ошибка при повторной регистрации существующего пользователя")
    def test_registration_existent_user_failed(self):
        """Тест: Регистрация существующего пользователя"""
        helpers.print_test_header("Регистрация существующего пользователя")

        with allure.step("Подготовка тестовых данных"):
            user_data = user_factory.create_user()

        with allure.step("Первая успешная регистрация пользователя"):
            print("Первая регистрация:")
            helpers.print_request(user_data)

            print("\nОтправляем POST запрос на /api/registration/")
            response = auth_client.register(user_data)
            allure.attach(
                json.dumps(user_data, ensure_ascii=False, indent=2),
                name="request body (первая регистрация)",
                attachment_type=allure.attachment_type.JSON,
            )
            allure.attach(
                str(response.status_code),
                name="status code (первая регистрация)",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert response.status_code == HTTPStatus.CREATED, \
                f"Первая регистрация не удалась: {response.status_code}"

        with allure.step("Повторная регистрация того же пользователя"):
            print("\nПовторная регистрация:")
            helpers.print_request(user_data)
            print("\nОтправляем повторный POST запрос на /api/registration/")
            response2 = auth_client.register(user_data)

        def check_response(data):
            assert ErrorMessages.ERROR_FIELD_DETAIL in data, \
                f"В ответе нет {ErrorMessages.ERROR_FIELD_DETAIL}"
            assert data[ErrorMessages.ERROR_FIELD_DETAIL] == ErrorMessages.USER_EMAIL_EXISTS, \
                f"{ErrorMessages.ERROR_FIELD_DETAIL} не совпадает"

        with allure.step("Проверка статуса и тела ответа"):
            print(f"\nПолучен статус: {response2.status_code}")
            allure.attach(
                json.dumps(user_data, ensure_ascii=False, indent=2),
                name="request body (вторая регистрация)",
                attachment_type=allure.attachment_type.JSON,
            )
            allure.attach(
                str(response2.status_code),
                name="status code (вторая регистрация)",
                attachment_type=allure.attachment_type.TEXT,
            )
            try:
                allure.attach(
                    json.dumps(response2.json(), ensure_ascii=False, indent=2),
                    name="response body (вторая регистрация)",
                    attachment_type=allure.attachment_type.JSON,
                )
            except Exception:
                allure.attach(
                    response2.text,
                    name="response body (вторая регистрация)",
                    attachment_type=allure.attachment_type.TEXT,
                )
            assert response2.status_code == HTTPStatus.BAD_REQUEST, \
                f"Ожидался {HTTPStatus.BAD_REQUEST}, получен {response2.status_code}"
            try:
                response_data = response2.json()
                print(f"Ответ сервера: {response_data}")
                check_response(response_data)
            except Exception as e:
                print(f"Ошибка при парсинге ответа: {e}")
                raise

        helpers.print_test_footer()

    @pytest.mark.parametrize("invalid_email,description",
                             [(email, desc) for desc, email in EmailTestCases.get_named_invalid()])
    def test_registration_with_invalid_email_named(self, invalid_email, description):
        """Тест: Регистрация с невалидной почтой (форматные кейсы)"""
        helpers.print_test_header(f"Регистрация с невалидной почтой: {description}")

        user_data = user_factory.create_user(email=invalid_email)
        helpers.print_request(user_data)

        print(f"\nОтправляем POST запрос на /api/registration/ с email: {invalid_email}")
        response = auth_client.register(user_data)

        def check_response(data):
            assert ErrorMessages.ERROR_FIELD_DETAIL in data, \
                f"В ответе нет {ErrorMessages.ERROR_FIELD_DETAIL}"
            assert data[ErrorMessages.ERROR_FIELD_DETAIL] == ErrorMessages.INVALID_EMAIL, \
                f"{ErrorMessages.ERROR_FIELD_DETAIL} не совпадает"

        helpers.handle_response(response, HTTPStatus.BAD_REQUEST, check_response)
        helpers.print_test_footer()

    @pytest.mark.parametrize("invalid_email,description",
                             [(email, desc) for desc, email in EmailTestCases.get_length_invalid()])
    @allure.link("registration_invalid_email_length", name="BUG")
    @pytest.mark.xfail(reason="BUG: API returns 500 instead of 400 for invalid email length")
    def test_registration_with_invalid_email_length(self, invalid_email, description):
        """Тест: Регистрация с невалидной почтой (кейсы по длине)"""
        helpers.print_test_header(f"Регистрация с невалидной почтой: {description}")

        user_data = user_factory.create_user(email=invalid_email)
        helpers.print_request(user_data)

        print(f"\nОтправляем POST запрос на /api/registration/ с email: {invalid_email}")
        response = auth_client.register(user_data)

        def check_response(data):
            pass

        helpers.handle_response(response, HTTPStatus.BAD_REQUEST, check_response)
        helpers.print_test_footer()

    @pytest.mark.parametrize("invalid_email,description",
                             [(email, desc) for desc, email in EmailTestCases.get_required_invalid()
                              if email is not None])
    def test_registration_with_invalid_email_required(self, invalid_email, description):
        """Тест: Регистрация с невалидной почтой (обязательные поля)"""
        helpers.print_test_header(f"Регистрация с невалидной почтой: {description}")

        user_data = user_factory.create_user(email=invalid_email)
        helpers.print_request(user_data)

        print(f"\nОтправляем POST запрос на /api/registration/ с email: {invalid_email}")
        response = auth_client.register(user_data)

        def check_response(data):
            if not data:
                return
            if ErrorMessages.ERROR_FIELD_EMAIL in data:
                err = data[ErrorMessages.ERROR_FIELD_EMAIL]
                if isinstance(err, list):
                    assert err, f"{ErrorMessages.ERROR_FIELD_EMAIL} — пустой список"
                    msg = err[0]
                else:
                    msg = err
                assert isinstance(msg, str) and msg.strip(), \
                    f"{ErrorMessages.ERROR_FIELD_EMAIL} без текста: {data!r}"
                return
            assert data, "Ожидалось непустое тело ошибки"

        helpers.handle_response(response, HTTPStatus.BAD_REQUEST, check_response)
        helpers.print_test_footer()

    @pytest.mark.parametrize("invalid_first_name,description",
                             [(name, desc) for desc, name in first_name_test_cases.get_format_invalid()])
    @allure.link("registration_first_name_spaces", name="BUG")
    @pytest.mark.xfail(
        reason="BUG: API accepts first_name with leading/trailing spaces and returns 201 instead of 400"
    )
    def test_registration_with_invalid_first_name_format(self, invalid_first_name, description):
        """Тест: Регистрация с невалидным именем (форматные кейсы: цифры, спецсимволы и т.д.)"""
        helpers.print_test_header(f"Регистрация с невалидным именем: {description}")

        user_data = user_factory.create_user(first_name=invalid_first_name)
        helpers.print_request(user_data)

        print(f"\nОтправляем POST запрос на /api/registration/ с именем: '{invalid_first_name}'")
        response = auth_client.register(user_data)

        def check_response(data):
            assert ErrorMessages.ERROR_FIELD_DETAIL in data, \
                f"В ответе нет {ErrorMessages.ERROR_FIELD_DETAIL}. Ответ: {data}"

            error_msg = data[ErrorMessages.ERROR_FIELD_DETAIL]
            if isinstance(error_msg, list):
                error_msg = error_msg[0]

            assert error_msg == ErrorMessages.INVALID_FIRST_NAME, \
                f"Ожидалась ошибка '{ErrorMessages.INVALID_FIRST_NAME}', получена '{error_msg}'"

        helpers.handle_response(response, HTTPStatus.BAD_REQUEST, check_response)
        helpers.print_test_footer()

    @pytest.mark.parametrize("invalid_first_name,description",
                             [(name, desc) for desc, name in first_name_test_cases.get_length_invalid()])
    def test_registration_with_invalid_first_name_length(self, invalid_first_name, description):
        """Тест: Регистрация с невалидным именем (кейсы по длине)"""
        helpers.print_test_header(f"Регистрация с невалидным именем: {description}")

        user_data = user_factory.create_user(first_name=invalid_first_name)
        helpers.print_request(user_data)

        print(f"\nОтправляем POST запрос на /api/registration/ с именем: '{invalid_first_name}'")
        response = auth_client.register(user_data)

        def check_response(data):
            assert ErrorMessages.ERROR_FIELD_FIRST_NAME in data, \
                f"В ответе нет {ErrorMessages.ERROR_FIELD_FIRST_NAME}. Ответ: {data}"

            error_msg = data[ErrorMessages.ERROR_FIELD_FIRST_NAME]
            if isinstance(error_msg, list):
                assert error_msg, f"{ErrorMessages.ERROR_FIELD_FIRST_NAME} пустой список"
                error_msg = error_msg[0]
            assert isinstance(error_msg, str) and error_msg.strip(), \
                f"Некорректное сообщение в {ErrorMessages.ERROR_FIELD_FIRST_NAME}: {error_msg!r}"

        helpers.handle_response(response, HTTPStatus.BAD_REQUEST, check_response)
        helpers.print_test_footer()

    @pytest.mark.parametrize("invalid_first_name,description",
                             [(name, desc) for desc, name in first_name_test_cases.get_required_invalid()
                              if name is not None])
    def test_registration_with_invalid_first_name_required(self, invalid_first_name, description):
        """Тест: Регистрация с невалидным именем (обязательные поля: пусто, пробелы, None)"""
        helpers.print_test_header(f"Регистрация с невалидным именем: {description}")

        user_data = user_factory.create_user(first_name=invalid_first_name)
        helpers.print_request(user_data)

        print(f"\nОтправляем POST запрос на /api/registration/ с именем: '{invalid_first_name}'")
        response = auth_client.register(user_data)

        def check_response(data):
            assert ErrorMessages.ERROR_FIELD_FIRST_NAME in data, \
                f"В ответе нет {ErrorMessages.ERROR_FIELD_FIRST_NAME}. Ответ: {data}"

            error_msg = data[ErrorMessages.ERROR_FIELD_FIRST_NAME]
            if isinstance(error_msg, list):
                assert error_msg, f"{ErrorMessages.ERROR_FIELD_FIRST_NAME} пустой список"
                error_msg = error_msg[0]
            assert isinstance(error_msg, str) and error_msg.strip(), \
                f"Некорректное сообщение в {ErrorMessages.ERROR_FIELD_FIRST_NAME}: {error_msg!r}"

        helpers.handle_response(response, HTTPStatus.BAD_REQUEST, check_response)
        helpers.print_test_footer()

    @pytest.mark.parametrize("invalid_phone,description",
                             [(phone, desc) for desc, phone in phone_number_test_cases.get_format_invalid()])
    def test_registration_with_invalid_phone_format(self, invalid_phone, description):
        """Тест: Регистрация с невалидным номером телефона (форматные кейсы)"""
        helpers.print_test_header(f"Регистрация с невалидным номером телефона: {description}")

        user_data = user_factory.create_user(phone_number=invalid_phone)
        helpers.print_request(user_data)

        print(f"\nОтправляем POST запрос на /api/registration/ с телефоном: '{invalid_phone}'")
        response = auth_client.register(user_data)

        def check_response(data):
            has_phone = ErrorMessages.ERROR_FIELD_PHONE in data
            has_detail = ErrorMessages.ERROR_FIELD_DETAIL in data
            assert has_phone or has_detail, (
                f"Ожидались ключи {ErrorMessages.ERROR_FIELD_PHONE} или "
                f"{ErrorMessages.ERROR_FIELD_DETAIL}. Ответ: {data}"
            )

            if has_phone:
                error_msg = data[ErrorMessages.ERROR_FIELD_PHONE]
                if isinstance(error_msg, list):
                    assert error_msg, f"{ErrorMessages.ERROR_FIELD_PHONE} — пустой список"
                    error_msg = error_msg[0]
                assert isinstance(error_msg, str) and error_msg.strip(), \
                    f"Некорректное сообщение в {ErrorMessages.ERROR_FIELD_PHONE}: {error_msg!r}"

            if has_detail:
                detail = data[ErrorMessages.ERROR_FIELD_DETAIL]
                assert isinstance(detail, str) and detail.strip(), \
                    f"Некорректное значение {ErrorMessages.ERROR_FIELD_DETAIL}: {detail!r}"

        assert response.status_code == HTTPStatus.BAD_REQUEST, \
            f"Ожидался статус 400, получен {response.status_code}"

        helpers.handle_response(response, HTTPStatus.BAD_REQUEST, check_response)
        helpers.print_test_footer()

    @pytest.mark.parametrize("invalid_phone,description",
                             [(phone, desc) for desc, phone in phone_number_test_cases.get_length_invalid()])
    def test_registration_with_invalid_phone_length(self, invalid_phone, description):
        """Тест: Регистрация с невалидным номером телефона (кейсы по длине)"""
        helpers.print_test_header(f"Регистрация с невалидным номером телефона: {description}")

        user_data = user_factory.create_user(phone_number=invalid_phone)
        helpers.print_request(user_data)

        print(f"\nОтправляем POST запрос на /api/registration/ с телефоном: '{invalid_phone}'")
        response = auth_client.register(user_data)

        def check_response(data):
            def assert_non_empty_str_or_list(value, label):
                if isinstance(value, list):
                    assert value, f"{label} — пустой список"
                    value = value[0]
                assert isinstance(value, str) and value.strip(), \
                    f"Некорректное сообщение в {label}: {value!r}"

            has_phone = ErrorMessages.ERROR_FIELD_PHONE in data
            has_detail = ErrorMessages.ERROR_FIELD_DETAIL in data
            assert has_phone or has_detail, (
                f"Ожидались ключи {ErrorMessages.ERROR_FIELD_PHONE} или "
                f"{ErrorMessages.ERROR_FIELD_DETAIL}. Ответ: {data}"
            )

            if has_phone:
                assert_non_empty_str_or_list(
                    data[ErrorMessages.ERROR_FIELD_PHONE],
                    ErrorMessages.ERROR_FIELD_PHONE,
                )
            if has_detail:
                assert_non_empty_str_or_list(
                    data[ErrorMessages.ERROR_FIELD_DETAIL],
                    ErrorMessages.ERROR_FIELD_DETAIL,
                )

        assert response.status_code == HTTPStatus.BAD_REQUEST, \
            f"Ожидался статус 400, получен {response.status_code}"

        helpers.handle_response(response, HTTPStatus.BAD_REQUEST, check_response)
        helpers.print_test_footer()

    @pytest.mark.parametrize("invalid_phone,description",
                             [(phone, desc) for desc, phone in phone_number_test_cases.get_required_invalid()
                              if phone is not None])
    def test_registration_with_invalid_phone_required(self, invalid_phone, description):
        """Тест: Регистрация с невалидным номером телефона (обязательные поля)"""
        helpers.print_test_header(f"Регистрация с невалидным номером телефона: {description}")

        user_data = user_factory.create_user(phone_number=invalid_phone)
        helpers.print_request(user_data)

        print(f"\nОтправляем POST запрос на /api/registration/ с телефоном: '{invalid_phone}'")
        response = auth_client.register(user_data)

        def check_response(data):
            def assert_non_empty_str_or_list(value, label):
                if isinstance(value, list):
                    assert value, f"{label} — пустой список"
                    value = value[0]
                assert isinstance(value, str) and value.strip(), \
                    f"Некорректное сообщение в {label}: {value!r}"

            has_phone = ErrorMessages.ERROR_FIELD_PHONE in data
            has_detail = ErrorMessages.ERROR_FIELD_DETAIL in data
            assert has_phone or has_detail, (
                f"Ожидались ключи {ErrorMessages.ERROR_FIELD_PHONE} или "
                f"{ErrorMessages.ERROR_FIELD_DETAIL}. Ответ: {data}"
            )

            if has_phone:
                assert_non_empty_str_or_list(
                    data[ErrorMessages.ERROR_FIELD_PHONE],
                    ErrorMessages.ERROR_FIELD_PHONE,
                )
            if has_detail:
                assert_non_empty_str_or_list(
                    data[ErrorMessages.ERROR_FIELD_DETAIL],
                    ErrorMessages.ERROR_FIELD_DETAIL,
                )

        assert response.status_code == HTTPStatus.BAD_REQUEST, \
            f"Ожидался статус 400, получен {response.status_code}"

        helpers.handle_response(response, HTTPStatus.BAD_REQUEST, check_response)
        helpers.print_test_footer()

    def test_registration_existent_email_new_phone(self):
        """Тест: Регистрация с существующей почтой и новым номером"""
        helpers.print_test_header("Регистрация с существующей почтой и новым номером")

        user_data1 = user_factory.create_user()
        email = user_data1['email']
        print("Первая регистрация:")
        helpers.print_request(user_data1)

        print("\nОтправляем POST запрос на /api/registration/")
        response1 = auth_client.register(user_data1)
        assert response1.status_code == HTTPStatus.CREATED, \
            f"Первая регистрация не удалась: {response1.status_code}"

        user_data2 = user_factory.create_user(email=email)
        assert user_data1['phone_number'] != user_data2['phone_number'], \
            "Телефоны должны быть разными для этого теста"

        print("\nВторая регистрация:")
        helpers.print_request(user_data2)
        print("\nОтправляем POST запрос на /api/registration/")
        response2 = auth_client.register(user_data2)

        def check_response(data):
            assert ErrorMessages.ERROR_FIELD_DETAIL in data, \
                f"В ответе нет {ErrorMessages.ERROR_FIELD_DETAIL}"
            assert data[ErrorMessages.ERROR_FIELD_DETAIL] == ErrorMessages.USER_EMAIL_EXISTS, \
                f"{ErrorMessages.ERROR_FIELD_DETAIL} не совпадает"

        helpers.handle_response(response2, HTTPStatus.BAD_REQUEST, check_response)
        helpers.print_test_footer()

    def test_registration_existent_phone_new_email(self):
        """Тест: Регистрация с существующим номером телефона и новой почтой"""
        helpers.print_test_header("Регистрация с существующим номером телефона и новой почтой")

        user_data1 = user_factory.create_user()
        phone_number = user_data1['phone_number']
        print("Первая регистрация:")
        helpers.print_request(user_data1)

        print("\nОтправляем POST запрос на /api/registration/")
        response1 = auth_client.register(user_data1)
        assert response1.status_code == HTTPStatus.CREATED, \
            f"Первая регистрация не удалась: {response1.status_code}"

        user_data2 = user_factory.create_user(phone_number=phone_number)
        assert user_data1['email'] != user_data2['email'], \
            "Почты должны быть разными для этого теста"

        print("\nВторая регистрация:")
        helpers.print_request(user_data2)
        print("\nОтправляем POST запрос на /api/registration/")
        response2 = auth_client.register(user_data2)

        def check_response(data):
            has_detail = ErrorMessages.ERROR_FIELD_DETAIL in data
            has_phone = ErrorMessages.ERROR_FIELD_PHONE in data
            assert has_detail or has_phone, (
                f"Ожидались ключи {ErrorMessages.ERROR_FIELD_DETAIL} или "
                f"{ErrorMessages.ERROR_FIELD_PHONE}. Ответ: {data}"
            )

            if has_detail:
                detail = data[ErrorMessages.ERROR_FIELD_DETAIL]
                assert isinstance(detail, str) and detail.strip(), \
                    f"Некорректное значение {ErrorMessages.ERROR_FIELD_DETAIL}: {detail!r}"

            if has_phone:
                error_msg = data[ErrorMessages.ERROR_FIELD_PHONE]
                if isinstance(error_msg, list):
                    assert error_msg, f"{ErrorMessages.ERROR_FIELD_PHONE} — пустой список"
                    error_msg = error_msg[0]
                assert isinstance(error_msg, str) and error_msg.strip(), \
                    f"Некорректное сообщение в {ErrorMessages.ERROR_FIELD_PHONE}: {error_msg!r}"

        helpers.handle_response(response2, HTTPStatus.BAD_REQUEST, check_response)
        helpers.print_test_footer()

    def test_registration_missing_first_name_and_phone(self):
        """Тест: Регистрация без полей имя и телефон"""
        helpers.print_test_header("Регистрация без полей имя и телефон")

        user_data = {
            'email': user_factory.get_valid_email()
        }

        helpers.print_request(user_data)
        print("\nОтправляем POST запрос на /api/registration/")
        response = auth_client.register(user_data)

        def check_response(data):
            assert response.status_code == HTTPStatus.BAD_REQUEST, \
                f"Ожидался 400, получен {response.status_code}"

        helpers.handle_response(response, HTTPStatus.BAD_REQUEST, check_response)
        helpers.print_test_footer()

    def test_registration_empty_first_name_and_phone(self):
        """Тест: Регистрация с пустыми строками в полях имя и телефон"""
        helpers.print_test_header("Регистрация с пустыми строками в полях имя и телефон")

        user_data = {
            "email": user_factory.get_valid_email(),
            "first_name": "",
            "phone_number": ""
        }

        helpers.print_request(user_data)
        print("\nОтправляем POST запрос на /api/registration/")
        response = auth_client.register(user_data)

        def check_response(data):
            assert ErrorMessages.ERROR_FIELD_FIRST_NAME in data, \
                f"В ответе нет {ErrorMessages.ERROR_FIELD_FIRST_NAME}"
            first_name_error = data[ErrorMessages.ERROR_FIELD_FIRST_NAME]
            if isinstance(first_name_error, list):
                first_name_error = first_name_error[0]
            assert first_name_error == ErrorMessages.FIELD_CANNOT_BE_EMPTY, \
                f"{ErrorMessages.ERROR_FIELD_FIRST_NAME} не совпадает"

            assert ErrorMessages.ERROR_FIELD_PHONE in data, \
                f"В ответе нет {ErrorMessages.ERROR_FIELD_PHONE}"
            phone_error = data[ErrorMessages.ERROR_FIELD_PHONE]
            if isinstance(phone_error, list):
                phone_error = phone_error[0]
            assert phone_error == ErrorMessages.FIELD_CANNOT_BE_EMPTY, \
                f"{ErrorMessages.ERROR_FIELD_PHONE} не совпадает"

        helpers.handle_response(response, HTTPStatus.BAD_REQUEST, check_response)
        helpers.print_test_footer()

    @allure.epic("Registration")
    @allure.feature("Auth API")
    @allure.story("Registration with all fields empty")
    @allure.title("Ошибка при регистрации с пустыми всеми полями")
    def test_registration_all_fields_empty(self):
        """Тест: Регистрация с пустыми строками во всех полях"""
        helpers.print_test_header("Регистрация с пустыми строками во всех полях")

        with allure.step("Подготовка запроса с пустыми данными"):
            user_data = user_factory.create_empty_user()
            helpers.print_request(user_data)

        print("\nОтправляем POST запрос на /api/registration/")
        with allure.step("Отправка POST запроса на /api/registration/"):
            response = auth_client.register(user_data)

        def check_response(data):
            assert ErrorMessages.ERROR_FIELD_FIRST_NAME in data, \
                f"В ответе нет {ErrorMessages.ERROR_FIELD_FIRST_NAME}"
            first_name_error = data[ErrorMessages.ERROR_FIELD_FIRST_NAME]
            if isinstance(first_name_error, list):
                first_name_error = first_name_error[0]
            assert first_name_error == ErrorMessages.FIELD_CANNOT_BE_EMPTY, \
                f"{ErrorMessages.ERROR_FIELD_FIRST_NAME} не совпадает"

            assert ErrorMessages.ERROR_FIELD_PHONE in data, \
                f"В ответе нет {ErrorMessages.ERROR_FIELD_PHONE}"
            phone_error = data[ErrorMessages.ERROR_FIELD_PHONE]
            if isinstance(phone_error, list):
                phone_error = phone_error[0]
            assert phone_error == ErrorMessages.FIELD_CANNOT_BE_EMPTY, \
                f"{ErrorMessages.ERROR_FIELD_PHONE} не совпадает"

        with allure.step("Проверка статуса и тела ответа"):
            print(f"\nПолучен статус: {response.status_code}")
            allure.attach(
                json.dumps(user_data, ensure_ascii=False, indent=2),
                name="request body",
                attachment_type=allure.attachment_type.JSON,
            )
            allure.attach(
                str(response.status_code),
                name="status code",
                attachment_type=allure.attachment_type.TEXT,
            )
            try:
                allure.attach(
                    json.dumps(response.json(), ensure_ascii=False, indent=2),
                    name="response body",
                    attachment_type=allure.attachment_type.JSON,
                )
            except Exception:
                allure.attach(
                    response.text,
                    name="response body",
                    attachment_type=allure.attachment_type.TEXT,
                )
            assert response.status_code == HTTPStatus.BAD_REQUEST, \
                f"Ожидался {HTTPStatus.BAD_REQUEST}, получен {response.status_code}"
            try:
                response_data = response.json()
                print(f"Ответ сервера: {response_data}")
                check_response(response_data)
            except Exception as e:
                print(f"Ошибка при парсинге ответа: {e}")
                raise

        helpers.print_test_footer()

    @allure.epic("Registration")
    @allure.feature("Auth API")
    @allure.story("Registration without request body")
    @allure.title("Ошибка при регистрации без тела запроса")
    def test_registration_no_body(self):
        """Тест: Регистрация без тела запроса"""
        helpers.print_test_header("Регистрация без тела запроса")

        with allure.step("Подготовка запроса без body"):
            helpers.print_request(None)

        print("\nОтправляем POST запрос на /api/registration/")
        with allure.step("Отправка POST запроса на /api/registration/"):
            response = auth_client.register(None)

        def check_response(data):
            def assert_non_empty_str_or_list(value, label):
                if isinstance(value, list):
                    assert value, f"{label} — пустой список"
                    value = value[0]
                assert isinstance(value, str) and value.strip(), \
                    f"Некорректное сообщение в {label}: {value!r}"

            keys_to_check = (
                ErrorMessages.ERROR_FIELD_PHONE,
                ErrorMessages.ERROR_FIELD_EMAIL,
                ErrorMessages.ERROR_FIELD_DETAIL,
            )
            present = [k for k in keys_to_check if k in data]
            assert present, (
                f"Ожидался хотя бы один из ключей {keys_to_check}. Ответ: {data}"
            )
            for key in present:
                assert_non_empty_str_or_list(data[key], key)

        with allure.step("Проверка статуса и тела ответа"):
            print(f"\nПолучен статус: {response.status_code}")
            allure.attach(
                json.dumps(None, ensure_ascii=False),
                name="request body",
                attachment_type=allure.attachment_type.JSON,
            )
            allure.attach(
                str(response.status_code),
                name="status code",
                attachment_type=allure.attachment_type.TEXT,
            )
            try:
                allure.attach(
                    json.dumps(response.json(), ensure_ascii=False, indent=2),
                    name="response body",
                    attachment_type=allure.attachment_type.JSON,
                )
            except Exception:
                allure.attach(
                    response.text,
                    name="response body",
                    attachment_type=allure.attachment_type.TEXT,
                )
            assert response.status_code == HTTPStatus.BAD_REQUEST, \
                f"Ожидался {HTTPStatus.BAD_REQUEST}, получен {response.status_code}"
            try:
                response_data = response.json()
                print(f"Ответ сервера: {response_data}")
                check_response(response_data)
            except Exception as e:
                print(f"Ошибка при парсинге ответа: {e}")
                raise

        helpers.print_test_footer()
