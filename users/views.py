from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from djroles.models import Role
from djroles.exceptions import RoleError

from .models import Driver, Officer
from .serializers import DriverSerializer, UserSerializer

class ParQAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if 'role' not in request.data:
            return Response({"role":["To pole jest wymagane."]}, 
                    status=status.HTTP_406_NOT_ACCEPTABLE)
        if request.data['role'] == 'driver':
            role = Role.objects.get_for_class(Driver)
            try:
                user_role = Role.objects.get_user_role(user)
            except RoleError:
                return Response({'User without role'}, status=status.HTTP_403_FORBIDDEN)
            if role != user_role:
                return Response({'User is not driver'}, status=status.HTTP_403_FORBIDDEN)
        elif request.data['role'] == 'officer':
            role = Role.objects.get_for_class(Officer)
            try:
                user_role = Role.objects.get_user_role(user)
            except RoleError:
                return Response({'User without role'}, status=status.HTTP_403_FORBIDDEN)
            if role != user_role:
                return Response({'User is not officer'}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response({'Role is not known'}, status=status.HTTP_403_FORBIDDEN)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

@api_view(['GET'])
def current_user(request):
    try:
        driver = Driver.objects.get(pk=request.user.id)
        serializer = DriverSerializer(driver)
    except Driver.DoesNotExist:
        serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes((AllowAny,))
def register_driver(request, format=None):
    print(request.data)
    serializer = DriverSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])
def driver_detail(request, pk, format=None):
    try:
        driver = Driver.objects.get(pk=pk)
    except Driver.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DriverSerializer(driver)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        driver.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
