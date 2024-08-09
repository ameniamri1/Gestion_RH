# Generated by Django 3.2.25 on 2024-08-07 23:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_conges', '0002_absence'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('attendance_id', models.AutoField(primary_key=True, serialize=False)),
                ('work_hours', models.TimeField()),
                ('overtime_hours', models.TimeField()),
                ('date', models.DateField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_conges.employee')),
            ],
        ),
    ]
