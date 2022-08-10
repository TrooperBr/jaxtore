# Generated by Django 3.2.6 on 2022-07-01 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('times', '0006_auto_20220628_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='time',
            name='email',
            field=models.EmailField(default='none@none.com', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='time',
            name='instagram',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='time',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='time',
            name='twitter',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='time',
            name='youtube',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]