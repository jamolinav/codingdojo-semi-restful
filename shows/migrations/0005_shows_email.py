# Generated by Django 2.2.4 on 2021-05-12 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shows', '0004_auto_20210509_0246'),
    ]

    operations = [
        migrations.AddField(
            model_name='shows',
            name='email',
            field=models.CharField(default='.', max_length=100),
            preserve_default=False,
        ),
    ]
