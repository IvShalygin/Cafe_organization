from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import FileExtensionValidator

User = get_user_model()

class Dish(models.Model):
    """
    Модель для блюд.
    """
    name = models.CharField(max_length=100, verbose_name="Имя блюда")
    description = models.TextField(verbose_name="Описание блюда")
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(
        verbose_name="Картинка",
        upload_to='images/%Y/%m/%d/',
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))],
        blank=True,
        help_text="Загрузите изображение блюда (PNG, JPG, JPEG).",
        default='images/default.png'
    )
    updater = models.ForeignKey(
        to=User, verbose_name="Создал/обновил", on_delete=models.SET_NULL, null=True, blank=True
    )
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата/время обновления")

    class Meta:
        ordering = ['name']
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"

    def __str__(self):
        return self.name


class Order(models.Model):
    """
    Модель для заказов.
    """
    STATUS_CHOICES = (
        (0, 'В ожидании'),
        (1, 'Готово'),
        (2, 'Оплачено'),
    )

    table_number = models.PositiveIntegerField(verbose_name="Номер столика")
    dishes = models.ManyToManyField(
        to=Dish,
        through='OrderItem',
        related_name='orders',
        verbose_name="Список заказываемых блюд"
    )
    status = models.SmallIntegerField(
        choices=STATUS_CHOICES,
        default=0,
        verbose_name="Статус заказа"
    )
    updater = models.ForeignKey(
        to=User, verbose_name="Создал/обновил", on_delete=models.SET_NULL, null=True, blank=True
    )
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата/время обновления")

    class Meta:
        ordering = ['table_number']
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ для столика {self.table_number} - {self.get_status_display()}"


class OrderItem(models.Model):
    """
    Промежуточная модель для связи блюд и заказов.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name="Заказ")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='order_items', verbose_name="Блюдо")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказов"

    def __str__(self):
        return f"{self.dish.name} x {self.quantity} для заказа {self.order.table_number}"
