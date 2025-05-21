from django.urls import path
from dashboard.views import DashboardView, DashboardViewPost


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('post-request/', DashboardViewPost.as_view(), name='dashboard_post'),
]
