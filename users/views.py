from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from users.models import Employees

class UserMainView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('sessions.view_session',)

class UserProfileListView(UserMainView):
    template_name = 'users/profile_list.html'
    permission_required = ('users.view_employees',)

    def get(self, request, *args, **kwargs):
        employees = Employees.objects.get_employees_json_list()
        return render(request, self.template_name, {'employees': employees})

class UserProfileViewOthers(UserMainView):
    template_name = 'users/profile_others.html'
    permission_required = ('users.view_employees',)

    def get(self, request, *args, **kwargs):
        employeeId = kwargs.get('employeeId', None)
        profile = Employees.objects.get_profile_by_id(employeeId)
        if profile:
            return render(request, self.template_name, {'profile': profile})
        return redirect('profile_list', permanent=True)

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
        elif action == 'link_profile':
            if Employees.objects.link_profile(employeeId, request.user):
                return JsonResponse({'message': 'Profile Linked'})
            return JsonResponse({'message': 'Profile Not Found'}, status=404)
        elif action == 'update_profile':
            data = request.POST.dict()
            del data['action']
            del data['csrfmiddlewaretoken']

            Employees.objects.update_profile(data)
            return JsonResponse({'message': 'Profile Updated'})
        return JsonResponse({'message': 'invalid request'}, status=400)


