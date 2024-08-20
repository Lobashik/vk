from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_field
from drf_spectacular.types import OpenApiTypes


from .serializers import *
from .permissions import *
from .models import *
from vk_project.tarantool import connection


class RegisterAPIView(APIView):
    @extend_schema(
        request=RegisterSerialiser,
        responses={
            201: OpenApiResponse(
                response=RegisterOpenAPISerialiser,
                description='User registered successfully'
            ),
            400: OpenApiResponse(
                response=OpenApiTypes.STR,
                description='Invalid input'
            ),
        },
        tags=['Authentication']
    )
    def post(self, request):
        serializer = RegisterSerialiser(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            hashed_password = make_password(password)
            connection.insert('user', (
                None,
                username,
                email,
                hashed_password
            ))
            user = connection.select('user', username, index='username')
            user = User(
                id=user[0][0],
                username=user[0][1],
                email=user[0][2],
                password=user[0][3]
            )
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                'error': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
            )


class LoginAPIView(APIView):
    @extend_schema(
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(
                response=RegisterOpenAPISerialiser,
                description='User logined successfully'
            ),
            401: OpenApiResponse(
                response=OpenApiTypes.STR,
                description='Invalid password'
            ),
            404: OpenApiResponse(
                response=OpenApiTypes.STR,
                description='Invalid username'
            ),
        },
        tags=['Authentication']
    )
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = connection.select('user', username, index='username')
        if user:
            if check_password(password, user[0][3]):
                user = User(
                    id=user[0][0],
                    username=user[0][1],
                    email=user[0][2],
                    password=user[0][3]
                )
                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token)
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {'detail': ('Invalid password')},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(
            {'detail': ('Invalid username')},
            status=status.HTTP_404_NOT_FOUND
        )


class RefreshTokenAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    @extend_schema(
        request=TokenRefreshSerializer,
        responses={
            200: OpenApiResponse(
                response=RegisterOpenAPISerialiser,
                description='User logined successfully'
            ),
            401: OpenApiResponse(
                response=OpenApiTypes.STR,
                description='Refresh token is required'
            ),
            400: OpenApiResponse(
                response=OpenApiTypes.STR,
                description='Invalid refresh token'
            ),
        },
        tags=['Authentication']
    )
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {
                    'detail': 'Refresh token is required'
                },
                status=status.HTTP_401_UNAUTHORIZED
                )
        try:
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)
            return Response(
                {
                'access': new_access_token,
                },
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {
                    'detail': 'Invalid refresh token'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        

class NewBookAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    @extend_schema(
        request=BookSerializer,
        responses={
            201: OpenApiResponse(
                response=OpenApiTypes.STR,
                description='Success'
            ),
            401: OpenApiResponse(
                response=OpenApiTypes.STR,
                description='Not authorized'
            ),
            400: OpenApiResponse(
                response=OpenApiTypes.STR,
                description='Invalid data'
            ),
        },
    )
    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data['title']
            author = serializer.validated_data['author']
            year = serializer.validated_data['year']
            connection.insert('book', (
                None,
                title,
                author,
                year
            ))
            return Response(
                {
                    'status': 'success'
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    

class GetBookAPIView(APIView):
    permission_classes = (IsAuthenticated, )
    @extend_schema(
        request=GetBooksSerializer,
        responses={
            201: OpenApiResponse(
                response=BooksDataSerializer,
                description='data'
            ),
            401: OpenApiResponse(
                response=OpenApiTypes.STR,
                description='Not authorized'
            ),
            400: OpenApiResponse(
                response=OpenApiTypes.STR,
                description='Error'
            ),
        },
    )
    def post(self, request):
        keys = request.data.get('titles', [])
        if not isinstance(keys, list):
            return Response(
                {
                    'error': 'Invalid input, expected list of keys.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            results = connection.call('batch_read_by_title', [keys])
            return Response(
                {
                    'data': results[0]
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'error': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )