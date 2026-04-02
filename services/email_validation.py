import re


class EmailValidator:
    """Валидатор email с подробными проверками"""

    MAX_LENGTH = 254
    MIN_LENGTH = 6
    INVALID_CHARS = ["'", '"', "`", "\\", ",", ";", ":", "!", "#", "$", "%", "&", "*"]

    @classmethod
    def validate(cls, email):
        checks = [
            cls._check_not_none,
            cls._check_not_empty,
            cls._check_no_spaces,
            cls._check_one_at,
            cls._check_local_and_domain,
            cls._check_allowed_chars,
            cls._check_domain_has_dot,
            cls._check_no_underscore_in_domain,
            cls._check_length,
            cls._check_invalid_chars,
            cls._check_no_russian,
            cls._check_no_hieroglyphs,
            cls._check_no_double_dot,
            cls._check_local_dots,
            cls._check_domain_parts,
            cls._check_tld,
        ]

        for check in checks:
            is_valid, message = check(email)
            if not is_valid:
                return False, message

        return True, "Email валидный"

    @classmethod
    def _check_not_none(cls, email):
        if email is None:
            return False, "Email не может быть None"
        return True, ""

    @classmethod
    def _check_not_empty(cls, email):
        if email == "":
            return False, "Email не может быть пустым"
        return True, ""

    @classmethod
    def _check_no_spaces(cls, email):
        if " " in email:
            return False, "Email не должен содержать пробелы"
        return True, ""

    @classmethod
    def _check_one_at(cls, email):
        if "@" not in email:
            return False, "Email должен содержать @"
        if email.count("@") != 1:
            return False, "Email должен содержать ровно одну @"
        return True, ""

    @classmethod
    def _check_local_and_domain(cls, email):
        local, domain = email.split("@")

        if not local:
            return False, "Локальная часть не может быть пустой"
        if not domain:
            return False, "Домен не может быть пустым"

        return True, ""

    @classmethod
    def _check_allowed_chars(cls, email):
        """Проверка на допустимые символы: только A-Za-z0-9 @ . _ + -"""
        if not re.match(r"^[A-Za-z0-9@._+-]+$", email):
            return (
                False,
                "Email может содержать только латинские буквы, цифры и символы @ . _ + -",
            )
        return True, ""

    @classmethod
    def _check_domain_has_dot(cls, email):
        _, domain = email.split("@")
        if "." not in domain:
            return False, "Домен должен содержать точку"
        return True, ""

    @classmethod
    def _check_length(cls, email):
        if len(email) < cls.MIN_LENGTH:
            return False, "Email слишком короткий"
        if len(email) > cls.MAX_LENGTH:
            return False, "Email слишком длинный"
        return True, ""

    @classmethod
    def _check_invalid_chars(cls, email):
        for char in cls.INVALID_CHARS:
            if char in email:
                return False, f"Недопустимый символ: {char}"
        return True, ""

    @classmethod
    def _check_no_russian(cls, email):
        if re.search(r"[а-яёА-ЯЁ]", email):
            return False, "Русские буквы запрещены"
        return True, ""

    @classmethod
    def _check_no_hieroglyphs(cls, email):
        if re.search("[\u4e00-\u9fff]", email):
            return False, "Иероглифы запрещены"
        return True, ""

    @classmethod
    def _check_no_double_dot(cls, email):
        if ".." in email:
            return False, "Две точки подряд запрещены"
        return True, ""

    @classmethod
    def _check_local_dots(cls, email):
        local, _ = email.split("@")
        if local.startswith(".") or local.endswith("."):
            return False, "Точка в начале или конце запрещена"
        return True, ""

    @classmethod
    def _check_domain_parts(cls, email):
        _, domain = email.split("@")
        parts = domain.split(".")

        for part in parts:
            if not part:
                return False, "Пустая часть домена"
            if part.startswith("-") or part.endswith("-"):
                return False, "Дефис в начале/конце запрещен"

        return True, ""

    @classmethod
    def _check_tld(cls, email):
        tld = email.split(".")[-1]
        if len(tld) < 2:
            return False, "Слишком короткий домен"
        return True, ""

    @classmethod
    def _check_no_underscore_in_domain(cls, email):
        try:
            _, domain = email.split("@", 1)
        except ValueError:
            return False, "Некорректный формат email"
        if "_" in domain:
            return False, "Домен не должен содержать символ '_'"
        return True, ""
