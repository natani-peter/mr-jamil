# Generated by Django 5.0.3 on 2024-03-04 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseApp', '0003_alter_classrecord_enter_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='classrecord',
            name='auto_removed',
            field=models.BooleanField(default=False),
        ),
    ]
