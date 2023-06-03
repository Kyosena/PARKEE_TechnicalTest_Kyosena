from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class Buku(models.Model):
    isbn = models.BigIntegerField(primary_key = True, default = 1000000000000, validators=[MinValueValidator(1000000000000), MaxValueValidator(9999999999999)])
    judul = models.CharField(max_length = 180)
    stok = models.IntegerField()

    def __str__(self):
        return str(self.isbn)

# class CustomUser(AbstractUser):
#     primary_id = models.AutoField(primary_key = True)
#     username = models.CharField(max_length = 180, blank = False, null = False, unique = True)
    
#     def __str__(self):
#         return self.primary_id

class Peminjaman(models.Model):
    primary_id = models.AutoField(primary_key = True)
    buku = models.ForeignKey(Buku,on_delete = models.CASCADE, null=True)
    # informasi peminjam
    ktp = models.BigIntegerField()
    nama = models.CharField(max_length = 20)
    email = models.CharField(max_length = 30)
    # tanggal pinjaman
    tanggal_pinjam = models.DateField(auto_now_add = False, auto_now = False, blank = False)
    tanggal_deadline = models.DateField(auto_now = False, blank = False)
    tanggal_pengembalian = models.DateTimeField(auto_now_add = False, auto_now = False, blank = True, null = True)
    dikembalikan = models.BooleanField(default = False)
    telat = models.BooleanField(default = False)

    def clean(self):
        if self.tanggal_deadline and self.tanggal_pinjam and self.tanggal_deadline < self.tanggal_pinjam:
            raise ValidationError("End date cannot be earlier than start date.")
        if self.tanggal_deadline and self.tanggal_pinjam and (self.tanggal_deadline - self.tanggal_pinjam).days > 30:
            raise ValidationError("End date must be within 30 days of start date.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.primary_id)
    