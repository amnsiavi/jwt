from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User




class AuthSerializer(ModelSerializer):

    class Meta:
        model = User
        fields=['id','username','password','is_superuser']


        