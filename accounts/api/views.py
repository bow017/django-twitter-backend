from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from accounts.api.serializers import UserSerializer, LoginSerializer, SignupSerializer
from django.contrib.auth import (
    authenticate as django_authenticate,
    login as django_login,
    logout as django_logout,
)


class UserViewSet(viewsets.ModelViewSet):
    """ API endpoints for viewing and editing users """

    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class AccountViewSet(viewsets.ViewSet):
    serializer_class = SignupSerializer

    # user sign up
    @action(methods=['Post'], detail=False)
    def signup(self, request):

        serializer = SignupSerializer(data=request.data)

        # format error
        if not serializer.is_valid():
            # print("---------------------")
            # print(serializer.errors)
            return Response({
                "success": False,
                "message": "Please check input",
                "errors": serializer.errors
            }, status=400)

        user = serializer.save()
        django_login(request, user)
        return Response({
            "success": True,
            "user": UserSerializer(user).data
        }, status=201)

    # log user in
    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        # handles invalid input
        if not serializer.is_valid():
            return Response({
                "success": False,
                "message": "Please check input.",
                "errors": serializer.errors
            }, status=400)

        # if username does not exist
        username = serializer.validated_data['username'].lower()
        password = serializer.validated_data['password']

        if not User.objects.filter(username=username).exists():
            return Response({
                "success": False,
                "message": "Please check input.",
                "errors": {
                    "username": [
                        "User does not exist."
                    ]
                }
            }, status=400)

        user = django_authenticate(request, username=username, password=password)
        # wrong password
        if not user:
            return Response({
                "success": False,
                "message": "Username and password does not match."
            }, status=400)

        # log user in
        django_login(request, user)
        return Response({
            "success": True,
            "user": UserSerializer(instance=user).data,
        })

    # check user login status
    @action(methods=['GET'], detail=False)
    def login_status(self, request):
        data = {'has_logged_in': request.user.is_authenticated}
        if request.user.is_authenticated:
            data['user'] = UserSerializer(request.user).data
        return Response(data)

    # log user out
    @action(methods=['POST'], detail=False)
    def logout(self, request):
        django_logout(request)
        return Response({
            "success": True
        })
