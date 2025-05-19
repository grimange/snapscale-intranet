from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from users.models import Employees

class UserMainView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('sessions.view_session',)

class UserProfileListView(UserMainView):
    template_name = 'users/profile_list.html'
    def get(self, request, *args, **kwargs):

        return render(request, self.template_name)

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


