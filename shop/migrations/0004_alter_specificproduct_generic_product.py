# Generated by Django 4.0.4 on 2022-09-10 16:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_productimage_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specificproduct',
            name='generic_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specific_products', to='shop.genericproduct'),
        ),
    ]
