# Generated by Django 2.1 on 2018-09-07 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('design', '0007_merge_20180907_1757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='works',
            name='DefaultImg',
            field=models.URLField(default='static/img/Team_img/none.jpg'),
        ),
        migrations.AlterField(
            model_name='works',
            name='logo',
            field=models.URLField(default='static/img/Team_img/none.jpg'),
        ),
    ]