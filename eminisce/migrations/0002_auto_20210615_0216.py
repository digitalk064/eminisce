# Generated by Django 3.2.4 on 2021-06-14 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eminisce', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='author',
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.CharField(default='', help_text='Separated by commas.', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book',
            name='barcode',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
