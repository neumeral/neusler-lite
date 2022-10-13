from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import APIView, ObtainAuthToken
from rest_framework.response import Response

from .serializers import CustomAuthTokenSerializer, SignupInputSerializer, UserSerializer


class TokenAPI(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = CustomAuthTokenSerializer(data=request.data, context={"request": request})
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data["user"]

            token, created = Token.objects.get_or_create(user=user)
            profile_serializer = UserSerializer(user)
            return Response({"token": token.key, "user": profile_serializer.data})

        except serializers.ValidationError:
            return Response(
                {"detail": "Invalid Credentials"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SignupAPI(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def post(self, request, *args, **kwargs):
        try:
            input_serializer = SignupInputSerializer(data=request.data)
            input_serializer.is_valid(raise_exception=True)
            user = input_serializer.save()

            if user:
                token, created = Token.objects.get_or_create(user=user)
                profile_serializer = UserSerializer(user)
                return Response({"token": token.key, "user": profile_serializer.data})
            else:
                return Response(
                    {"detil": "Error Processing your request."},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY,
                )

        except serializers.ValidationError:
            return Response(
                {"detail": "Invalid"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
