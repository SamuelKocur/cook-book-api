# Generated by Django 4.0.2 on 2022-03-05 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cookbook_api', '0011_alter_ingredient_note_alter_ingredient_unit_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.AlterField(
            model_name='recipe',
            name='account',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='recipes', to='cookbook_api.account'),
        ),
    ]
