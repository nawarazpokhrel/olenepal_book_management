# Generated by Django 3.2 on 2021-04-29 07:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookborrow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.author'),
        ),
        migrations.AddField(
            model_name='book',
            name='publication',
            field=models.ManyToManyField(to='books.Publication'),
        ),
        migrations.AddField(
            model_name='author',
            name='publication',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.publication'),
        ),
        migrations.AddConstraint(
            model_name='bookborrow',
            constraint=models.UniqueConstraint(fields=('book', 'user'), name='unique book for user'),
        ),
    ]
