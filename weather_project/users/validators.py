from django.core.exceptions import ValidationError
import re


class PasswordValidator(object):
    def validate(self, password, user=None):
        if not any(char.isupper() for char in password):
            raise ValidationError('Password must contain at least one uppercase letter, one lowercase letter, and one special character')

        if not any(char.islower() for char in password):
            raise ValidationError('Password must contain at least one uppercase letter, one lowercase letter, and one special character')

        if not re.search(r'[!@#$%^&*()_+]', password):
            raise ValidationError('Password must contain at least one uppercase letter, one lowercase letter, and one special character')

    def get_help_text(self):
        return _(
            "Ensure that your password is at least 8 characters long and includes uppercase letters, lowercase letters, and special characters"
        )