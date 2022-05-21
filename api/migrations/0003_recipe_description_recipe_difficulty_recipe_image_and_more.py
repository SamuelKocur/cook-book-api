# Generated by Django 4.0.2 on 2022-04-05 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_account_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='description',
            field=models.TextField(default='null'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recipe',
            name='difficulty',
            field=models.CharField(choices=[('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Hard')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.ImageField(default='null', upload_to='recipes/images'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='category',
            field=models.CharField(choices=[('main course', 'Main Course'), ('side dish', 'Side Dish'), ('desert', 'Dessert'), ('appetizer', 'Appetizer'), ('salad', 'Salad'), ('breakfast', 'Breakfast'), ('soup', 'Soup'), ('snack', 'Snack'), ('beverage', 'Beverage')], max_length=20, null=True),
        ),
    ]