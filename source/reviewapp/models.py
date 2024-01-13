from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


category_choices = [('electronics', 'Electronics'), ('clothing', 'Clothing'), ('books', 'Books')]


class Products(models.Model):
    name = models.CharField(max_length=50, blank=False, verbose_name='Название')
    category = models.CharField(max_length=20, choices=category_choices, verbose_name='Категория')
    description = models.CharField(max_length=255, verbose_name='Описание')
    image = models.ImageField(upload_to='static/images/', blank=True, verbose_name='Картинка')

    def __str__(self):
        return f"{self.name}"

    def get_absolute_url(self):
        return reverse('reviewapp:article_view', args=[str(self.id)])

class Reviews(models.Model):
    author = models.ForeignKey(User, blank=False, related_name='reviews', on_delete=models.CASCADE, verbose_name='Автор')
    product = models.ForeignKey(Products, blank=False, related_name='reviews',  on_delete=models.CASCADE, verbose_name='Товар')
    description = models.CharField(max_length=255, blank=False, verbose_name='Текс отзыва')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=False, verbose_name='Оценка')
    is_moderated = models.BooleanField(default=False,)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.description}"





