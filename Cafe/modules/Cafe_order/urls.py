from django.urls import path

from .views import HomeView, UserAppLogout  # from .views import UserAppLogout, HomeView

from modules.Cafe_order.Views.views_dishes import (DishesList, DishesCreate, DishesDetail, DishesUpdate, DishesDelete,
                                                   DishessBulkDelete)

urlpatterns = [

    path('dishes/', DishesList.as_view(), name='dishes'),
    path('dishes/create/', DishesCreate.as_view(), name='dishes_create'),
    path('dishes/<int:pk>/', DishesDetail.as_view(), name='dishes_detail'),
    path('dishes/<int:pk>/update/', DishesUpdate.as_view(), name='dishes_update'),
    path('dish/delete/<int:pk>/', DishesDelete.as_view(), name='delete_Dishes'),
    path('dish_delete_something/', DishessBulkDelete.as_view(), name='dish_delete_something'),
    # path('dishes/upload/', DishesUploadas_view(), name='Dishes_upload'),

    path('home/', HomeView.as_view(), name='home'),
    path('', HomeView.as_view(), name='directory_list'),
    path('page_logout/', UserAppLogout.as_view(), name='page_logout'),
]
