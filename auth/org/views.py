from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import User, Organisation
from .serializers import UserSerializer, OrganisationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated, AllowAny
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    logger.info("Register endpoint hit")
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        org_name = f"{user.firstName}'s Organisation"
        org = Organisation.objects.create(name=org_name)
        user.organisations.add(org)
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "status": "success",
            "message": "Registration successful",
            "data": {
                "accessToken": str(refresh.access_token),
                "user": UserSerializer(user).data
            }
        }, status=status.HTTP_201_CREATED)
    logger.error(f"Validation errors: {serializer.errors}")
    return Response({
        "status": "Bad request",
        "message": "Registration unsuccessful",
        "statusCode": 400
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        logger.error(f"Failed login attempt for user {email}")
        return Response({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
        }, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(username=user.username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            "status": "success",
            "message": "Login successful",
            "data": {
                "accessToken": str(refresh.access_token),
                "user": UserSerializer(user).data
            }
        }, status=status.HTTP_200_OK)
    else:
        logger.error(f"Failed login attempt for user {email}")
        return Response({
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, id):
    try:
        user = User.objects.get(userId=id)
    except User.DoesNotExist:
        return Response({
            "status": "Bad request",
            "message": "User not found",
            "statusCode": 404
        }, status=status.HTTP_404_NOT_FOUND)

    if user == request.user or request.user.organisations.filter(id__in=user.organisations.values_list('id', flat=True)).exists():
        return Response({
            "status": "success",
            "message": "User retrieved successfully",
            "data": UserSerializer(user).data
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "status": "Forbidden",
            "message": "Access denied",
            "statusCode": 403
        }, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_organisations(request):
    organisations = request.user.organisations.all()
    serializer = OrganisationSerializer(organisations, many=True)
    return Response({
        "status": "success",
        "message": "Organisations retrieved successfully",
        "data": {
            "organisations": serializer.data
        }
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_organisation(request, orgId):
    try:
        organisation = Organisation.objects.get(orgId=orgId)
    except Organisation.DoesNotExist:
        return Response({
            "status": "Bad request",
            "message": "Organisation not found",
            "statusCode": 404
        }, status=status.HTTP_404_NOT_FOUND)

    if organisation in request.user.organisations.all():
        return Response({
            "status": "success",
            "message": "Organisation retrieved successfully",
            "data": OrganisationSerializer(organisation).data
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "status": "Forbidden",
            "message": "Access denied",
            "statusCode": 403
        }, status=status.HTTP_403_FORBIDDEN)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_organisation(request):
    serializer = OrganisationSerializer(data=request.data)
    if serializer.is_valid():
        organisation = serializer.save()
        request.user.organisations.add(organisation)
        return Response({
            "status": "success",
            "message": "Organisation created successfully",
            "data": OrganisationSerializer(organisation).data
        }, status=status.HTTP_201_CREATED)
    return Response({
        "status": "Bad Request",
        "message": "Client error",
        "statusCode": 400
    }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_user_to_organisation(request, orgId):
    try:
        organisation = Organisation.objects.get(orgId=orgId)
    except Organisation.DoesNotExist:
        return Response({
            "status": "Bad request",
            "message": "Organisation not found",
            "statusCode": 404
        }, status=status.HTTP_404_NOT_FOUND)

    userId = request.data.get('userId')
    try:
        user = User.objects.get(userId=userId)
    except User.DoesNotExist:
        return Response({
            "status": "Bad request",
            "message": "User not found",
            "statusCode": 404
        }, status=status.HTTP_404_NOT_FOUND)

    if organisation in request.user.organisations.all():
        organisation.users.add(user)
        return Response({
            "status": "success",
            "message": "User added to organisation successfully",
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "status": "Forbidden",
            "message": "Access denied",
            "statusCode": 403
        }, status=status.HTTP_403_FORBIDDEN)


