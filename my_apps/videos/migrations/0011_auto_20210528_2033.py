# Generated by Django 3.1.3 on 2021-05-28 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0010_videoprogress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videoprogress',
            name='sub',
            field=models.IntegerField(verbose_name='集数'),
        ),
    ]