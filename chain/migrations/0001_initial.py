# Generated by Django 5.0.1 on 2024-01-24 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='название')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('country', models.CharField(max_length=50, verbose_name='страна')),
                ('city', models.CharField(max_length=50, verbose_name='город')),
                ('street', models.CharField(max_length=50, verbose_name='улица')),
                ('house_number', models.PositiveSmallIntegerField(verbose_name='номер дома')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания')),
                ('status', models.CharField(blank=True, editable=False, max_length=14, null=True, verbose_name='статус')),
                ('factory_id', models.PositiveSmallIntegerField(blank=True, editable=False, null=True, verbose_name='ID завода')),
                ('retail_network_id', models.PositiveSmallIntegerField(blank=True, editable=False, null=True, verbose_name='ID розничной сети')),
                ('entrepreneur_id', models.PositiveSmallIntegerField(blank=True, editable=False, null=True, verbose_name='ID ИП')),
                ('products', models.ManyToManyField(to='products.product', verbose_name='продукты')),
            ],
            options={
                'verbose_name': 'поставщик',
                'verbose_name_plural': 'поставщики',
                'ordering': ('name',),
            },
        ),
    ]
