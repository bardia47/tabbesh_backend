# Generated by Django 2.2.6 on 2020-02-26 09:31

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
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('fname', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('address', models.CharField(max_length=30)),
                ('mobile_phone', models.CharField(max_length=30)),
                ('home_phone', models.CharField(blank=True, max_length=30)),
                ('profile_image', models.ImageField(upload_to='')),
                ('email', models.EmailField(max_length=254)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
