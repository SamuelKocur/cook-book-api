# Generated by Django 4.0.2 on 2022-04-06 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_review_userfavoriterecipe_delete_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userfavoriterecipe',
            old_name='date_created',
            new_name='date_added',
        ),
    ]
