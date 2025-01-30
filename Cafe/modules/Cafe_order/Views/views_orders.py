from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from modules.Cafe_order.forms import DishUpdateForm, DishCreateForm, OrderCreateForm, OrderItemFormSet
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

class OrdersListAll(LoginRequiredMixin, ListView):
    """
    View to list all orders
    """
    model = Order
    login_url = '/login/'
    context_object_name = 'orders'
    template_name = 'orders/orders_view.html'
    paginate_by = 6
    queryset = Order.objects.prefetch_related('order_items__dish')
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

class OrderCreateView(LoginRequiredMixin, CreateView):
    """
    View для стварэння заказу
    """
    model = Order
    form_class = OrderCreateForm
    template_name = "orders/order_create.html"
    success_url = reverse_lazy("orders_list")  # Переход на список заказа


    def get_context_data(self, **kwargs):
        """
        Дадаем у кантэкст інфармацыю пра вольныя столікі і FormSet
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["order_items"] = OrderItemFormSet(self.request.POST)
        else:
            context["order_items"] = OrderItemFormSet()
        return context

    def form_valid(self, form):
        """
        Захаванне заказу і звязаных элементаў
        """
        context = self.get_context_data()
        order_items = context["order_items"]

        with transaction.atomic():
            # Сохраняем заказ
            form.instance.updater = self.request.user
            self.object = form.save()

            # Привязываем FormSet к заказу
            order_items.instance = self.object

            if order_items.is_valid():
                order_items.save()  # Сохраняем FormSet
                self.object.calculate_total_price()  # Обновляем общую стоимость
            else:
                # Если FormSet не валиден, возвращаем ошибку
                print(order_items.errors)  # Для отладки
                return self.form_invalid(form)

        return super().form_valid(form)

class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    View для дэталёвага прагляду заказу
    """
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_object(self):
        """
        Атрымаць канкрэтны заказ
        """
        return get_object_or_404(Order, id=self.kwargs["pk"])

