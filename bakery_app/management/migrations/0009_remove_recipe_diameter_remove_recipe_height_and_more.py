# Generated by Django 4.2.9 on 2024-02-21 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("management", "0008_remove_supplier_created_ingredient_created_by_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="recipe",
            name="diameter",
        ),
        migrations.RemoveField(
            model_name="recipe",
            name="height",
        ),
        migrations.RemoveField(
            model_name="recipe",
            name="length",
        ),
        migrations.RemoveField(
            model_name="recipe",
            name="width",
        ),
        migrations.CreateModel(
            name="ProductVariation",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("diameter", models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ("length", models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ("width", models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ("main_variation", models.BooleanField(default=False)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="variations", to="management.product"
                    ),
                ),
            ],
        ),
    ]
