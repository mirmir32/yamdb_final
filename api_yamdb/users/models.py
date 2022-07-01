from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, EmailField, TextField


class CustomUser(AbstractUser):
    """Переопределенная модель User с дополнительными полями."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )
    email = EmailField(unique=True, blank=False)
    bio = TextField(
        blank=True,
        verbose_name='Информация о пользователе'
    )
    role = CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль'
    )
    confirmation_code = CharField(max_length=256, default='')

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'

    def __str__(self) -> str:
        return self.username
