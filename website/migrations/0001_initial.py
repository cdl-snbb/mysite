# Generated by Django 2.0 on 2020-03-12 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userme', models.CharField(max_length=20)),
                ('text', models.TextField()),
                ('comment_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-comment_time'],
            },
        ),
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
    ]
