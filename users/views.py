from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from users.models import Employees

class UserMainView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('sessions.view_session',)

class UserProfileView(UserMainView):
    template_name = 'users/profile.html'
    def get(self, request, *args, **kwargs):
        profiles = Employees.objects.get_bbc__profile(request.user)
        multiple_profiles = False
        if len(profiles) > 1:
            multiple_profiles = True
        return render(request, self.template_name, {'profiles': profiles, 'multiple_profiles': multiple_profiles})

    def post(self, request, *args, **kwargs):
        pass

