# Generated by Django 3.2.4 on 2021-08-07 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eminisce', '0013_auto_20210807_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fine',
            name='reason',
            field=models.CharField(blank=True, help_text='Reason for the fine.', max_length=200, null=True, verbose_name='Reason'),
        ),
    ]