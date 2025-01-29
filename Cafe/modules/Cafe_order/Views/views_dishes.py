from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from modules.Cafe_order.forms import DishUpdateForm, DishCreateForm
from modules.Cafe_order.models import Dish


class DishesList(LoginRequiredMixin, ListView):
    """
    View to list all dishes
    """
    model = Dish
    login_url = '/login/'
    context_object_name = 'dishes'
    template_name = 'dishes/dishes_view.html'
    paginate_by = 6  # if pagination is desired
    queryset = Dish.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Нашы блюды'
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
