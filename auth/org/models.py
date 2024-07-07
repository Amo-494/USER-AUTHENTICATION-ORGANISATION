from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError

class User(AbstractUser):
    userId = models.CharField(max_length=255, unique=True)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=15, blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', blank=True)
    organisations = models.ManyToManyField('Organisation', related_name='users', blank=True)

    def clean(self):
        errors = []
        if not self.firstName:
            errors.append({"field": "firstName", "message": "First name cannot be empty."})
        if not self.lastName:
            errors.append({"field": "lastName", "message": "Last name cannot be empty."})
        if not self.password:
            errors.append({"field": "password", "message": "Password cannot be empty."})
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate all fields before saving
        super().save(*args, **kwargs)



class Organisation(models.Model):
    orgId = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

# class UserOrganisation(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE)





    
