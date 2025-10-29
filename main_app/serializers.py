from rest_framework import serializers
from .models import User, Employee, LeaveType, LeaveRequest, LeaveBalance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'


class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'
    
    def update(self, leave_type_object, validated_data):
        # if there's Put request for update leave `type`, Update `description` and `max_days_allowed` automatically!
        if 'type' in validated_data and validated_data['type'] != leave_type_object.type:
            # Update `type`
            leave_type_object.type = validated_data['type']
            # Update `description`
            leave_type_object.description = leave_type_object.get_description()
            # Update `max_days_allowed`
            leave_type_object.max_days_allowed = leave_type_object.get_max_days_allowed()

        leave_type_object.save()
        return leave_type_object


class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'


class LeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveBalance
        fields = '__all__'