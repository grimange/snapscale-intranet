from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View

# Create your views here.
class DashboardViewMain(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('dashboard.view_dashboard',)
    template_name = 'dashboard/index.html'

class DashboardView(DashboardViewMain):
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
