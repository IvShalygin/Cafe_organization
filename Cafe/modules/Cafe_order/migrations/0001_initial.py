# Generated by Django 5.1.5 on 2025-01-29 21:47

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryDish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название категории')),
            ],
            options={
                'verbose_name': 'Категория блюда',
                'verbose_name_plural': 'Категории блюд',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(unique=True, verbose_name='Номер столика')),
                ('is_occupied', models.BooleanField(default=False, verbose_name='Состояние столика')),
            ],
        ),
        migrations.CreateModel(
            name='Dish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя блюда')),
                ('description', models.TextField(verbose_name='Описание блюда')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Цена')),
                ('image', models.ImageField(blank=True, default='images/default.png', help_text='Загрузите изображение блюда (PNG, JPG, JPEG).', upload_to='images/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))], verbose_name='Картинка')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата/время обновления')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Cafe_order.categorydish', verbose_name='Категория блюда')),
                ('updater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Создал/обновил')),
            ],
            options={
                'verbose_name': 'Блюдо',
                'verbose_name_plural': 'Блюда',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(0, 'В ожидании'), (1, 'Готово'), (2, 'Оплачено')], default=0, verbose_name='Статус заказа')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата/время обновления')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Общая стоимость')),
                ('updater', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Создал/обновил')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
                'ordering': ['table_number'],
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='Cafe_order.dish', verbose_name='Блюдо')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='Cafe_order.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Элемент заказа',
                'verbose_name_plural': 'Элементы заказов',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='dishes',
            field=models.ManyToManyField(related_name='orders', through='Cafe_order.OrderItem', to='Cafe_order.dish', verbose_name='Блюда'),
        ),
        migrations.AddField(
            model_name='order',
            name='table_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='Cafe_order.table', verbose_name='Номер столика'),
        ),
    ]
