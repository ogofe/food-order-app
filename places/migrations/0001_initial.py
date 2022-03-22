# Generated by Django 2.2 on 2022-02-18 13:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import places.utils.helpers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
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
                ('required', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CustomizationOption',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.CharField(max_length=100)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=1000)),
                ('to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.Customization')),
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
                ('about', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=1000)),
                ('featured', models.BooleanField(default=False)),
                ('category', models.ManyToManyField(blank=True, to='places.Category')),
                ('customizations', models.ManyToManyField(blank=True, related_name='customizations', to='places.Customization')),
                ('images', models.ManyToManyField(blank=True, related_name='images', to='places.FoodImage')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_type', models.CharField(max_length=20)),
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
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('staff_id', models.CharField(default=places.utils.helpers.generate_staff_id, max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comment', models.CharField(blank=True, max_length=500, null=True)),
                ('by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.FoodItem')),
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
                ('delivered', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('on-route', 'On Route'), ('delivered', 'Delivered')], default='pending', max_length=20)),
                ('delivery_is_on', models.BooleanField(default=False)),
                ('invoice_id', models.CharField(default=places.utils.helpers.generate_invoice_id, max_length=12)),
                ('paid', models.BooleanField(default=False)),
                ('items', models.ManyToManyField(blank=True, to='places.OrderItem')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.Customer')),
            ],
        ),
        migrations.AddField(
            model_name='fooditem',
            name='reviews',
            field=models.ManyToManyField(blank=True, related_name='reviews', to='places.Review'),
        ),
        migrations.AddField(
            model_name='fooditem',
            name='tags',
            field=models.ManyToManyField(blank=True, to='places.Tag'),
        ),
        migrations.AddField(
            model_name='foodimage',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.FoodItem'),
        ),
        migrations.AddField(
            model_name='customization',
            name='default_option',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='places.CustomizationOption'),
        ),
        migrations.AddField(
            model_name='customization',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.FoodItem'),
        ),
        migrations.AddField(
            model_name='customization',
            name='options',
            field=models.ManyToManyField(blank=True, related_name='choices', to='places.CustomizationOption'),
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
