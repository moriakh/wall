from __future__ import unicode_literals
from django.db import models #, IntegrityError

class UsersManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 4:
            errors["first_name"] = "The user's first name should be at least 4 characters lenght"
        if len(postData['last_name']) < 4:
            errors["last_name"] = "The user's last name should be at least 4 characters lenght"    
        if len(postData['email']) < 4:
            errors["email"] = "The user's email should be at least 4 characters lenght"
        if len(postData['password']) < 6:
            errors["password"] = "The user's password should be at least 6 characters lenght"
        if postData['password'] != postData['password_confirm']:
            errors["password"] = "Both passwords should be the same"
        return errors

class Users(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField(unique = True)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    followers = models.ManyToManyField('Users', related_name = 'followeds')
    objects = UsersManager()

    def __str__(self) -> str:
        return f'{self.id} : {self.first_name} {self.last_name}'

class Posts(models.Model):
    post = models.TextField(null=True, blank=True)
    user = models.ForeignKey(Users, related_name = "posts", on_delete = models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return f'{self.id} : {self.post}'

class Comments(models.Model):
    comment = models.TextField(blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(Users, related_name = 'comments', on_delete = models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Posts, related_name = 'comments', on_delete = models.CASCADE, null=True, blank=True)
        
    def __str__(self) -> str:
        return f'{self.id} : {self.comment}'

# python manage.py createsuperuser