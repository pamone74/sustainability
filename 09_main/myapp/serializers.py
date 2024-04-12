from rest_framework import serializers
from .models import ProfileUser, Product, Ownership, User

class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileUser
        fields = ['user']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id']


class OwnershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ownership
        fields = ['product_uid', 'new_owner', 'status', 'action']
