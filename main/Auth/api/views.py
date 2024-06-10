from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from Auth.permissions import IsAdminUser, IsRegularUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from Auth.api.serializer import AuthSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated,IsAdminUser|IsRegularUser])
@authentication_classes([JWTAuthentication])
def get_user(request):

    try:
        instance = User.objects.all()
        serializer = AuthSerializer(instance,many=True)
        return Response({
            'data':serializer.data
        })
    except:
        return Response({
            'errors':'User is not authorized'
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
@authentication_classes([JWTAuthentication])
def create_user(request):
    if len(request.data)==0:
        return Response({
            'errors':'Recieved Empty Objects'
        })
    serializer = AuthSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')
        email = serializer.validated_data.get('email')
        is_admin = serializer.validated_data.get('is_superuser')
        if is_admin:
            User.objects.create_superuser(
                username=username,password=password,
                email=email
            )
            return Response({
                'data':serializer.data,
                'msg':'Admin Created'
            })
        else:
            User.objects.create_user(
                username=username,password=password,
                email=email
            )
            return Response({
                'data':serializer.data,
                'msg':'Guest User Created'
            })
    else:
        return Response({
            'errors':'Invalid Data Format'
        })
    