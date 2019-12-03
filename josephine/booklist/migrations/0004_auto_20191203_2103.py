# Generated by Django 3.0 on 2019-12-03 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booklist', '0003_auto_20191202_1433'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shelf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'shelves',
            },
        ),
        migrations.AddField(
            model_name='book',
            name='shelves',
            field=models.ManyToManyField(to='booklist.Shelf'),
        ),
    ]
