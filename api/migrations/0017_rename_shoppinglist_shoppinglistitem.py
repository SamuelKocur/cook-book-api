# Generated by Django 4.0.2 on 2022-04-14 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_alter_shoppinglist_unique_together_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ShoppingList',
            new_name='ShoppingListItem',
        ),
    ]
