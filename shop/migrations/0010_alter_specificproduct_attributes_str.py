# Generated by Django 4.0.4 on 2022-08-22 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_attributeclass_alter_specificproduct_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specificproduct',
            name='attributes_str',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]