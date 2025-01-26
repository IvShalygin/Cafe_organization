from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.views import View


class UserAppLogout(LogoutView):
    """
    Выход з дадатку
    """
    next_page = 'home'

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'list.html')