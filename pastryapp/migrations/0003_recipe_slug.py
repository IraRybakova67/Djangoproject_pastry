# Generated by Django 5.1.2 on 2024-11-21 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pastryapp', '0002_recipe_image_alter_category_name_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True),
        ),
    ]
