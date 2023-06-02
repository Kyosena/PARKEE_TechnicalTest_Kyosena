from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class Buku(models.Model):
    primary_id = models.AutoField(primary_key = True)
    judul = models.CharField(max_length = 180)
    author = models.CharField(max_length = 180)
    stok = models.IntegerField()

    def __str__(self):
        return self.primary_id

class CustomUser(AbstractUser):
    primary_id = models.AutoField(primary_key = True)
    username = models.CharField(max_length = 180, blank = False, null = False, unique = True)
    
    def __str__(self):
        return self.primary_id

class Peminjaman(models.Model):
    primary_id = models.AutoField(primary_key = True)
    buku = models.ForeignKey(Buku,on_delete = models.CASCADE)
    peminjam = models.ForeignKey(CustomUser,on_delete = models.CASCADE)
    tanggal_pinjam = models.DateTimeField(auto_now_add = True, auto_now = False, blank = False)
    tanggal_deadline = models.DateTimeField(auto_now_add = False, auto_now = False, blank = False)
    tanggal_pengembalian = models.DateTimeField(auto_now_add = False, auto_now = False, blank = False)
    dikembalikan = models.BooleanField(default = False)

    def __str__(self):
        return self.primary_id
    