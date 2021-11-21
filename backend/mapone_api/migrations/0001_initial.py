# Generated by Django 3.2.9 on 2021-11-21 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=100)),
                ('link', models.CharField(max_length=200)),
                ('body', models.CharField(max_length=100)),
                ('scale', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('publication_info', models.CharField(max_length=100)),
            ],
        ),
    ]
