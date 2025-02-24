# Generated by Django 5.1.4 on 2025-01-05 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_remove_product_quantity_aboutproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('unisex', 'Unisex')], default='male', max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='aboutproduct',
            name='size',
            field=models.CharField(choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL'), ('XXXL', 'XXXL')], max_length=10),
        ),
    ]
