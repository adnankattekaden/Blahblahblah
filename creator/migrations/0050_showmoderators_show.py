# Generated by Django 2.2.12 on 2021-03-27 10:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('creator', '0049_showmoderators_roles'),
    ]

    operations = [
        migrations.AddField(
            model_name='showmoderators',
            name='show',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='creator.Show'),
        ),
    ]