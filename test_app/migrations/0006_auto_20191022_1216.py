# Generated by Django 2.2.5 on 2019-10-22 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0005_room_db'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room_db',
            name='d_to',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='room_db',
            name='e_to',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='room_db',
            name='n_to',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='room_db',
            name='s_to',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='room_db',
            name='u_to',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='room_db',
            name='w_to',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
