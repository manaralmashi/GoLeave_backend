from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, AllowAny, AllowAnyOrReadOnly
from .permissions import IsAdminUser, IsEmployeeUser

from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import User, Employee, LeaveType, LeaveRequest, LeaveHistory, LeaveBalance
from .serializers import UserSerializer, EmployeeSerializer, LeaveTypeSerializer, LeaveRequestSerializer, LeaveBalanceSerializer

# Create your views here.

class Home(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        content = {'message': 'Welcome to the GoLeave API !'}
        return Response(content)


class UserListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Get all of users from the DB
        queryset = User.objects.all()
        
        # convert to a JSON using a serializer
        serializer = UserSerializer(queryset, many=True)

        return Response(serializer.data)


class UserDetailView(APIView):
    permission_classes = [AllowAny]

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
        

class EmployeeListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # Get all of all employees from the DB
        queryset = Employee.objects.all()
        
        # convert to a JSON using a serializer
        serializer = EmployeeSerializer(queryset, many=True)

        return Response(serializer.data)
    

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


# class EmployeeListView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         # Get all of all employees from the DB
#         queryset = Employee.objects.all()
        
#         # convert to a JSON using a serializer
#         serializer = EmployeeSerializer(queryset, many=True)

#         return Response(serializer.data)


# class EmployeeCreateView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         try:
#             serializer = EmployeeSerializer(data=request.data)

#             if serializer.is_valid(): # if all fields is valid,
#                 serializer.save() # save it to thr DB
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             # if any field is Invalid, return this
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         except Exception as error:
#             return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeDetailView(APIView):
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

    def get(self, request):
        # Get all of all leave types from the DB
        queryset = LeaveType.objects.all()
        
        # convert to a JSON using a serializer
        serializer = LeaveTypeSerializer(queryset, many=True)

        return Response(serializer.data)


class LeaveTypeUpdateView(APIView):
    permission_classes = [IsAdminUser]

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


class LeaveRequestListCreateView(APIView):
    permission_classes = [AllowAny]

    # List Leave Requests
    def get(self, request):
        # Get all of all leave requests from the DB
        queryset = LeaveRequest.objects.all()
        
        # convert to a JSON using a serializer
        serializer = LeaveRequestSerializer(queryset, many=True)

        return Response(serializer.data)
    
    # Create Leave Requests
    def post(self, request):
        try:
            serializer = LeaveRequestSerializer(data=request.data)

            if serializer.is_valid(): # if all fields is valid,
                serializer.save() # save it to thr DB
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            # if any field is Invalid, return this
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class LeaveRequestListView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         # Get all of all leave requests from the DB
#         queryset = LeaveRequest.objects.all()
        
#         # convert to a JSON using a serializer
#         serializer = LeaveRequestSerializer(queryset, many=True)

#         return Response(serializer.data)


# class LeaveRequestCreateView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         try:
#             serializer = LeaveRequestSerializer(data=request.data)

#             if serializer.is_valid(): # if all fields is valid,
#                 serializer.save() # save it to thr DB
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             # if any field is Invalid, return this
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         except Exception as error:
#             return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LeaveRequestDetailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, leave_request_id):
        try:
            # Get single Leave Request from the DB using her id
            queryset = get_object_or_404(LeaveRequest, id=leave_request_id)

            # convert to a JSON using a serializer
            serializer = LeaveRequestSerializer(queryset)

            # return a Response
            return Response(serializer.data)
        
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LeaveRequestUpdateView(APIView):
    permission_classes = [AllowAny]

    def put(self, request, leave_request_id):
        try:
            # Get the single leave request from the DB
            # Look up an leave request in the DB and if it does not exist return a 404 
            queryset = get_object_or_404(LeaveRequest, id=leave_request_id)
            # Overwrite it with the new data
            serializer = LeaveRequestSerializer(queryset, data=request.data)
            # save it!
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LeaveRequestDeleteView(APIView):
    permission_classes = [AllowAny]

    def delete(self, request, leave_request_id):
        try:
            # Get an leave request or return a 404
            queryset = get_object_or_404(LeaveRequest, id=leave_request_id)
            # delete the leave request
            queryset.delete()
            # return a response
            return Response({'message': f'Leave Request: {leave_request_id} has been deleted!'}, status=status.HTTP_204_NO_CONTENT)
        
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ApproveLeaveRequestView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, leave_request_id):
        try:
            # TODO:
            # 1. Get the LeaveRequest object with ID
            leave_request = get_object_or_404(LeaveRequest, id=leave_request_id)
            
            # 2. Update status to 'approved'
            leave_request.status = 'approved'
            
            # 3. Save it to the DB
            leave_request.save()
            
            # 4. Add new row on Leave History table
            LeaveHistory.objects.create(
                leave_request= leave_request,
                action_type= 'approved',
                action_by_user= request.user,
                note= request.data.get('note', '')
            )
        
            # 5. Return a response
            return Response({
                'message': 'Leave request approved successfully',
                'leave_request_id': leave_request.id,
                'new_status': 'approved',
            }, status=status.HTTP_200_OK)
            
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RejectLeaveRequestView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, leave_request_id):
        try:
            # TODO:
            # 1. Get the LeaveRequest object with ID
            leave_request = get_object_or_404(LeaveRequest, id=leave_request_id)
            
            # 2. Update status to 'rejected'
            leave_request.status = 'rejected'
            
            # 3. Save it to the DB
            leave_request.save()
            
            # 4. Add new row on Leave History table
            LeaveHistory.objects.create(
                leave_request= leave_request,
                action_type= 'rejected',
                action_by_user= request.user,
                note= request.data.get('note', '')
            )
        
            # 5. Return a response
            return Response({
                'message': 'Leave request rejected successfully',
                'leave_request_id': leave_request.id,
                'new_status': 'rejected',
            }, status=status.HTTP_200_OK)
            
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PendingLeaveRequestView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, leave_request_id):
        try:
            # TODO:
            # 1. Get the LeaveRequest object with ID
            leave_request = get_object_or_404(LeaveRequest, id=leave_request_id)
            
            # 2. Update status to 'pending'
            leave_request.status = 'pending'
            
            # 3. Save it to the DB
            leave_request.save()
            
            # 4. Add new row on Leave History table
            LeaveHistory.objects.create(
                leave_request= leave_request,
                action_type= 'pending',
                action_by_user= request.user,
                note= request.data.get('note', '')
            )
        
            # 5. Return a response
            return Response({
                'message': 'Leave request pending successfully',
                'leave_request_id': leave_request.id,
                'new_status': 'pending',
            }, status=status.HTTP_200_OK)
            
        except Exception as error:
            return Response({'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class LeaveBalanceListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        # TODO:
        # 1. Get all of all leave balances from the DB
        queryset = LeaveBalance.objects.all()
        
        # 2. convert to a JSON using a serializer
        serializer = LeaveBalanceSerializer(queryset, many=True)

        # 3. return a response
        return Response(serializer.data)


# class LeaveBalanceByEmployeeView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, employee_id):
#         # TODO:
#         # 1. Get all of all leave balances from the DB that related to employee_id
#         queryset = LeaveBalance.objects.filter(employee= employee_id)

#         # 2. convert to a JSON using a serializer
#         serializer = LeaveBalanceSerializer(queryset, many=True)

#         # 3. return a response
#         return Response(serializer.data, status=status.HTTP_200_OK)
class LeaveBalanceByEmployeeView(APIView):
    permission_classes= [AllowAny]

    def get(self, request, employee_id):  # 🔥 أضف employee_id هنا
        try:
            # استخدم employee_id من الـ URL بدل request.user
            employee = Employee.objects.get(id=employee_id)
            leave_balances = LeaveBalance.objects.filter(
                employee=employee, 
                is_active=True
            ).select_related('leave_type')
            
            # organize balance_data by leave_types
            balance_data = {}
            for balance in leave_balances:
                balance_data[balance.leave_type.type] = {
                    'remaining_days': balance.remaining_days,
                    'used_days': balance.used_days,
                    'total_days': balance.total_days,
                    'max_days_allowed': balance.leave_type.max_days_allowed,
                    'warning_status': balance.get_warning_status()[0],
                    'warning_message': balance.get_warning_status()[1]
                }
            
            return Response(balance_data)
            
        except Employee.DoesNotExist:
            return Response(
                {'error': 'Employee profile not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

class SignupUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # User model data
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        # Employee model data
        job_title = request.data.get("job_title")
        department = request.data.get("department")
        role = request.data.get("role")
        hire_date = request.data.get("hire_date")

        required_fields = [username, password, email, first_name, last_name, job_title, department, role, hire_date]
        if not all(required_fields):
            return Response(
                {"error": "Please provide all required fields!"},
                status=status.HTTP_400_BAD_REQUEST)

        # if User Already Exists
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': "User Already Exists"},
                status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. Create new `User`
            user = User.objects.create_user(
                username=username, 
                email=email, 
                password=password, 
                first_name=first_name, 
                last_name=last_name
            )
            
            # 2. Create new `Employee` that related to `User`
            employee = Employee.objects.create(
                user=user,
                job_title=job_title,
                department=department,
                role=role,
                hire_date=hire_date
            )
            
            return Response({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "employee_id": employee.id,
                "job_title": employee.job_title,
                "department": employee.department,
                "role": employee.role
            }, status=status.HTTP_201_CREATED)
            
        except Exception as err:
            # if Employee faild delete the User, local(): Variables inside the current function/block, Source: `https://www.geeksforgeeks.org/python/python-locals-function/`
            if 'user' in locals():
                user.delete()

            return Response(
                {"error": str(err)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class DashboardStatsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        user = request.user
        employee = Employee.objects.filter(user=user).first()
        
        if employee.role == 'admin':
            total_employees = Employee.objects.count()
            pending_requests = LeaveRequest.objects.filter(status='pending').count()
            approved_this_month = LeaveRequest.objects.filter(
                status='approved',
                created_at__month=timezone.now().month
            ).count()
            
            recent_requests = LeaveRequest.objects.select_related('employee__user').order_by('-created_at')[:5]
            
            stats = {
                'total_employees': total_employees,
                'pending_requests': pending_requests,
                'approved_this_month': approved_this_month,
                'recent_requests': LeaveRequestSerializer(recent_requests, many=True).data
            }
            
        else:
            my_requests = LeaveRequest.objects.filter(employee=employee)
            total_requests = my_requests.count()
            approved_requests = my_requests.filter(status='approved').count()
            pending_requests = my_requests.filter(status='pending').count()
            
            leave_balance = LeaveBalance.objects.filter(employee=employee).first()
            
            stats = {
                'total_requests': total_requests,
                'approved_requests': approved_requests,
                'pending_requests': pending_requests,
                'leave_balance': LeaveBalanceSerializer(leave_balance).data if leave_balance else None
            }
        
        return Response(stats)