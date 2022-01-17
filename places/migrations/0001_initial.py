# Generated by Django 2.2 on 2021-11-28 20:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import places.utils.helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100, unique=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('date_joined', models.DateField(auto_now=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Associated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verified_email', models.BooleanField(default=False)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='people/')),
            ],
        ),
        migrations.CreateModel(
            name='Customization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='CustomizationOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=100)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=1000)),
            ],
        ),
        migrations.CreateModel(
            name='FoodImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='food/')),
            ],
        ),
        migrations.CreateModel(
            name='FoodItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('subtitle', models.CharField(blank=True, max_length=150, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('category', models.CharField(blank=True, max_length=20, null=True)),
                ('tags', models.CharField(blank=True, max_length=200, null=True)),
                ('customizations', models.ManyToManyField(blank=True, to='places.Customization')),
                ('images', models.ManyToManyField(blank=True, to='places.FoodImage')),
                ('packed_with', models.ManyToManyField(blank=True, to='places.Associated')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.CharField(max_length=20)),
                ('message', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderCustomization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.Customization')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.CustomizationOption')),
            ],
        ),
        migrations.CreateModel(
            name='StaffPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_name', models.CharField(max_length=150)),
                ('verbose_name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_id', models.CharField(default=places.utils.helpers.generate_staff_id, max_length=20)),
                ('permissions', models.ManyToManyField(blank=True, to='places.StaffPermissions')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customizations', models.ManyToManyField(blank=True, to='places.OrderCustomization')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.FoodItem')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cleared', models.BooleanField(default=False)),
                ('status', models.CharField(blank=True, choices=[('pending', 'Pending'), ('on-route', 'On Route'), ('delivered', 'Delivered')], max_length=20, null=True)),
                ('delivery', models.BooleanField(default=False)),
                ('invoice_id', models.CharField(default=places.utils.helpers.generate_invoice_id, max_length=12)),
                ('paid', models.BooleanField(default=False)),
                ('items', models.ManyToManyField(blank=True, to='places.OrderItem')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.Customer')),
            ],
        ),
        migrations.AddField(
            model_name='customization',
            name='options',
            field=models.ManyToManyField(blank=True, to='places.CustomizationOption'),
        ),
        migrations.AddField(
            model_name='customer',
            name='cart',
            field=models.ManyToManyField(blank=True, to='places.OrderItem'),
        ),
        migrations.AddField(
            model_name='customer',
            name='orders',
            field=models.ManyToManyField(blank=True, to='places.Order'),
        ),
        migrations.AddField(
            model_name='customer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
