# Generated by Django 2.0 on 2020-03-10 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_auto_20200310_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]