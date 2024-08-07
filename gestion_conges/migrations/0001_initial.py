# Generated by Django 3.2.25 on 2024-08-02 18:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(default='', max_length=50)),
                ('last_name', models.CharField(default='', max_length=50)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Other', max_length=10)),
                ('address', models.TextField(blank=True, default='', null=True)),
                ('phone_number', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('email', models.EmailField(default='example@example.com', max_length=254, unique=True)),
                ('photo_url', models.CharField(blank=True, default='', max_length=255, null=True)),
                ('department', models.CharField(default='Unassigned', max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Leave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_leave', models.CharField(choices=[('maladie', 'Congés maladie'), ('vacances', 'Congés vacances'), ('maternité', 'Congés maternité'), ('sabbatique', 'Congés sabbatique')], default='maladie', max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('reason', models.TextField(blank=True, default='', null=True)),
                ('attachment', models.FileField(blank=True, null=True, upload_to='attachments/')),
                ('approval_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('en_attente', 'En attente'), ('approuvee', 'Approuvée'), ('rejettee', 'Rejetée')], default='en_attente', max_length=20)),
                ('comments', models.TextField(blank=True, default='', null=True)),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='approved_leaves', to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leave_requests', to='gestion_conges.employee')),
            ],
        ),
        migrations.CreateModel(
            name='ApprovalLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('level', models.IntegerField(unique=True)),
                ('approvers', models.ManyToManyField(related_name='approval_levels', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
