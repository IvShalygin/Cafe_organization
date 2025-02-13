from decimal import Decimal
from time import timezone

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

from modules.Cafe_order.models import Dish, CategoryDish
from rest_framework.test import APITestCase


class DishAPITestCase(APITestCase):
    def setUp(self):
        # Создание категорий должно быть ПЕРВЫМ
        self.category_main = CategoryDish.objects.create(name="Main")
        self.category_dessert = CategoryDish.objects.create(name="Dessert")

        # Создание пользователей
        self.admin_user = User.objects.create_user(
            username='admin',
            password='adminpass',
            is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username='user',
            password='userpass'
        )

        # Создание тестового блюда
        self.dish = Dish.objects.create(  # <--- ДОБАВЛЕНО
            name='Test Dish',
            description='Test Description',
            category=self.category_main,  # Используем объект категории
            price=10.99
        )

        # URL должен создаваться ПОСЛЕ создания блюда
        self.dish_url = reverse('dish_api_view-detail', kwargs={'pk': self.dish.pk})

        # Данные для обновления
        self.valid_update_data = {
            'name': 'Updated Dish',
            'description': 'Updated Description',
            'category': self.category_dessert.id,  # ID категории
            'price': '15.00'
        }
        self.valid_partial_data = {
            'name': 'Partial Update',
            'price': '20.00',
            'category': self.category_dessert.id
        }
        self.invalid_data = {'price': '-10.00'}

    def test_get_dish(self):
        self.client.force_authenticate(user=self.regular_user)  # Лучше использовать force_authenticate для API

        url = reverse('dish_api_view-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Dish.objects.count())

    # Исправленный тест создания блюда
    def test_create_dish(self):
        self.client.force_authenticate(user=self.admin_user)

        url = reverse('dish_api_view-list')
        data = {
            'name': 'New Dish',
            'price': '9.99',
            'description': 'New description',
            'category': self.category_main.id,  # Используем ID категории
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dish.objects.count(), 2)

    # # Тесты для update (PUT)
    def test_admin_can_fully_update_dish(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.put(self.dish_url, self.valid_update_data)
        self.dish.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dish.category, self.category_dessert)  # Проверяем объект

    def test_admin_can_partially_update_dish(self):
        self.client.force_authenticate(user=self.admin_user)  # Исправлено имя

        response = self.client.patch(self.dish_url, self.valid_partial_data)
        self.dish.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.dish.name, 'Partial Update')
        self.assertEqual(float(self.dish.price), '20.00')
        self.assertEqual(self.dish.category, self.category_dessert)

    def test_non_admin_cannot_update_dish(self):
        """Обычный пользователь не может обновить блюдо"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.put(self.dish_url, self.valid_update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_with_invalid_data(self):
        """Проверка валидации при обновлении"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(self.dish_url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # # Тесты для partial_update (PATCH)
    def test_admin_can_partially_update_dish(self):
        """Админ может частично обновить блюдо"""
        """Админ может частично обновить блюдо"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(self.dish_url, self.valid_partial_data)
        self.dish.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Сравнение имени (строки)
        self.assertEqual(self.dish.name, self.valid_partial_data['name'])

        # Сравнение цены как Decimal
        expected_price = Decimal(self.valid_partial_data['price'])
        self.assertEqual(self.dish.price, expected_price)

    def test_partial_update_with_invalid_data(self):
        """Частичное обновление с невалидными данными"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.patch(self.dish_url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # # Тесты для destroy (DELETE)
    def test_admin_can_delete_dish(self):
        """Админ может удалить блюдо"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(self.dish_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Dish.objects.filter(pk=self.dish.pk).exists())

    def test_non_admin_cannot_delete_dish(self):
        """Обычный пользователь не может удалить блюдо"""
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.delete(self.dish_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Dish.objects.filter(pk=self.dish.pk).exists())

    def test_unauthenticated_user_cannot_modify(self):
        """Неаутентифицированные запросы отклоняются"""
        """Неаутентифицированные запросы отклоняются"""
        # PUT
        response = self.client.put(self.dish_url, self.valid_update_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Было 401

        # PATCH
        response = self.client.patch(self.dish_url, self.valid_partial_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Было 401

        # DELETE
        response = self.client.delete(self.dish_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Было 401