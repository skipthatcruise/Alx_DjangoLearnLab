from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .serializers import CustomUserSerializer  # Import the serializer for CustomUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from notifications.models import Notification




class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(RetrieveUpdateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


User = get_user_model()

class FollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            target_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if target_user == request.user:
            return Response({'error': 'You cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(target_user)

        # Create notification if not self-follow
        Notification.objects.create(
            recipient=target_user,
            actor=request.user,
            verb='started following you',
            content_type=ContentType.objects.get_for_model(request.user),
            object_id=request.user.id
        )

        return Response({'message': f'You are now following {target_user.username}'}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        try:
            user_to_unfollow = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        request.user.following.remove(user_to_unfollow)
        return Response({'message': f'You have unfollowed {user_to_unfollow.username}'}, status=status.HTTP_200_OK)


class UserListView(generics.GenericAPIView):
    queryset = CustomUser.objects.all()  # Fetch all CustomUser instances from the database
    serializer_class = CustomUserSerializer  # Specify the serializer to be used

    def get(self, request, *args, **kwargs):
        # This method handles GET requests
        users = self.get_queryset()  # Get the queryset (CustomUser objects)
        serializer = self.get_serializer(users, many=True)  # Serialize the user data
        return Response(serializer.data)

