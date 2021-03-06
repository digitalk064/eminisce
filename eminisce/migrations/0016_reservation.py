# Generated by Django 3.2.4 on 2021-08-08 05:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('eminisce', '0015_alter_fine_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('ACTIVE', 'Reservation is currently active.'), ('INACTIVE', 'Reservation is currently inactive.')], default='ACTIVE', max_length=20)),
                ('pickup_date', models.DateTimeField(help_text='The expected pickup date of the book.')),
                ('due_date', models.DateTimeField(help_text='The due date after which the reservation will be canceled.')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eminisce.book')),
                ('borrower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eminisce.libraryuser')),
            ],
        ),
    ]
