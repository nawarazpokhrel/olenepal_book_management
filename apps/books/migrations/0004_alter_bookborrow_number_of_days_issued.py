# Generated by Django 3.2 on 2021-04-30 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_bookborrow_number_of_days_issued'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookborrow',
            name='number_of_days_issued',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
