# Generated by Django 5.1.1 on 2024-12-06 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Technicians", "0002_alter_technicianprofile_deviceid"),
    ]

    operations = [
        migrations.AddField(
            model_name="technicianprofile",
            name="addressline",
            field=models.CharField(blank=True, default="", max_length=100, null=True),
        ),
    ]
