import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class PasswordStrengthValidator:
    """
    Validador que exige:
      - al menos 8 caracteres
      - al menos 1 mayúscula
      - al menos 1 minúscula
      - al menos 1 número
      - al menos 1 carácter especial: - _ * $ , # + %
    """

    SPECIAL_CHARS = r'-_*$,#+%'

    def validate(self, password, user=None):
        if password is None:
            return

        if len(password) < 8:
            raise ValidationError(
                _("La contraseña debe tener al menos 8 caracteres."),
                code='password_too_short'
            )
        if not re.search(r'[A-Z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos una letra mayúscula."),
                code='password_no_upper'
            )
        if not re.search(r'[a-z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos una letra minúscula."),
                code='password_no_lower'
            )
        if not re.search(r'\d', password):
            raise ValidationError(
                _("La contraseña debe contener al menos un número."),
                code='password_no_number'
            )
        if not re.search(f"[{re.escape(self.SPECIAL_CHARS)}]", password):
            raise ValidationError(
                _("La contraseña debe contener al menos un carácter especial (-, _, *, $)."),
                code='password_no_special'
            )

    def get_help_text(self):
        return _(
            "La contraseña debe tener al menos 8 caracteres, incluir mayúsculas, minúsculas, números y al menos un carácter especial (-, _, *, $)."
        )
