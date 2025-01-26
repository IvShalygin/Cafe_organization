# Generated by Django 5.1.5 on 2025-01-26 18:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Cafe_order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dish',
            name='image',
            field=models.ImageField(blank=True, default='images/avatars/default.png', help_text='Загрузите изображение блюда (PNG, JPG, JPEG).', upload_to='images/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))], verbose_name='Картинка'),
        ),
    ]
