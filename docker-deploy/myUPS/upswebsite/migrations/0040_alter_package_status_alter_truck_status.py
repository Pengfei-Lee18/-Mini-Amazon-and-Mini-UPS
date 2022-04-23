# Generated by Django 4.0.4 on 2022-04-23 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upswebsite', '0039_alter_package_status_alter_truck_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='status',
            field=models.CharField(choices=[('delivered', 'delivered'), ('loading', 'loading'), ('pick_up', 'pick_up'), ('delivering', 'delivering')], default='pick_up', max_length=32),
        ),
        migrations.AlterField(
            model_name='truck',
            name='status',
            field=models.CharField(choices=[('traveling', 'traveling'), ('arrive warehouse', 'arrive warehouse'), ('idle', 'idle'), ('loading', 'loading'), ('delivering', 'delivering')], default='idle', max_length=32),
        ),
    ]