# Generated by Django 5.2 on 2025-05-04 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flash', '0005_remove_category_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
