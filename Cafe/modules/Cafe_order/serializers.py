from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from modules.Cafe_order.models import Dish, OrderItem, CategoryDish


class DishSerializer(ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=CategoryDish.objects.all()
    )

    class Meta:
        model = Dish
        fields = '__all__'
        read_only_fields = ('time_update',)

    def validate_price(self, value):
        """Правяраем, каб цана не была адмоўнай"""
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'