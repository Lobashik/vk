from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from vk_project.tarantool import connection
from drf_spectacular.extensions import OpenApiAuthenticationExtension


class TarantoolJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'vk_project.tarantoolAuthentication.TarantoolJWTAuthentication'
    name = 'TarantoolJWTAuthentication'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
    

class TarantoolUser:
    def __init__(self, id, username, email, is_authenticated):
        self.id = id
        self.username = username
        self.email = email
        self.is_authenticated = is_authenticated


class TarantoolJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            user = connection.select('user', user_id, index='id')
            if not user:
                raise AuthenticationFailed('User not found.')
            return TarantoolUser(
                user[0][0],
                user[0][1],
                user[0][2],
                True
                )
        except KeyError:
            raise AuthenticationFailed(
                'Token contained no recognizable user identification.'
                )

OpenApiAuthenticationExtension.register(TarantoolJWTAuthenticationScheme)
