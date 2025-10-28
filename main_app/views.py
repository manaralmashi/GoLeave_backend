from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import User, Employee, LeaveType
from .serializers import UserSerializer, EmployeeSerializer, LeaveTypeSerializer

# Create your views here.

class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the GoLeave API !'}
        return Response(content)


class UserListView(APIView):
    def get(self, request):
        # Get all of users from the DB
        queryset = User.objects.all()
        
        # convert to a JSON using a serializer
        serializer = UserSerializer(queryset, many=True)

        return Response(serializer.data)


class UserDetailView(APIView):
    def get(self, request, user_id):
        try:
            # Get single user from the DB using her id
            queryset = get_object_or_404(User, id=user_id)

            # convert to a JSON using a serializer
            serializer = UserSerializer(queryset)

            # return a Response
            return Response(serializer.data)
        
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class EmployeeListView(APIView):
    def get(self, request):
        # Get all of all employees from the DB
        queryset = Employee.objects.all()
        
        # convert to a JSON using a serializer
        serializer = EmployeeSerializer(queryset, many=True)

        return Response(serializer.data)


class EmployeeCreateView(APIView):
    def post(self, request):
        try:
            serializer = EmployeeSerializer(data=request.data)

            if serializer.is_valid(): # if all fields is valid,
                serializer.save() # save it to thr DB
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # if any field is Invalid, return this
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeDetailView(APIView):
    def get(self, request, employee_id):
        try:
            # Get single Employee from the DB using her id
            queryset = get_object_or_404(Employee, id=employee_id)

            # convert to a JSON using a serializer
            serializer = EmployeeSerializer(queryset)

            # return a Response
            return Response(serializer.data)
        
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeUpdateView(APIView):
    def put(self, request, employee_id):
        try:
            # Get the single employee from the DB
            # Look up an employee in the DB and if it does not exist return a 404 
            queryset = get_object_or_404(Employee, id=employee_id)
            # Overwrite it with the new data
            serializer = EmployeeSerializer(queryset, data=request.data)
            # save it!
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeDeleteView(APIView):
    def delete(self, request, employee_id):
        try:
            # Get an employee or return a 404
            queryset = get_object_or_404(Employee, id=employee_id)
            # delete the employee
            queryset.delete()
            # return a response
            return Response({'message': f'Employee {employee_id} has been deleted!'}, status=status.HTTP_204_NO_CONTENT)

        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LeaveTypeListView(APIView):
    def get(self, request):
        # Get all of all leave types from the DB
        queryset = LeaveType.objects.all()
        
        # convert to a JSON using a serializer
        serializer = LeaveTypeSerializer(queryset, many=True)

        return Response(serializer.data)
    

class LeaveTypeUpdateView(APIView):
    def put(self, request, leave_type_id):
        try:
            # Get the single leave type from the DB
            # Look up an leave type in the DB and if it does not exist return a 404 
            queryset = get_object_or_404(LeaveType, id=leave_type_id)
            # Overwrite it with the new data
            serializer = LeaveTypeSerializer(queryset, data=request.data)
            # save it!
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)