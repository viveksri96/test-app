# Generated by Django 3.1.5 on 2021-01-09 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20210109_1714'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.store'),
        ),
    ]
