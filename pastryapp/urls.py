from django.urls import path
from . import views
from .views import (register, add_category, edit_ingredient,custom_logout_view,
                    add_ingredient, add_recipe, login_view,
                    recipe_search, upload_image,
                    recipes_by_category, category_list,
                    recipe_search_by_ingredient
                    )

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('logout/', custom_logout_view, name='logout'),
    path('add-category/', add_category, name='add_category'),
    path('add_ingredient', add_ingredient, name='add_ingredient'),
    path('ingredient/<int:ingredient_id>/edit/', edit_ingredient, name='edit_ingredient'),
    path('add-recipe/', add_recipe, name='add_recipe'),
    path('edit_ingredient/', edit_ingredient, name='edit_ingredient'),
    path('category/<int:category_id>/', recipes_by_category, name='recipes_by_category'),
    path('categories/', category_list, name='category_list'),
    path('search_by_ingredient/', recipe_search_by_ingredient, name='recipe_search_by_ingredient'),
    path('search/', recipe_search, name='recipe_search'),
    path('<slug:slug>/', views.recipe_detail, name='recipe_detail'),
    path('upload/', upload_image, name='upload_image'),
    path('recipe/<slug:slug>/edit/', views.edit_recipe, name='recipe_edit'),




]
