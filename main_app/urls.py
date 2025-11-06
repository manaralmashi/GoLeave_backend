from django.urls import path
from .views import Home, UserListView, UserDetailView, EmployeeListCreateView, EmployeeDetailView, EmployeeUpdateView, EmployeeDeleteView, LeaveTypeListView, LeaveTypeUpdateView, LeaveRequestListCreateView, LeaveRequestDetailView, LeaveRequestUpdateView, LeaveRequestDeleteView, ApproveLeaveRequestView, RejectLeaveRequestView, PendingLeaveRequestView, LeaveBalanceListView, LeaveBalanceByEmployeeView, SignupUserView, DashboardStatsView # EmployeeListView, EmployeeCreateView, LeaveRequestListView, LeaveRequestCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', Home.as_view(), name=''), # for test
    path('users/', UserListView.as_view(), name='list-all-users'),
    path('users/<int:user_id>/', UserDetailView.as_view(), name='display-user-details'),
    # path('employees/', EmployeeListView.as_view(), name='list-all-employees'),
    # path('employees/', EmployeeCreateView.as_view(), name='create-employee'),
    path('employees/', EmployeeListCreateView.as_view(), name='employees'),
    path('employees/<int:employee_id>/', EmployeeDetailView.as_view(), name='display-employee-details'),
    path('employees/<int:employee_id>/edit/', EmployeeUpdateView.as_view(), name='update-employee'),
    path('employees/<int:employee_id>/delete/', EmployeeDeleteView.as_view(), name='delete-employee'),
    path('leave-types/', LeaveTypeListView.as_view(), name='list-all-leave-types'),
    path('leave-types/<int:leave_type_id>/edit/', LeaveTypeUpdateView.as_view(), name='list-all-leave-types'),
    # path('leave-requests/', LeaveRequestListView.as_view(), name='list-all-leave-requests'),
    # path('leave-requests/', LeaveRequestCreateView.as_view(), name='create-leave-request'),
    path('leave-requests/', LeaveRequestListCreateView.as_view(), name='leave-requests'),
    path('leave-requests/<int:leave_request_id>/', LeaveRequestDetailView.as_view(), name='display-leave-request-details'),
    path('leave-requests/<int:leave_request_id>/edit/', LeaveRequestUpdateView.as_view(), name='update-leave-request'),
    path('leave-requests/<int:leave_request_id>/delete/', LeaveRequestDeleteView.as_view(), name='delete-leave-request'),
    path('leave-requests/<int:leave_request_id>/approve/', ApproveLeaveRequestView.as_view(), name='approve-leave'),
    path('leave-requests/<int:leave_request_id>/reject/', RejectLeaveRequestView.as_view(), name='reject-leave'),
    path('leave-requests/<int:leave_request_id>/pending/', PendingLeaveRequestView.as_view(), name='pending-leave'),
    path('leave-balances/', LeaveBalanceListView.as_view(), name='list-all-leave-balances'),
    path('leave-balances/<int:employee_id>/', LeaveBalanceByEmployeeView.as_view(), name='list-employee-leave-balances'),

    path('signup/', SignupUserView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'), # token obtain pair
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # get new access token
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]
