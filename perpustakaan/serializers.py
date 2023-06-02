from rest_framework import serializers
from .models import *
class BukuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buku

class PeminjamanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peminjaman

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser