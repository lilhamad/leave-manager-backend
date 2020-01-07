from django.contrib.auth.models import User, Group
from rest_framework import serializers
from employee.models import Employee
from leave.models import Leave

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Employee
        fields = [ 'email', 'password','first_name', 'role']
        extra_kwargs = {'password':{'write_only':True,}}

    def create(self, validated_input):
        employee = Employee.objects.create(**validated_input)
        return employee

class LeaveSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Leave
        fields = ['start_date', 'employee', 'application_date', 'status']
    def create(self, validated_input):
        leave = Leave.objects.create(**validated_input)
        return leave