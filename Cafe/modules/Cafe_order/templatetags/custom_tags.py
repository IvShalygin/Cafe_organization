from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def format_localtime(value):
    if isinstance(value, timezone.datetime):
        # Пераўтвараем у мясцовы час і фарматуем у 24-гадзінны фармат
        local_time = timezone.localtime(value)
        return local_time.strftime("%b. %d, %Y, %H:%M")  # Месяц, дзень, год, гадзіны і хвіліны ў 24-гадзінным фармаце
    return value