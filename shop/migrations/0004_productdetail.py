# Generated by Django 4.0.4 on 2022-08-20 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_color_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stock', models.SmallIntegerField()),
                ('price', models.DecimalField(decimal_places=3, max_digits=9)),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.color')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.size')),
                ('specific_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.specificproduct')),
            ],
            options={
                'unique_together': {('specific_product', 'color', 'size')},
            },
        ),
    ]
