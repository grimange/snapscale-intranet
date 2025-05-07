from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginView(View):
    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard', permanent=True)
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, self.template_name, {'error': 'Invalid Password/Username'})
        else:
            login(request, user)
            return redirect('dashboard', permanent=True)


@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('dashboard', permanent=True)
