# Generated by Django 3.2 on 2021-04-30 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_bookreturn_overdue_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreturn',
            name='fine_amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
