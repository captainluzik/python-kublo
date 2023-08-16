from rest_framework import generics
from rest_framework.response import Response

from .serializers import UserSerializer
from .models import CustomUser


class UserCreationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs) -> Response:
        data = {}
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            data['response'] = "Successfully registered a new user."

            return Response(data)

        return Response(serializer.errors)
