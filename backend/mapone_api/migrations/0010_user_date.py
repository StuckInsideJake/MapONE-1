# Generated by Django 3.2.9 on 2022-03-05 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mapone_api', '0009_auto_20220226_0112'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='date',
            field=models.DateField(default='2000-01-01'),
            preserve_default=False,
        ),
    ]
