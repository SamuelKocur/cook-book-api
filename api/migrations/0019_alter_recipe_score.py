# Generated by Django 4.0.2 on 2022-04-15 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_alter_review_options_alter_review_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='score',
            field=models.FloatField(blank=True, default=0),
        ),
    ]