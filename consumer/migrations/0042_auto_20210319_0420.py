# Generated by Django 2.2.12 on 2021-03-19 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consumer', '0041_auto_20210319_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlistcontent',
            name='playlist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='consumer.Playlist'),
        ),
    ]
