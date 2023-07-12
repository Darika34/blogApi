from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    # required = True eto pole obpazatelno dlya zapolnenie
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True,required=True)
    # write_only = True pri sozdanyy obyekta eti dannie skrivautsya
    password_confirmation = serializers.CharField(min_length=8, write_only=True, required=True)


    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirmation')


    def validate(self, attrs):
        password_confirmation  = attrs.pop('password_confirmation')
        if password_confirmation != attrs['password']:
            raise serializers.ValidationError(
                'passwords are not the same'
            )
        if not attrs['first_name'].istitle():
            raise serializers.ValidationError(
                'name should strart from capitalize'
            )
        return attrs


    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self,data):
        request = self.context.get('request')
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = authenticate(username=username,
                                password=password,
                                request=request)
            if not user:
                raise serializers.ValidationError(
                    'this password or username not exist'
                )
        else:
            raise serializers.ValidationError(
                'username and password required'
            )
        data['user'] = user
        return data

    def validate_username(self, username):
        print(username)
        if not User.objects.filter(username = username).exists():
            raise serializers.ValidationError(
                'user with this  username not found'
            )
        return username

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)