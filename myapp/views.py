from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer


class UserCreationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="This method creates a new user.",
        responses={200: UserSerializer}
    )
    def post(self, request, *args, **kwargs) -> Response:
        data = {}
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "Successfully registered a new user."

            refresh_token = RefreshToken.for_user(user)
            data['refresh'] = str(refresh_token)
            data['access'] = str(refresh_token.access_token)

            return Response(data)

        return Response(serializer.errors)
