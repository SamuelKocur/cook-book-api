# Generated by Django 4.0.2 on 2022-04-15 11:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_rename_shoppinglist_shoppinglistitem'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='review',
            options={'ordering': ['-date_created']},
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='shoppinglistitem',
            name='amount',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='shoppinglistitem',
            name='ingredient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.ingredient'),
        ),
        migrations.AlterField(
            model_name='shoppinglistitem',
            name='name',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
