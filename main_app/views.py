from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import UserSerializer

# User = get_user_model()

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