from rest_framework import serializers
from .models import User, Employee, LeaveType, LeaveRequest, LeaveBalance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined']

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Employee
        fields = ['id', 'user', 'job_title', 'department', 'role', 'hire_date']

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_details = EmployeeSerializer(source='employee', read_only=True)
    leave_type_details = LeaveTypeSerializer(source='leave_type', read_only=True)
    class Meta:
        model = LeaveRequest
        fields = '__all__'
    
class LeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveBalance
        fields = '__all__'