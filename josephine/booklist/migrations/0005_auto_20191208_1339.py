# Generated by Django 3.0 on 2019-12-08 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booklist', '0004_auto_20191203_2103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='shelves',
            field=models.ManyToManyField(blank=True, to='booklist.Shelf'),
        ),
    ]
