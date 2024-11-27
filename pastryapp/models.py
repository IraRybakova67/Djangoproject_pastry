from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from unidecode import unidecode


class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Ингредиент')  # Чтобы не было повторений

    def __str__(self):
        return self.name


class Category(models.Model):
    name_category = models.CharField(max_length=30, default='Другая', unique=True, verbose_name='Категория')

    def __str__(self):
        return self.name_category


class Recipe(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    title = models.CharField(max_length=200, verbose_name='Название')  # Название рецепта
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes', verbose_name='Ингредиенты')  # Ингредиенты
    instructions = models.TextField(verbose_name='Описание приготовления')
    cooking_time = models.PositiveIntegerField(default=0, verbose_name='Время приготовления в минутах')
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания рецепта
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Автор рецепта
    image = models.ImageField(upload_to='myrecipes/images/', blank=True, null=True, verbose_name='Изображение')
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super().save(*args, **kwargs)

