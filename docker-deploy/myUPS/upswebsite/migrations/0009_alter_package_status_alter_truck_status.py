# Generated by Django 4.0.4 on 2022-04-23 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upswebsite', '0008_alter_package_status_alter_truck_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='status',
            field=models.CharField(choices=[('delivered', 'delivered'), ('loading', 'loading'), ('delivering', 'delivering'), ('pick_up', 'pick_up')], default='pick_up', max_length=32),
        ),
        migrations.AlterField(
            model_name='truck',
            name='status',
            field=models.CharField(choices=[('delivering', 'delivering'), ('idle', 'idle'), ('traveling', 'traveling'), ('arrive warehouse', 'arrive warehouse'), ('loading', 'loading')], default='idle', max_length=32),
        ),
    ]