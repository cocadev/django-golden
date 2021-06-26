from .models import Dealer, User, Client
from management.models import Employee
from django.db.utils import ProgrammingError
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings
from rest_framework import serializers



class CustomJWTSerializer(JSONWebTokenSerializer):
    def auth(self, username, password):
        yield CustomUserAuth().authenticate(None, username=username, password=password)
        yield CustomEmployeeAuth().authenticate(None, username=username, password=password)
        yield CustomClientAuth().authenticate(None, username=username, password=password)
        yield MobileDealerAuth().authenticate(None, username=username, password=password)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        if username and password:
            user = next(obj for obj in self.auth(username, password) if obj is not None)
            if user:
                if not user.is_active:
                    msg = 'User account is disabled.'
                    raise serializers.ValidationError(msg)

                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload)
                }
            else:
                msg = 'Unable to login with provided credentials.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Must include "username" and "password"'
            raise serializers.ValidationError(msg)


class CustomDealerAuth(object):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Dealer.objects.get(email=username)
            if user.check_password(password) & (user.tenant.domain_url == str(request.tenant)):
                return user
        except Dealer.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = Dealer.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except Dealer.DoesNotExist:
            return None


class MobileDealerAuth(object):
    def authenticate(self, request, username=None, password=None):
        try:
            user = Dealer.objects.get(email=username)
            if user.check_password(password):
                return user
        except Dealer.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = Dealer.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except Dealer.DoesNotExist:
            return None


class CustomUserAuth(object):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):

        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except User.DoesNotExist:
            return None


class CustomEmployeeAuth:
    def authenticate(self, request, username=None, password=None):
        try:
            user = Employee.objects.get(email=username)
            if user.check_password(password):
                return user
        except Employee.DoesNotExist:
            return None
        except ProgrammingError:
            return None

    def get_user(self, user_id):
        try:
            user = Employee.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except Employee.DoesNotExist:
            return None


class CustomClientAuth:
    def authenticate(self, request, username=None, password=None):
        try:
            client = Client.objects.get(email=username)
            if client.check_password(password):
                return client
        except Client.DoesNotExist:
            return None
        except ProgrammingError:
            return None

    def get_user(self, user_id):
        try:
            client = Client.objects.get(pk=user_id)
            if client.is_active:
                return client
            return None
        except Client.DoesNotExist:
            return None
