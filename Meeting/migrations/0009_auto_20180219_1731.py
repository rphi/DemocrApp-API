# Generated by Django 2.0.2 on 2018-02-19 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Meeting', '0008_auto_20180219_1444'),
    ]

    operations = [
        migrations.RenameField(
            model_name='authtoken',
            old_name='proxy',
            new_name='has_proxy',
        ),
        migrations.AddField(
            model_name='meeting',
            name='close_time',
            field=models.DateTimeField(null=True),
        ),
    ]