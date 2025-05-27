from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from dashboard.models import Post
from django.http import JsonResponse

# Create your views here.
class DashboardViewMain(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = ('sessions.view_session',)
    template_name = 'dashboard/index.html'

class DashboardView(DashboardViewMain):
    def get(self, request, *args, **kwargs):
        # print(request.user.get_all_permissions())
        posts = Post.objects.all()
        return render(request, self.template_name, {'posts': posts})

class DashboardViewPost(DashboardViewMain):
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        if action == 'new_post':
            content = request.POST.get('post_content', None)
            Post.objects.create(created_by=request.user, content=content)
            return JsonResponse(Post.objects.get_all_json(), safe=False)
        return JsonResponse({'message': 'invalid request'}, status=400)
