# Generated by Django 3.2.4 on 2021-06-17 13:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('eminisce', '0006_auto_20210616_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libraryuser',
            name='fingerprint',
            field=models.BinaryField(blank=True, editable=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 8, 13, 5, 51, 104947, tzinfo=utc), help_text='The due date of the loan.'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 17, 13, 5, 51, 104947, tzinfo=utc), help_text='The start date of the loan.'),
        ),
    ]
