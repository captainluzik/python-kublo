# Generated by Django 4.2.4 on 2023-09-09 20:37

import apps.myapp.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalcabinet',
            name='deposit_term',
            field=models.DateField(validators=[apps.myapp.models.date_validator]),
        ),
        migrations.AlterField(
            model_name='personalcabinet',
            name='first_name',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(2, message='First name characters number should be greater than 2!')]),
        ),
        migrations.AlterField(
            model_name='personalcabinet',
            name='interest_rate',
            field=models.DecimalField(decimal_places=5, max_digits=9, validators=[django.core.validators.MinValueValidator(0, message='Interest rate should be greater than 0!')]),
        ),
        migrations.AlterField(
            model_name='personalcabinet',
            name='investment_sector',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2, message='Investment sector characters number should be greater than 2!')]),
        ),
        migrations.AlterField(
            model_name='personalcabinet',
            name='last_name',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(2, message='Last name characters number should be greater than 2!')]),
        ),
        migrations.AlterField(
            model_name='personalcabinet',
            name='partnership_code',
            field=models.CharField(max_length=100, unique=True, validators=[django.core.validators.MinLengthValidator(3, message='Partnership code characters number should be greater than 3!')]),
        ),
    ]
