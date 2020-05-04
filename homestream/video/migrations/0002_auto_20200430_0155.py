# Generated by Django 2.2.9 on 2020-04-30 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='videofile',
            name='date_taken',
            field=models.DateField(null=True, verbose_name='date taken'),
        ),
        migrations.AddField(
            model_name='videofile',
            name='mime_type',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
    ]