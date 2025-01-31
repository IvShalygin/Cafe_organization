from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.utils import timezone
from django.db.models import Q

from modules.Cafe_order.forms import DishUpdateForm, DishCreateForm, OrderCreateForm, OrderItemFormSet, OrderUpdateForm, \
    OrderSearchForm
from modules.Cafe_order.models import Dish, OrderItem, Order


class OrdersList(LoginRequiredMixin, ListView):
    """
    View to list all orders excluding orders with status 2 = "Оплачено"
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


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    """
       View для рэдагавання заказу
       """
    model = Order
    form_class = OrderUpdateForm
    template_name = "orders/order_update.html"
    success_url = reverse_lazy("orders_list")

    def get_context_data(self, **kwargs):
        """
        Дадаем FormSet у кантэкст
        """
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["order_items"] = OrderItemFormSet(self.request.POST, instance=self.object)
        else:
            context["order_items"] = OrderItemFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        """
        Захаванне заказу і звязаных элементаў
        """
        context = self.get_context_data()
        order_items = context["order_items"]

        with transaction.atomic():
            form.instance.updater = self.request.user
            self.object = form.save()

            if order_items.is_valid():
                order_items.instance = self.object
                order_items.save()
                self.object.calculate_total_price()  # Абнаўляем кошт заказу
            else:
                print(order_items.errors)  # Для адладкі
                return self.form_invalid(form)

        return super().form_valid(form)


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    """
    View для выдалення заказу
    """
    model = Order
    success_url = reverse_lazy("orders_list")
    template_name = "orders/order_delete.html"

    def get_context_data(self, **kwargs):
        """
        Добавляем дополнительный контекст в шаблон.
        """
        context = super().get_context_data(**kwargs)
        context["order"] = self.get_object()  # Передаем заказ в шаблон
        return context

    def get(self, request, *args, **kwargs):
        print("Метод GET вызван")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Переопределяем метод post, чтобы вызвать delete.
        """
        print("Метод POST вызван")
        return self.delete(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Переопределяем метод delete для освобождения столика, если заказ активный.
        """
        try:
            print("Метод DELETE вызван")
            self.object = self.get_object()  # Получаем объект заказа

            print(
                f"Заказ #{self.object.id}: статус = {self.object.status}, столик = {self.object.table_number.number}, занят = {self.object.table_number.is_occupied}")

            if self.object.status != 2 or self.object.status != 'Оплачено':  # 2 — это статус "Оплачено"
                print(f"Заказ #{self.object.id} активный. Освобождаем столик #{self.object.table_number.number}.")
                # Освобождаем столик
                table = self.object.table_number
                table.is_occupied = False
                table.save()
                print(f"Столик #{table.number} освобожден.")
            else:
                print(f"Заказ #{self.object.id} оплачен. Столик не освобождается при удалении заказа.")

            # Удаляем заказ
            response = super().delete(request, *args, **kwargs)
            print(f"Заказ #{self.object.id} удален.")

            return response
        except Exception as e:
            print(f"Ошибка при удалении заказа: {e}")
            raise  # Повторно выбрасываем исключение


class DailyRevenueView(View):
    template_name = 'orders/daily_revenue.html'

    def get(self, request, *args, **kwargs):
        now = timezone.now()
        start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)

        orders = Order.objects.filter(time_update__gte=start_of_day, status=2)
        total_revenue = sum(order.total_price for order in orders)

        context = {
            'orders': orders,
            'total_revenue': total_revenue,
            'start_of_day': start_of_day,
            'now': now,
        }
        return render(request, self.template_name, context)


class OrderSearchView(View):
    template_name = 'orders/order_search.html'

    def get(self, request, *args, **kwargs):
        form = OrderSearchForm(request.GET)
        orders = Order.objects.all()

        query = request.GET.get('query')  # Получаем поисковый запрос из формы в хедере

        if query:
            # Фильтрация по номеру стола или статусу
            orders = orders.filter(
                Q(table_number__number__icontains=query) |  # Поиск по номеру стола
                Q(status__icontains=query)  # Поиск по статусу
            )

        if form.is_valid():
            table_number = form.cleaned_data.get('table_number')
            status = form.cleaned_data.get('status')

            # Фильтрация по номеру стола
            if table_number:
                orders = orders.filter(table_number__number=table_number)

            # Фильтрация по статусу
            if status:
                orders = orders.filter(status=status)

        context = {
            'form': form,
            'orders': orders,
            'query': query,  # Передаем поисковый запрос в шаблон
        }
        return render(request, self.template_name, context)