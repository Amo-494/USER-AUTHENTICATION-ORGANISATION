from django.urls import path
from .views import register_user, user_login, get_user, get_organisations, get_organisation, create_organisation, add_user_to_organisation

urlpatterns = [
    path('auth/register/', register_user, name='register_user'),
    path('auth/login/', user_login, name='user_login'),
    path('api/users/<str:id>/', get_user, name='get_user'),
    path('api/organisations/', get_organisations, name='get_organisations'),
    path('api/organisations/<str:orgId>/', get_organisation, name='get_organisation'),
    path('api/organisations/', create_organisation, name='create_organisation'),
    path('api/organisations/<str:orgId>/users/', add_user_to_organisation, name='add_user_to_organisation'),
]

