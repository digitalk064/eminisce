# Generated by Django 3.2.4 on 2021-06-16 07:18

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('eminisce', '0005_loan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='due_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 7, 7, 18, 33, 425057, tzinfo=utc), help_text='The due date of the loan.'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='return_date',
            field=models.DateTimeField(help_text='The actual date the book was returned and the loan finishes.', null=True),
        ),
        migrations.AlterField(
            model_name='loan',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 6, 16, 7, 18, 33, 425057, tzinfo=utc), help_text='The start date of the loan.'),
        ),
    ]
