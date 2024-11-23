from django.shortcuts import render, redirect, get_object_or_404
import logging
from .models import Ingredient, Recipe, Category
from django.contrib.auth.decorators import login_required  # Для аунтефицированных пользователей
from .forms import UserRegistrationForm, CategoryForm, IngredientForm, RecipeForm, ImageForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.utils.text import slugify

logger = logging.getLogger(__name__)


def register(request):  # регистрация нового пользователя
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)  # сохранение в БД нового пользователя,
            new_user.save()
            logger.info(f'Новый пользователь {new_user.username} успешно зарегистрирован!.')
            messages.success(request, f' {new_user.username} Ваш аккаунт успешно создан!')
            return redirect('index')  # URL-имя  страницы входа
    else:
        form = UserRegistrationForm()

    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Неверный логин или пароль')
        else:
            messages.error(request, 'Неверный логин или пароль')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def custom_logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли из аккаунта")
    return redirect('/')


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info(f'Создана категория: {form.cleaned_data=}.')
            return redirect('add_recipe')
    else:
        form = CategoryForm()
        return render(request, 'add_category.html', {'form': form})


def index(request):
    return render(request, 'base.html')


def edit_ingredient(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    if request.method == 'POST':
        ingredient.name = request.POST.get('name', ingredient.name)
        ingredient.save()
        return redirect('add_ingredient')
    context = {'ingredient': ingredient}
    return render(request, 'edit_ingredient.html', context)


def add_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['name']
            form.save()
            logger.info(f'Создан ингредиент: {form.cleaned_data=}.')
            return redirect('add_recipe')
    else:
        form = IngredientForm()
        return render(request, 'add_ingredient.html', {'form': form})


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.slug = slugify(recipe.title)
            recipe.author = request.user  # Установка автора рецепта
            recipe.save()  # Сохраняем рецепт, который включает также отношения many-to-many
            form.save_m2m()  # Сохраняем много ко многим
            logger.info(f'Создан рецепт: {form.cleaned_data=}.')
            return redirect('/')  # Перенаправление после успешного добавления
    else:
        form = RecipeForm()

    return render(request, 'add_recipe.html', {'form': form})


def recipe_search(request):
    query = request.GET.get('q')
    recipes = Recipe.objects.filter(title__icontains=query) if query else []  # Поиск по названию
    return render(request, 'recipe_search.html', {'recipes': recipes, 'query': query})


def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)  # Отображение на странице подробно
    print(f"Found recipe: {recipe}")
    return render(request, 'recipe_detail.html', {'recipe': recipe})


def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']
            fs = FileSystemStorage()
            fs.save(image.name, image)
    else:
        form = ImageForm()
    return render(request, 'upload_image.html', {'form': form})


@login_required
def edit_recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    if request.user != recipe.author and not request.user.is_staff:
        return redirect('recipe_detail', recipe_id=recipe.id)  # Если нет прав, перенаправляем на страницу рецепта

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', slug=slug)
    else:
        form = RecipeForm(instance=recipe)

    return render(request, 'edit_recipe.html', {'form': form, 'recipe': recipe})


def category_list(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'category_list.html', context)


def recipes_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    # Получаем все рецепты, относящиеся к данной категории
    recipes = Recipe.objects.filter(category=category)
    return render(request, 'recipes_by_category.html', {'category': category, 'recipes': recipes})


def recipe_search_by_ingredient(request):
    query = request.GET.get('q')
    recipes = Recipe.objects.filter(ingredients__name__icontains=query) if query else Recipe.objects.none()
    context = {
        'recipes': recipes,
        'query': query,
    }
    return render(request, 'recipe_search_by_ingredient.html', context)
