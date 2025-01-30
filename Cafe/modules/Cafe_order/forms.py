import re
from django.core.exceptions import ValidationError
from django.utils import timezone
from django import forms
from django.forms import inlineformset_factory

from .models import *

class DishCreateForm(forms.ModelForm):
    """
    Форма добавления блюда на сайте
    """

    class Meta:
        model = Dish
        fields = ('name', 'category', 'price', 'description', 'image')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Рэгулярны выраз: першая літара вялікая, затым могуць быць літары, лічбы, _ або -
        if not re.match(r'^[А-ЯA-Z][а-яa-zА-ЯA-Z]*(\s[а-яa-zА-ЯA-Z,]+){0,6}$', name):
            raise ValidationError(
                "Назва блюда павінна быць некалька слоў, павінна пачынацца з вялікай літары і ўтрымліваць "
                "толькі літары (кірыліцы ці лацініцы).")

        return name



class DishUpdateForm(DishCreateForm):
    """
    Форма обновления региона на сайте
    """

    class Meta:
        model = Dish
        fields = DishCreateForm.Meta.fields + ('updater',)

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        self.fields['updater'].widget.attrs['disabled'] = 'disabled'
        self.fields['updater'].widget = forms.HiddenInput()

        # Получить текущего пользователя
        current_user = self.instance.updater

        self.fields['updater'].widget.attrs.update({
            'class': 'form-check-input',
            # 'value': current_user.username if current_user else ''
            'value': current_user
        })

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.pk:  # Если объект еще не сохранен в базе данных (т.е. это создание нового объекта)
            instance.time_update = timezone.now()  # Устанавливаем время создания на текущее время
            if instance.updater is None:  # Если автор не указан
                instance.updater = User.objects.get(username='username')  # Устанавливаем автора
        if commit:
            instance.save()
        return instance

    def clean_updater(self):
        updater = self.cleaned_data.get('updater')
        if not updater:
            raise ValidationError("Выберыце карэктнага карыстальніка для абнаўлення.")
        return updater


class OrderCreateForm(forms.ModelForm):
    """
    Форма для стварэння заказу
    """
    class Meta:
        model = Order
        fields = ["table_number", "status"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        available_tables = Table.objects.filter(is_occupied=False)

        if available_tables.exists():
            self.fields["table_number"].queryset = available_tables
        else:
            self.fields["table_number"].widget = forms.HiddenInput()  # Схаваць поле
            self.fields["table_number"].required = False  # Зрабіць поле неабавязковым
            self.no_tables_available = True  # Сцяг для шаблона

class OrderItemForm(forms.ModelForm):
    """
    Форма для дадавання страў у заказ
    """
    class Meta:
        model = OrderItem
        fields = ["dish", "quantity"]


OrderItemFormSet = inlineformset_factory(Order, OrderItem, form=OrderItemForm, extra=1, can_delete=False)
