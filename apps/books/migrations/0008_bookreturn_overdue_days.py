# Generated by Django 3.2 on 2021-04-30 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_bookreturn_fine_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookreturn',
            name='overdue_days',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
