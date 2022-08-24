from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializer import *
from ..models import *
from common.exception import *
from datetime import timedelta, datetime
from django.conf import settings

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': "Registration successful",
                'data': serializer.data,
                'success': True
            }, status=200, )
        error_keys = list(serializer.errors.keys())
        if error_keys:
            error_msg = serializer.errors[error_keys[0]]
            return Response({'message': error_msg[0],'success': False}, status=400)
        return Response(serializer.errors, status=400)


class LogInUser(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = LogInUserSerializer

    def post(self, request, *args, **kwargs):
        import logging
        data = request.data
        logger = logging.getLogger('accounts')
        logger.info('inside post')
        logger.info(data)
        serializer = LogInUserSerializer(data=request.data)
        if serializer.is_valid():
            logger.info('serializer is valid')
            logger.info(data)
            return Response({'message': "Login Successful", 'data': serializer.data,'success': True}, status=200, )
        else:
            error_keys = list(serializer.errors.keys())
            if error_keys:
                error_msg = serializer.errors[error_keys[0]]
                return Response({'message': error_msg[0]}, status=400)
            return Response(serializer.errors, status=400)

