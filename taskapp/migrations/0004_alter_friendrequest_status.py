# Generated by Django 4.0.1 on 2022-02-01 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0003_profile_friendrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='status',
            field=models.CharField(choices=[('send', 'send'), ('accepted', 'accepted')], default='send', max_length=10),
        ),
    ]