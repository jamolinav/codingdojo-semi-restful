from django.db import models
from datetime import datetime, timedelta
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
import re
import bcrypt


class UserManager(models.Manager):
    def validator(self, postData):
        errors  = {}
        
        errorsEmail = self.checkEmail(postData['email'])
        if len(errorsEmail) > 0:
            errors['email'] = errorsEmail

        return errors
    
    def checkEmail(self, email):
        errors  = {}
        EMAIL_REGEX = re.compile(r'^[A-Za-z0-9.+_-]+@[A-Za-z0-9.+_-]+\.[A-Za-z]+$')
        if not EMAIL_REGEX.match(email):
            errors['email'] = 'Correo Inválido'
        return errors

class User(models.Model):
    first_name      = models.CharField(max_length=45)
    last_name       = models.CharField(max_length=45)
    email           = models.CharField(max_length=100)
    password        = models.CharField(max_length=254)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)
    objects         = UserManager()

    def __str__(self):
        return '%s the email' % self.email

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)
    
    @staticmethod
    def ifExists(email):
        users    = User.objects.filter(email = email)
        if len(users) > 0:
            return True
        else:
            return False

    @staticmethod
    def authenticate(email, password):
        users    = User.objects.filter(email = email)
        if len(users) > 0:
            user = users[0]
            bd_password = user.password
            if check_password(password, bd_password):
                return user
        return None

class MessageManager(models.Manager):
    def validator(self, postData):
        errors = {}
        len_comment = len(postData['message'])
        if len_comment < 15:
            errors['message'] = 'Debe ingresar un mensaje de al menos 15 caracteres'

        return errors

class Message(models.Model):
    message     = models.TextField(max_length=3000)
    created_at  = models.DateTimeField(auto_now_add=True) 
    updated_at  = models.DateTimeField(auto_now=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_user')
    objects     = MessageManager()

class CommentManager(models.Manager):
    def validator(self, postData):
        errors = {}
        len_comment = len(postData['comment'])
        if len_comment < 15:
            errors['comment'] = 'Debe ingresar un comentario de al menos 15 caracteres'

        return errors

class Comment(models.Model):
    comment     = models.TextField(max_length=3000)
    created_at  = models.DateTimeField(auto_now_add=True) 
    updated_at  = models.DateTimeField(auto_now=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    message     = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='comment_message')
    objects     = CommentManager()