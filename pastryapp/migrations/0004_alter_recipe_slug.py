# Generated by Django 5.1.2 on 2024-11-21 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pastryapp', '0003_recipe_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]