# Generated by Django 5.0.7 on 2024-07-29 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_conges', '0004_employee_department_leave_leave_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='first_name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='employee',
            name='last_name',
            field=models.CharField(default='', max_length=50),
        ),
    ]