from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Categories(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')

    def __str__(self):
        return f"{self.name}"


class Products(models.Model):
    name = models.CharField(max_length=50, blank=False, verbose_name='Название')
    category = models.ForeignKey(Categories, blank=False, on_delete=models.PROTECT, verbose_name='Категория')
    description = models.CharField(max_length=255, verbose_name='Описание')
    image = models.ImageField(upload_to='static/images/', verbose_name='Картинка')

    def __str__(self):
        return f"{self.name}"


class Reviews(models.Model):
    author = models.ForeignKey(User, blank=False, on_delete=models.CASCADE, verbose_name='Автор')
    product = models.ForeignKey(Products, blank=False, on_delete=models.CASCADE, verbose_name='Товар')
    description = models.CharField(max_length=255, blank=False, verbose_name='Текс отзыва')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=False, verbose_name='Оценка')
    is_moderated = models.BooleanField(default=False,)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')

    def __str__(self):
        return f"{self.description}"

