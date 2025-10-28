from django.urls import path
from .views import Home, UserListView, UserDetailView, EmployeeListView, EmployeeCreateView, EmployeeDetailView, EmployeeUpdateView, EmployeeDeleteView, LeaveTypeListView, LeaveTypeUpdateView

urlpatterns = [
    path('', Home.as_view(), name=''), # for test
    path('users/', UserListView.as_view(), name='list-all-users'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='display-user-details'),
    path('employees/', EmployeeListView.as_view(), name='list-all-employees'),
    path('employees/new/', EmployeeCreateView.as_view(), name='create-employee'),
    path('employees/<int:employee_id>/', EmployeeDetailView.as_view(), name='display-employee-details'),
    path('employees/<int:employee_id>/edit/', EmployeeUpdateView.as_view(), name='update-employee'),
    path('employees/<int:employee_id>/delete/', EmployeeDeleteView.as_view(), name='delete-employee'),
    path('leave-types/', LeaveTypeListView.as_view(), name='list-all-leave-types'),
    path('leave-types/<int:leave_type_id>/edit/', LeaveTypeUpdateView.as_view(), name='list-all-leave-types'),
]
