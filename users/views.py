from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from users.models import Employees

class UserMainView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('sessions.view_session',)

class UserProfileView(UserMainView):
    template_name = 'users/profile.html'
    def get(self, request, *args, **kwargs):
        profile = Employees.objects.get_bbc__profile(request.user)
        return render(request, self.template_name, {'profile': profile})

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        employeeId = request.POST.get('employeeId', None)

        if action == 'get_profile':
            result = Employees.objects.get_profile_json(employeeId)
            if result:
                return JsonResponse(result)
            return JsonResponse({'message': 'Not Found'}, status=404)
        return JsonResponse({'error': 'invalid request'}, status=400)


