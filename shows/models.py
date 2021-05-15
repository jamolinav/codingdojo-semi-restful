from django.db import models
import re
from datetime import datetime, timedelta

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
    email       = models.CharField(max_length=100)
    release_date= models.DateField()
    description  = models.CharField(max_length=255)
    created_at  = models.DateTimeField(auto_now_add=True) 
    updated_at  = models.DateTimeField(auto_now=True)
    objects     = ShowsManager()


