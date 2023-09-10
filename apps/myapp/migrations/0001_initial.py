# Generated by Django 4.2.4 on 2023-09-08 19:54

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.CharField(max_length=255, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='InvestmentSector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector', models.CharField(max_length=100, unique=True, validators=[django.core.validators.MinLengthValidator(2)])),
            ],
        ),
        migrations.CreateModel(
            name='PersonalCabinet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(2)])),
                ('last_name', models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(2)])),
                ('partnership_code', models.CharField(max_length=100, unique=True, validators=[django.core.validators.MinLengthValidator(3)])),
                ('investment_sector', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(2)])),
                ('deposit_term', models.DateField()),
                ('interest_rate', models.DecimalField(decimal_places=5, max_digits=9, validators=[django.core.validators.MinValueValidator(0)])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cabinet', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
