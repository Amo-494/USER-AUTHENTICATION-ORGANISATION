from rest_framework import serializers
from .models import User, Organisation
import logging

logger = logging.getLogger(__name__)



class OrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organisation
        fields = ['orgId', 'name', 'description']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'firstName', 'lastName', 'email', 'phone', 'password', 'userId']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        logger.info("Creating user with data: %s", validated_data)
        try:
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                email=validated_data['email'],
                firstName=validated_data['firstName'],
                lastName=validated_data['lastName'],
                userId=validated_data['userId'],
                phone=validated_data.get('phone')
            )
            logger.info("User created successfully: %s", user)
            return user
        except Exception as e:
            logger.error("Error creating user: %s", e)
            raise
    

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        org_name = f"{user.firstName}'s Organisation"
        org = Organisation.objects.create(orgId=user.userId, name=org_name)
        user.organisations.add(org)
        return user
