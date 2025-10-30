from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    # Only Admins
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'employee') and request.user.employee.role == 'admin'

class IsEmployeeUser(permissions.BasePermission):
    # Only Employees
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'employee') and request.user.employee.role == 'employee'