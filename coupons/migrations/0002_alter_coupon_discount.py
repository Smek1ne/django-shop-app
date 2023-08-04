# Generated by Django 4.2.3 on 2023-08-04 09:12

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coupons", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coupon",
            name="discount",
            field=models.IntegerField(
                help_text="Percentage value (0 to 100)",
                validators=[
                    django.core.validators.MinValueValidator,
                    django.core.validators.MaxValueValidator,
                ],
            ),
        ),
    ]
