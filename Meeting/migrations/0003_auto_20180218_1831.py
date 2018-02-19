# Generated by Django 2.0.2 on 2018-02-18 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Meeting', '0002_candidate'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoterToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proxy', models.BooleanField(default=False)),
            ],
        ),
        migrations.RenameModel(
            old_name='Candidate',
            new_name='Option',
        ),
        migrations.RemoveField(
            model_name='ballotentry',
            name='data',
        ),
        migrations.RemoveField(
            model_name='ballotentry',
            name='vote',
        ),
        migrations.AddField(
            model_name='ballotentry',
            name='candidate',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='Meeting.Option'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vote',
            name='live',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='ballotentry',
            name='token',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Meeting.VoterToken'),
        ),
        migrations.RenameModel(
            old_name='Token',
            new_name='AuthToken',
        ),
        migrations.AddField(
            model_name='votertoken',
            name='auth_token',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Meeting.AuthToken'),
        ),
    ]
