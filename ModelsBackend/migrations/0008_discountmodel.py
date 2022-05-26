# Generated by Django 4.0.4 on 2022-05-26 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ModelsBackend', '0007_alter_storeuserpermissionsmodel_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discountID', models.IntegerField()),
                ('percent', models.IntegerField()),
                ('type', models.CharField(choices=[('Product', 'Product'), ('Category', 'Category'), ('Store', 'Store'), ('Composite', 'Composite')], max_length=100)),
                ('composite_type', models.CharField(choices=[('Max', 'Max'), ('Add', 'Add'), ('Or', 'Or')], max_length=100, null=True)),
                ('decide', models.IntegerField(choices=[(1, 1), (2, 2)], null=True)),
                ('dID1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='firstDiscountID', to='ModelsBackend.discountmodel')),
                ('dID2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='secondDiscountID', to='ModelsBackend.discountmodel')),
            ],
        ),
    ]
