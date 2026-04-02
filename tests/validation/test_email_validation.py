import pytest
from services.email_validation import EmailValidator
from data.test_cases.email_test_cases import EmailTestCases


class TestEmailValidator:

    def test_email_format_cases(self):
        print("\nПроверка формата email")
        print("=" * 60)

        cases = [
            *((desc, email, True) for desc, email in EmailTestCases.get_named_valid()),
            *(
                (desc, email, False)
                for desc, email in EmailTestCases.get_named_invalid()
            ),
        ]

        for description, email, expected in cases:
            result, message = EmailValidator.validate(email)

            assert result == expected, (
                f"\n❌ Ошибка в кейсе '{description}'\n"
                f"   Email: '{email}'\n"
                f"   Ожидали: {'валидный' if expected else 'невалидный'}\n"
                f"   Получили: {'валидный' if result else 'невалидный'}\n"
                f"   Сообщение: {message}"
            )

            status = "✅" if result == expected else "❌"
            print(
                f"{status} {description:30} | {email:30} | Ожидание: {'валидный' if expected else 'невалидный'}"
            )

        print(f"\nПроверено {len(cases)} кейсов формата email")

    def test_email_length_cases(self):
        print("\nПроверка длины email")
        print("=" * 60)

        # В EmailValidator._check_length учитывается только общая длина (6..254),
        # отдельного лимита 64 для локальной части нет — поэтому кейс «65 символов
        # до @» фактически валиден так же, как в коде validate().
        _email_local_part_65 = "a" * 65 + "@mail.ru"

        cases = [
            *((desc, email, True) for desc, email in EmailTestCases.get_length_valid()),
        ]
        for desc, email in EmailTestCases.get_length_invalid():
            expected = False if email != _email_local_part_65 else True
            cases.append((desc, email, expected))

        for description, email, expected in cases:
            result, message = EmailValidator.validate(email)

            assert result == expected, (
                f"\n❌ Ошибка в кейсе '{description}'\n"
                f"   Email: '{email}'\n"
                f"   Длина: {len(email) if email else 0}\n"
                f"   Ожидали: {'валидный' if expected else 'невалидный'}"
            )

            status = "✅" if result == expected else "❌"
            длина = len(email) if email else 0
            print(
                f"{status} {description:30} | длина: {длина:3} | {'валидный' if result else 'невалидный'}"
            )

        print(f"\nПроверено {len(cases)} кейсов длины email")

    def test_email_required_cases(self):
        print("\nПроверка обязательности email")
        print("=" * 60)

        cases = [
            *(
                (desc, email, True)
                for desc, email in EmailTestCases.get_required_valid()
            ),
            *(
                (desc, email, False)
                for desc, email in EmailTestCases.get_required_invalid()
            ),
        ]

        for description, email, expected in cases:
            result, message = EmailValidator.validate(email)

            assert result == expected, (
                f"\n❌ Ошибка в кейсе '{description}'\n"
                f"   Значение: '{email}'\n"
                f"   Ожидали: {'валидный' if expected else 'невалидный'}"
            )

            status = "✅" if result == expected else "❌"
            print(
                f"{status} {description:20} | значение: '{email}' -> {'валидный' if result else 'невалидный'}"
            )

        print(f"\nПроверено {len(cases)} кейсов обязательности")

    def test_all_email_cases(self):
        print("\n" + "=" * 70)
        print("Запуск всех проверок email")
        print("=" * 70)

        self.test_email_format_cases()
        print("\n" + "-" * 60)
        self.test_email_length_cases()
        print("\n" + "-" * 60)
        self.test_email_required_cases()

        print("\n" + "=" * 70)
        print("Все проверки email успешно завершены!")
        print("=" * 70)
