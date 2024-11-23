from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Ingredient, Recipe


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='Введите адрес электронной почты.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name_category']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['category', 'title', 'ingredients', 'instructions', 'cooking_time', 'image', 'slug']

    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Выбор ингредиентов в виде чекбоксов
        required=True,
        label="Ингредиенты"
    )


class ImageForm(forms.Form):
    image = forms.ImageField()
