from django.urls import path
from users.views import UserProfileView, UserProfileListView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('', UserProfileListView.as_view(), name='profile_list'),
]
