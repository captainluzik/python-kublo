from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from apps.cabinet_api.models import CustomUser, PersonalAccount
from apps.cabinet_api.serializers.user import UserSerializer, PersonalAccountSerializer


# CustomUser = get_user_model()


class UserCreateAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="User registration endpoint",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(title="Username", type=openapi.TYPE_STRING, max_length=150),
                "email": openapi.Schema(
                    title="Email", type=openapi.TYPE_STRING, format="email", pattern=r"^[\w.@+-]+$"
                ),
                "password": openapi.Schema(title="Password", type=openapi.TYPE_STRING, format="password", min_length=8),
            },
            required=["username", "email", "password"],
        ),
        responses={201: 'Registration is successfull',
                   400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs) -> Response:
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response({'user': serializer.data, 'tokens': tokens}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        user_id = self.kwargs.get('pk')

        return get_object_or_404(CustomUser, pk=user_id)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
