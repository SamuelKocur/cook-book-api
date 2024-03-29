# Generated by Django 4.0.2 on 2022-04-06 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_recipe_diary_free_recipe_gluten_free_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(editable=False)),
                ('likes', models.IntegerField(blank=True, default=0, editable=False)),
                ('dislikes', models.IntegerField(blank=True, default=0, editable=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='api.account')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='api.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='UserFavoriteRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_recipes', to='api.account')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite_recipes', to='api.recipe')),
            ],
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
