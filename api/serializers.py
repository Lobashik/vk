from rest_framework import serializers


class RegisterSerialiser(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)
    email = serializers.EmailField(write_only=True)

    def create(self, validated_data):
        return validated_data


class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    author = serializers.CharField(max_length=50)
    year = serializers.IntegerField()

    def create(self, validated_data):
        return validated_data
    

class RegisterOpenAPISerialiser(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)


class RefreshTokenSerializer(serializers.Serializer):
    access = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=50)
    password = serializers.CharField(max_length=50)


class GetBooksSerializer(serializers.Serializer):
    titles = serializers.ListField()


class OpenAPIBookSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    author = serializers.CharField()
    year = serializers.IntegerField()


class BooksDataSerializer(serializers.Serializer):
    data = serializers.DictField(
        child=OpenAPIBookSerializer()
    )
