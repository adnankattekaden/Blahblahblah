# Generated by Django 2.2.12 on 2021-03-19 04:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0004_visiblity'),
        ('creator', '0041_delete_visiblity'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='visiblity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='owner.Visiblity'),
        ),
        migrations.AlterField(
            model_name='show',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='owner.Category'),
        ),
    ]
