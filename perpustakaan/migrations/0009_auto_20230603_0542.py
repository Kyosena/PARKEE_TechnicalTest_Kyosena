# Generated by Django 3.2.6 on 2023-06-03 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perpustakaan', '0008_alter_peminjaman_tanggal_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peminjaman',
            name='tanggal_pengembalian',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='peminjaman',
            name='tanggal_pinjam',
            field=models.DateField(),
        ),
    ]