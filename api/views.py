from django.shortcuts import render
from rest_framework import viewsets
from .serializers import UserSerializer, LeaveSerializer
from employee.models import Employee
from leave.models import Leave
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED
)
from rest_framework import status
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.fields import CurrentUserDefault
from django.contrib.auth import get_user_model

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    
    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class LeaveViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employees to be viewed or edited.
    """
    queryset = Leave.objects.all().order_by('-application_date')
    serializer_class = LeaveSerializer

#login employee
@csrf_exempt
@api_view(["POST"])
def login(request):
    print('here to login')
    username = request.data.get("email")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both email and password'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = get_user_model().objects.get(Q(email__iexact=username))
    except get_user_model().DoesNotExist:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    data = {}
    data["first_name"]=user.first_name
    data["last_name"]=user.last_name
    data["email"]=user.email
    # data["username"]=user.username
    return Response({'data':{'token': token.key,'user':data}}, status=HTTP_200_OK)

#list of all leaves (admin only)
class AllLeaves(APIView):
    permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,) 
    def get(self, request):
        leaves = Leave.objects.all()
        return Response(leaves)


#list of leaves a user has applied for
def my_leaves(request, user_id):
    serializer_context = {
            'request': request,
    }
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,) 
    leaves = Leave.objects.filter(employee_id=user_id)
    serializer = LeaveSerializer(leaves, many=True, read_only=True, context=serializer_context)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
@permission_classes((IsAdminUser,))
def leave_detail(request, id):
    # permission_classes = (IsAuthenticated, )
    authentication_classes = (TokenAuthentication,) 
    print(request)
    serializer_context = {'request': request,}
    """
    Retrieve, update or delete a leave.
    """
    try:
        leave = Leave.objects.get(id=id)
    except Leave.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = LeaveSerializer(leave, context=serializer_context)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request, strict = False)
        serializer = LeaveSerializer(leave, data=data, context=serializer_context)
        if serializer.is_valid():
            print(serializer)
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        leave.delete()
        return HttpResponse(status=204)

# @csrf_exempt
# # @permission_classes((AllowAny,))

#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,) 


@api_view(['GET', 'PUT', 'DELETE'])
def user_detail(request, id):
    """
    Retrieve, update or delete a code snippet.
    """
    print('IIIIIIIIIIIIIIIIIi')
    try:
        employee = get_user_model().objects.get(pk=id)
    except get_user_model().DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(employee)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)