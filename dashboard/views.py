from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View

# Create your views here.
class DashboardViewMain(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('sessions.view_session',)
    template_name = 'dashboard/index.html'

class DashboardView(DashboardViewMain):
    def get(self, request, *args, **kwargs):
        # print(request.user.get_all_permissions())
        return render(request, self.template_name)
