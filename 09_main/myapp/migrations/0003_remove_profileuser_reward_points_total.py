# Generated by Django 5.0.4 on 2024-04-12 10:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0002_profileuser_recover_rewards_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profileuser",
            name="reward_points_total",
        ),
    ]
