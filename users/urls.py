from django.urls import path
from users.views import UserProfileView, UserProfileListView, UserProfileViewOthers

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/<str:employeeId>/', UserProfileViewOthers.as_view(), name='profile_others'),
    path('', UserProfileListView.as_view(), name='profile_list'),
]
