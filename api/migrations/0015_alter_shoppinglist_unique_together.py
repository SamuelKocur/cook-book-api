# Generated by Django 4.0.2 on 2022-04-14 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_shoppinglist'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shoppinglist',
            unique_together={('account', 'ingredient')},
        ),
    ]
