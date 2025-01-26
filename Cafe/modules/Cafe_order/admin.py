from django.contrib import admin
from .models import Dish, Order, OrderItem


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'updater', 'time_update')
    search_fields = ('name',)
    list_filter = ('time_update',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'get_dishes', 'status', 'updater', 'time_update', )
    list_filter = ('status', 'time_update')
    search_fields = ('table_number',)

    def get_dishes(self, obj):
        return ", ".join([dish.name for dish in obj.dishes.all()])
    get_dishes.short_description = 'Блюда'


admin.site.register(OrderItem)
