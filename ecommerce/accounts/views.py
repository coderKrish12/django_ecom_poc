from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserSerializer, UserLoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate,logout
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.

class UserRegistrationView(APIView):  
    authentication_classes = []
    permission_classes = []
    def post(self, request, format=None):   
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        user = serializer.save()
        user_data = UserSerializer(user).data  
        refresh = RefreshToken.for_user(user)
        return Response({'message':'Registration Successful', 'tokens':{'refresh':str(refresh),'access':str(refresh.access_token)},'user':user_data}, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data
            return Response({'message':'Login Successful', 'tokens':{'refresh':str(refresh),'access':str(refresh.access_token)},'user':user_data}, status=status.HTTP_200_OK)
        else:
            return Response({'message':'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        user_data = UserSerializer(user).data
        return Response({'user':user_data}, status=status.HTTP_200_OK)

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]    
    def post(self, request, format=None):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            logout(request)
            return Response({"message":"Logout successfuly"},status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)    
