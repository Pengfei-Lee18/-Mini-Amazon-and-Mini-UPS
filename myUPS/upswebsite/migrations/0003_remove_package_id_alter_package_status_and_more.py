# Generated by Django 4.0.4 on 2022-04-15 23:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('upswebsite', '0002_truck_package'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='package',
            name='id',
        ),
        migrations.AlterField(
            model_name='package',
            name='status',
            field=models.CharField(choices=[('pick_up', 'pick_up'), ('delivering', 'delivering'), ('delivered', 'delivered'), ('loading', 'loading')], default='pick_up', max_length=32),
        ),
        migrations.AlterField(
            model_name='package',
            name='tracking_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]