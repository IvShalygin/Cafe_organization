from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from modules.Cafe_order.forms import DishUpdateForm, DishCreateForm
from modules.Cafe_order.models import Dish, OrderItem, Order


class OrdersList(LoginRequiredMixin, ListView):
    """
    View to list all orders
    """
    model = Order
    login_url = '/login/'
    context_object_name = 'orders'
    template_name = 'orders/orders_view.html'
    paginate_by = 6
    queryset = Order.objects.prefetch_related('order_items__dish').exclude(status=2)
    custom_title = 'Заказы'
    custom_title_single = 'Заказ'
    create_url_name = 'order_create'
    detail_url_name = 'order_detail'
    delete_multiple_url_name = 'delete_multiple_orders'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model_name'] = self.custom_title if self.custom_title else self.model.__name__
        context['custom_title'] = self.custom_title
        context['custom_title_single'] = self.custom_title_single
        context['create_url_name'] = self.create_url_name
        context['detail_url_name'] = self.detail_url_name
        context['delete_multiple_url_name'] = self.delete_multiple_url_name
        return context


