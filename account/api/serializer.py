from django.db.models import Q
from rest_framework.serializers import *
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from setuptools.config._validate_pyproject import ValidationError

from common.exception import *
from ..models import *

from django.conf import settings
from rest_framework.response import Response
import os,sys


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserCreateSerializer(serializers.Serializer):
    email = serializers.CharField(
        error_messages={'required': "email key is required", 'blank': "email key can't be blank"})
    password = serializers.CharField(write_only=True, required=False,
                error_messages={'blank': "password key can't be blank"})
    authorization = serializers.CharField(read_only=True)
    user_id = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs['email']
        if not email.isdigit():
            index = email.index("@")
            email_domain = email[index:]
            if email_domain != '@unilever.com':
                raise APIException400({"message": "Invalid email"})
            email = email
            if User.objects.filter(email=email).exists():
                raise APIException400({"message": "This email already exists. Please login"})
        else:
            raise APIException400({'error_message': "Invalid email address"})
        if 'password' not in attrs:
            raise APIException400({'error_message': "Password is required"})
        password = attrs['password']
        if len(password) < 8:
            raise APIException400({'message': "Password must be of atleast 8 characters"})
        return attrs
    def create(self, validated_data):
        email = validated_data['email']
        if not email.isdigit():
            user = User.objects.create(username=email, email=email)
            user.set_password(validated_data['password'])
            user.save()
        payload = jwt_payload_handler(user)
        token = 'JWT ' + jwt_encode_handler(payload)
        validated_data['authorization'] = token
        validated_data['user_id'] = user.id
        return validated_data


class LogInUserSerializer(serializers.Serializer):
    email = serializers.CharField(
        error_messages={'required': "email is required", 'blank': "email can't be blank"})
    password = serializers.CharField(required=False, write_only=True,
                                     error_messages={'blank': "Password can't be blank"})
    authorization = serializers.CharField(read_only=True)
    user_id = serializers.CharField(read_only=True)
    def validate(self, attrs):
        email = attrs['email']
        if not email.isdigit():
            index = email.index("@")
            email_domain = email[index:]
            if email_domain != '@unilever.com':
                raise APIException400({"message": "Invalid email"})
            email = email
        else:
            raise APIException400({'error_message': "Invalid email address"})
        try:
            user = User.objects.get(email=email)
        except:
            raise APIException400({"message": "Email doesn't exist"})
        if 'password' not in attrs or attrs['password'] == '':
            raise APIException400({"message": "Please provide Password"})
        if not user.check_password(attrs['password']):
            raise APIException400({"message": "Password does not matches"})
        user.save()
        payload = jwt_payload_handler(user)
        token = 'JWT ' + jwt_encode_handler(payload)
        attrs['authorization'] = token
        attrs['email'] = user.email
        attrs['user_id'] = user.id
        return attrs

