from django.contrib import admin
from .models import Employee, LeaveRequest, LeaveType, LeaveHistory, LeaveBalance

# Register your models here.
admin.site.register(Employee)
admin.site.register(LeaveRequest)
admin.site.register(LeaveType)
admin.site.register(LeaveHistory)
admin.site.register(LeaveBalance)