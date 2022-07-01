import datetime as dt

from django import forms
from django.core.exceptions import ValidationError


def validate_emptiness(value):
    """
    Валидатор контролирует поле, чтобы оно было заполнено.
    """
    if value == '':
        raise forms.ValidationError(
            'Add review text.',
            params={'value': value}
        )


def validate_year(value):
    year = dt.datetime.now().year
    if year < value:
        raise ValidationError('Год выпуска произведения'
                              'не может быть больше текущего!')
    return value
