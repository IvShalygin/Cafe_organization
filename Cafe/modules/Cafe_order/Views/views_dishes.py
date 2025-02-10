from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django_filters.rest_framework import DjangoFilterBackend  # Правільны імпарт
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from modules.Cafe_order.forms import DishUpdateForm, DishCreateForm
from modules.Cafe_order.models import Dish, CategoryDish
from modules.Cafe_order.serializers import DishSerializer


class DishesList(LoginRequiredMixin, ListView):
    """
    View to list all dishes
    """
    # model = Dish
    # login_url = '/login/'
    # context_object_name = 'dishes'
    # template_name = 'dishes/dishes_view.html'
    # paginate_by = 6  # if pagination is desired
    # queryset = Dish.objects.all()

    model = Dish
    login_url = '/login/'
    context_object_name = 'dishes_by_category'
    template_name = 'dishes/dishes_view.html'
    paginate_by = None  # У гэтым выпадку лепш без пагінацыі

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Нашы блюда'

        # Катэгорыі, якія павінны ісці першымі
        priority_categories = ["Первые блюда", "Вторые блюда"]

        # Групуем стравы па катэгорыях
        dishes_by_category = defaultdict(list)
        all_categories = set()

        for dish in Dish.objects.select_related('category').all():
            dishes_by_category[dish.category].append(dish)
            all_categories.add(dish.category)

        # Фільтруем і сартыруем катэгорыі
        ordered_categories = []

        # Дадаем прыярытэтныя катэгорыі
        for cat_name in priority_categories:
            category = CategoryDish.objects.filter(name=cat_name).first()
            if category and category in dishes_by_category:
                ordered_categories.append(category)

        # Дадаем астатнія катэгорыі ў алфавітным парадку
        remaining_categories = sorted(all_categories - set(ordered_categories), key=lambda x: x.name)
        ordered_categories.extend(remaining_categories)

        # Збіраем выніковыя дадзеныя
        context['dishes_by_category'] = {category: dishes_by_category[category] for category in ordered_categories}
        return context

class DishesDetail(LoginRequiredMixin, DetailView):
    """
    View to show a single dish
    """
    model = Dish
    context_object_name = 'dish'
    template_name = 'dishes/dishes_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context

class DishesUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления отдельного блюда = View to update a single dish
    """
    model = Dish
    template_name = 'dishes/dishes_update.html'
    context_object_name = 'dish'
    success_url = '/dishes/'
    form_class = DishUpdateForm
    login_url = 'dishes_detail'
    success_message = 'The material has been successfully updated'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Update dish: {self.object.name}'
        return context

    def form_valid(self, form):
        form.instance.updater = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('dishes_detail', kwargs={'pk': self.object.pk})


class DishesCreate(LoginRequiredMixin, CreateView):
    model = Dish
    login_url = '/dishes/'
    context_object_name = 'dish'
    template_name = 'dishes/dishes_create.html'
    form_class = DishCreateForm
    success_message = 'The material has been successfully created'
    success_url = reverse_lazy('dishes_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Adding dish'
        return context

    def form_valid(self, form):
        form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)


class DishesDelete(LoginRequiredMixin, DeleteView):
    """
    Представление: удаления материала
    """
    model = Dish
    success_url = reverse_lazy('dishes')
    context_object_name = 'dish'
    template_name = 'dishes/dishes_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаленне блюда: {self.object.name}'
        return context




class DishessBulkDelete(LoginRequiredMixin, ListView):
    pass


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    renderer_classes = [JSONRenderer]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'category', 'price', 'time_update']
    pagination_class = PageNumberPagination

    def get_permissions(self):
        """Настройка доступу: стварэнне/змена/выдаленне толькі для адміністратара"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        """Стварэнне новай стравы"""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        """Поўнае абнаўленне стравы"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        """Частковае абнаўленне стравы"""
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        """Выдаленне стравы"""
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Dish deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request):
        """Масавае выдаленне"""
        ids = request.data.get('ids', [])
        deleted_count, _ = Dish.objects.filter(id__in=ids).delete()
        return Response({'status': 'success', 'message': f'{deleted_count} dishes deleted'}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get a list of dishes",
        responses={200: DishSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)