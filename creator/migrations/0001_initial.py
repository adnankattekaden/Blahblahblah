# Generated by Django 2.2.12 on 2021-02-25 19:15

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
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CreatorDeatails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_me', models.CharField(max_length=255)),
                ('role', models.CharField(default='Podcaster', max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artist', models.CharField(max_length=255)),
                ('episode_name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=2000)),
                ('date_of_published', models.DateField(auto_now_add=True)),
                ('podcast', models.FileField(upload_to='podcasts/')),
                ('thumbnail', models.FileField(upload_to='thumbnail/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='creator.Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
