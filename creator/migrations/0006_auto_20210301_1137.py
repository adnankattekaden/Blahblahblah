# Generated by Django 2.2.12 on 2021-03-01 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0005_auto_20210301_1019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contents',
            name='Show',
        ),
        migrations.AddField(
            model_name='contents',
            name='show',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='creator.Show'),
        ),
    ]
