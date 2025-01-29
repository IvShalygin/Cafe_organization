from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import FileExtensionValidator

User = get_user_model()

class CategoryDish(models.Model):
    """
    Модель для категорий блюд.
    """
    name = models.CharField(max_length=100, verbose_name="Название категории")

    class Meta:
        verbose_name = "Категория блюда"
        verbose_name_plural = "Категории блюд"

    def __str__(self):
        return self.name

class Dish(models.Model):
    """
    Модель для блюд.
    """
    name = models.CharField(max_length=100, verbose_name="Имя блюда")
    description = models.TextField(verbose_name="Описание блюда")
    category = models.ForeignKey(
        to=CategoryDish, verbose_name="Категория блюда", on_delete=models.SET_NULL, null=True
    )
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

class Table(models.Model):
    number = models.PositiveIntegerField(unique=True, verbose_name="Номер столика")
    is_occupied = models.BooleanField(default=False, verbose_name="Занят")

    def __str__(self):
        return f"Столик {self.number} ({'Занят' if self.is_occupied else 'Свободен'})"

class Order(models.Model):
    """
    Модель для заказов.
    """
    STATUS_CHOICES = (
        (0, 'В ожидании'),
        (1, 'Готово'),
        (2, 'Оплачено'),
    )

    table_number = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='orders', verbose_name="Номер столика")
    status = models.SmallIntegerField(
        choices=STATUS_CHOICES,
        default=0,
        verbose_name="Статус заказа"
    )
    dishes = models.ManyToManyField(Dish, through='OrderItem', related_name='orders', verbose_name="Блюда")
    updater = models.ForeignKey(
        to=User, verbose_name="Создал/обновил", on_delete=models.SET_NULL, null=True, blank=True
    )
    time_update = models.DateTimeField(auto_now=True, verbose_name="Дата/время обновления")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Общая стоимость")

    class Meta:
        ordering = ['table_number']
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ {self.id} для столика {self.table_number} - {self.get_status_display()}"

    def calculate_total_price(self):
        # Вычисляем общую стоимость заказа на основе блюд
        total = sum(item.dish.price * item.quantity for item in self.order_items.all())
        self.total_price = total
        self.save(update_fields=['total_price'])  # Абнаўляем ТОЛЬКІ total_price

    def save(self, *args, **kwargs):
        # Автоматически обновляем статус столика при создании заказа, оплате заказа
        is_new = self.pk is None  # Калі заказ ствараецца ўпершыню
        previous_status = None
        if self.pk:
            previous_status = Order.objects.get(pk=self.pk).status

        super().save(*args, **kwargs)

        # Освобождение столика при изменении статуса на "Оплачено"
        if self.status == 2 and previous_status != 2:
            self.table_number.is_occupied = False
            self.table_number.save()

        if is_new:
            self.table_number.is_occupied = True
            self.table_number.save()


class OrderItem(models.Model):
    """
    Промежуточная модель для связи блюд и заказов.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name="Заказ")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name='order_items', verbose_name="Блюдо")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    @property
    def total_price(self):
        """ Вяртае агульны кошт пэўнага элемента заказу (колькасць × цана). """
        return self.dish.price * self.quantity

    def save(self, *args, **kwargs):
        """ Пасля захавання OrderItem абнаўляем total_price у Order. """
        super().save(*args, **kwargs)
        self.order.calculate_total_price()

    def delete(self, *args, **kwargs):
        """ Пасля выдалення OrderItem абнаўляем total_price у Order. """
        super().delete(*args, **kwargs)
        self.order.calculate_total_price()


    class Meta:
        verbose_name = "Элемент заказа"
        verbose_name_plural = "Элементы заказов"

    def __str__(self):
        return f"{self.dish.name} x {self.quantity} для заказа {self.order.id}"
