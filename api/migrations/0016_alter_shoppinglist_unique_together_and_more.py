# Generated by Django 4.0.2 on 2022-04-14 16:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_alter_shoppinglist_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='shoppinglist',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='shoppinglist',
            name='amount',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='shoppinglist',
            name='name',
            field=models.CharField(max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='shoppinglist',
            name='ingredient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.ingredient'),
        ),
    ]
