from django.urls import path

from .views import HomeView, UserAppLogout  # from .views import UserAppLogout, HomeView

from modules.Cafe_order.Views.views_dishes import (DishesList, DishesCreate, DishesDetail, DishesUpdate, DishesDelete,
                                                   DishessBulkDelete)
from modules.Cafe_order.Views.views_orders import OrdersList, OrderCreateView, OrderDetailView, OrdersListAll, \
    OrderUpdateView, OrderDeleteView, DailyRevenueView, OrderSearchView

urlpatterns = [
    # dishes
    path('dishes/', DishesList.as_view(), name='dishes'),
    path('dishes/create/', DishesCreate.as_view(), name='dishes_create'),
    path('dishes/<int:pk>/', DishesDetail.as_view(), name='dishes_detail'),
    path('dishes/<int:pk>/update/', DishesUpdate.as_view(), name='dishes_update'),
    path('dish/delete/<int:pk>/', DishesDelete.as_view(), name='delete_dishes'),
    path('dish_delete_something/', DishessBulkDelete.as_view(), name='dish_delete_something'),
    # path('dishes/upload/', DishesUploadas_view(), name='Dishes_upload'),

    # orders
    path('orders/', OrdersList.as_view(), name='orders_list'),
    path('orders_all/', OrdersListAll.as_view(), name='orders_list_all'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/<int:pk>/update/', OrderUpdateView.as_view(), name='order_update'),
    path('order_delete/<int:pk>/', OrderDeleteView.as_view(), name='order_delete'),
    path('daily_revenue/', DailyRevenueView.as_view(), name='daily_revenue'),
    path('order_search/', OrderSearchView.as_view(), name='order_search'),
    # home
    path('home/', HomeView.as_view(), name='home'),
    path('', HomeView.as_view(), name='directory_list'),
    path('page_logout/', UserAppLogout.as_view(), name='page_logout'),
]
