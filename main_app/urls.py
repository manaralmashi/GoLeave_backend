from django.urls import path
from .views import Home, UserListView, UserDetailView

urlpatterns = [
    path('', Home.as_view(), name=''), # for test
    path('users/', UserListView.as_view(), name='list-all-users'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='display-user-details'),
]
