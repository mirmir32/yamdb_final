from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_emptiness, validate_year


class Categories(models.Model):
    """Категории произведений."""
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('slug', unique=True, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанры произведений."""
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('slug', unique=True, db_index=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """
    Модель для создания произведений.
    """
    name = models.TextField('Название', max_length=256, db_index=True)
    year = models.IntegerField(
        blank=True,
        validators=[validate_year]
    )
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        db_index=True,
        related_name='titles',
        verbose_name='Жанр'
    )
    description = models.CharField(
        'Описание',
        max_length=256,
        blank=True,
    )

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Название произведения'
        verbose_name_plural = 'Названия произведений'

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    Модель для создания отзыва, который связан с конкретным произведением
    (модель Title). Автор создает только один отзыв к конкретному произведению.
    """
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='review_title'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='user',
        on_delete=models.CASCADE,
        related_name='review_author'
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        default=1,
        blank=False,
        null=False,
        validators=[MinValueValidator(
            1, message='Упс, ваша оценка слишком низкая.'),
            MaxValueValidator(
            10,
            message='Упс, ваша оценка слишком высокая.')]
    )
    text = models.TextField(
        verbose_name='Отзыв',
        help_text='Add review',
        validators=[validate_emptiness],
        blank=False
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата',
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('id',)
        db_table = 'review'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title',),
                name='unique_review'),
            models.CheckConstraint(
                name='author_not_title_again',
                check=~models.Q(author=models.F('title')),
            )
        ]

    def __str__(self) -> str:
        return self.text[:25]


class Comment(models.Model):
    """
    Модель для создания комментария к конкретному отзыву (модель Review).
    """
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='changename_title',
        blank=True,
        null=True
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comment_review',
        blank=False,
        null=False
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='comment_author'
    )
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Add review',
        validators=[validate_emptiness],
        blank=False
    )
    pub_date = models.DateTimeField(
        verbose_name='Created date',
        auto_now_add=True,
        db_index=True)

    class Meta:
        ordering = ('id',)

    def __str__(self) -> str:
        return self.text[:15]
