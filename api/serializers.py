from django.contrib.auth.models import User, Group
from rest_framework import serializers
from employee.models import Employee
from leave.models import Leave
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [ 'email', 'password','first_name','last_name', 'role', 'token']
        extra_kwargs = {'password':{'write_only':True,}}

    def create(self, validated_input):
        employee = get_user_model().objects.create(**validated_input)
        try:
            user = get_user_model().objects.get(Q(email__iexact=employee.email))
        except get_user_model().DoesNotExist:
            return Response({'error': 'Invalid Credentials'},
                            status=status.HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return {'token': token.key,'first_name':user.first_name, 'last_name':user.last_name, 'email':user.email}

class LeaveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Leave
        fields = ['start_date', 'employee', 'application_date', 'status']
    def create(self, validated_input):
        leave = Leave.objects.create(**validated_input)
        return leave