# Generated by Django 3.1.7 on 2021-03-27 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('data', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
