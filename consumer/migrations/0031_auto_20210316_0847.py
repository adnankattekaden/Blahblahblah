# Generated by Django 2.2.12 on 2021-03-16 08:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0033_auto_20210315_1648'),
        ('consumer', '0030_auto_20210316_0844'),
    ]

    operations = [
        migrations.AddField(
            model_name='likedlist',
            name='content',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='creator.Contents'),
        ),
        migrations.AlterField(
            model_name='likedlist',
            name='playlist_name',
            field=models.CharField(default='LikedSongs', max_length=20),
        ),
        migrations.AlterField(
            model_name='playlistcontent',
            name='playlist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='consumer.Playlist'),
        ),
    ]