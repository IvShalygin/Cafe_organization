from django.urls import reverse

from modules.Cafe_order.models import Dish
from rest_framework.test import APITestCase


class DishAPITestCase(APITestCase):
    def test_get_dish(self):
        url = reverse('dish_api_view-list')
        print(url)
        response = self.client.get(url)
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), Dish.objects.count())
