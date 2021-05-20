from django.db import models
from datetime import datetime, timedelta
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password
import re
import bcrypt

def checkNameField(field, value):
    errors  = {}
    #FIELD_REGEX = re.compile(r'^[A-Za-z]+[\ A-Za-z0-9.+_-]+')
    FIELD_REGEX = re.compile(r'^[\ A-Za-z0-9.+_-]+')
    if len(value.strip()) < 3:
            errors[field] = 'Deber tener un largo minimo de 3 caracteres'
    if not FIELD_REGEX.match(value):
        errors[field] = 'Nombre inválido, debe comenzar con una letra'
    return errors

def checkDateField(field, value):
    errors = {}
    FIELD_REGEX = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    if not FIELD_REGEX.match(value):
        errors[field] = 'Fecha inválida'

    ayer = datetime.now() - timedelta(days=1)
    ayer = ayer.strftime('%Y-%m-%d')
    present = datetime.now().strftime('%Y-%m-%d')

    format_date = "%Y-%m-%d"
    try:
        fecha = datetime.strptime(value, format_date).strftime('%Y-%m-%d')
        print('ayer: ', ayer)
        print('fecha: ', fecha)
        if fecha < ayer:
            print('fecha ingresada es menor')
        else:
            print('fecha ingresada es mayor o igual')
            errors[field] = 'La fecha debe ser en el pasado'
    except ValueError:
        errors[field] = 'Formato de fecha incorrecta. Debe ser dd/mm/aaaa'

    return errors

class ShowsManager(models.Manager):
    def validator(self, postData):
        errors = {}
        error_field = checkNameField('Title',postData['title'])
        if len(error_field) > 0:
            errors['title_format'] = error_field

        field_name = 'network'
        error_field = checkNameField(field_name,postData[field_name])
        if len(error_field) > 0:
            errors[field_name+'_format'] = error_field

        field_name = 'release_date'
        error_field = checkDateField(field_name,postData[field_name])
        if len(error_field) > 0:
            errors[field_name+'_format'] = error_field

        if len(postData['description']) > 0 and len(postData['description']) < 10:
            errors['description'] = 'Si ingresa descripcion debe ser de al menos 10 caracteres'

        if Shows.objects.filter(title=postData['title']).exclude(id=postData['id']):
            errors['title'] = 'Esta pelicula ya esta registrada'

        return errors

    def checkEmail(self, email):
        errors  = {}
        EMAIL_REGEX = re.compile(r'^[A-Za-z0-9.+_-]+@[A-Za-z0-9.+_-]+\.[A-Za-z]+$')
        if not EMAIL_REGEX.match(email):
            errors['email'] = 'Correo Inválido'
        return errors


class Shows(models.Model):
    title       = models.CharField(max_length=45)
    network     = models.CharField(max_length=45)
    email       = models.EmailField(max_length=254, validators=[validators.EmailValidator(message='Correo no vválido')])
    #tipo        = models.PositiveSmallIntegerField(
    #            validators
    #)
    release_date= models.DateField()
    description  = models.CharField(max_length=255)
    created_at  = models.DateTimeField(auto_now_add=True) 
    updated_at  = models.DateTimeField(auto_now=True)
    objects     = ShowsManager()

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

    

