# Generated by Django 3.1.7 on 2021-03-08 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0013_follows_total_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='follows',
            name='follow_type',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='follows',
            name='total_followers',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
