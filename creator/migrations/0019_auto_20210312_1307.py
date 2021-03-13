# Generated by Django 2.2.12 on 2021-03-12 13:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0018_auto_20210312_1303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follows',
            name='followed',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follow_followed', to=settings.AUTH_USER_MODEL),
        ),
    ]