from django.contrib import admin
from .models import Dish, Order, OrderItem, CategoryDish, Table


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'updater', 'time_update')
    search_fields = ('name',)
    list_filter = ('time_update', 'category')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'get_dishes', 'status', 'total_price', 'updater', 'time_update', )
    list_filter = ('status', 'time_update')
    search_fields = ('table_number',)

    def get_dishes(self, obj):
        return ", ".join([dish.name for dish in obj.dishes.all()])
    get_dishes.short_description = 'Блюда'


admin.site.register(OrderItem)

@admin.register(CategoryDish)
class CategoryDish(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'is_occupied', )
    search_fields = ('number',)
    list_filter = ('is_occupied',)