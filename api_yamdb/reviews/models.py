import datetime as dt

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint


class UserRole:
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICE = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        blank=False,
    )
    first_name = models.CharField(
        max_length=150,
        default=''
    )
    bio = models.TextField(
        default=''
    )
    role = models.CharField(
        max_length=9,
        choices=UserRole.ROLE_CHOICE,
        default=UserRole.USER,
    )
    confirmation_code = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['username']

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    @property
    def is_user(self):
        return self.role == UserRole.USER

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Уникальное сокращение', unique=True)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Уникальное сокращение', unique=True)

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=200)
    year = models.IntegerField(
        'Год', validators=[
            MinValueValidator(1), MaxValueValidator(dt.date.today().year)])
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория',)
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр',)
    description = models.TextField('Описание', default='')

    class Meta:
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'
        ordering = ['name']

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Тайтл',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    text = models.TextField('Текст рецензии')
    author = models.ForeignKey(
        User,
        verbose_name='Автор публикации',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        'Оценка',
        default=5,
        validators=(MinValueValidator(1), MaxValueValidator(10)),
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['title', 'author'],
                name='one_review_per_user'
            ),
        ]
        verbose_name = 'рецензия'
        verbose_name_plural = 'рецензии'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:20]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField('Текст комментария')
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата комментария',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'комментаций'
        verbose_name_plural = 'комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:20]
