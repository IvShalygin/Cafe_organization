from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from modules.Cafe_order.models import Dish


class DishesList(LoginRequiredMixin, ListView):
    model = Dish
    login_url = '/login/'
    context_object_name = 'dishes'
    template_name = 'dishes/view.html'
    paginate_by = 10  # if pagination is desired
    queryset = Dish.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Нашы блюды'
        return context


class DishesCreate(LoginRequiredMixin, ListView):
    model = Dish
    login_url = '/login/'
    context_object_name = 'dishes'
    template_name = 'dishes/create.html'
    paginate_by = 10  # if pagination is desired
    queryset = Dish.objects.all()

class DishesDetail(LoginRequiredMixin, ListView):
    model = Dish
    login_url = '/login/'
    context_object_name = 'dishes'
    template_name = 'dishes/detail.html'
    paginate_by = 10  # if pagination is desired
    queryset = Dish.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Нашы блюды'
        return context


class DishesUpdate(LoginRequiredMixin, ListView):
    model = Dish
    login_url = '/login/'
    context_object_name = 'dishes'
    template_name = 'dishes/update.html'
    paginate_by = 10  # if pagination is desired
    queryset = Dish.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Нашы блюды'
        return context


class DishesDelete(LoginRequiredMixin, ListView):
    model = Dish
    login_url = '/login/'
    context_object_name = 'dishes'
    template_name = 'dishes/delete.html'
    paginate_by = 10  # if pagination is desired
    queryset = Dish.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Нашы блюды'
        return context

class DishessBulkDelete(LoginRequiredMixin, ListView):
    pass
