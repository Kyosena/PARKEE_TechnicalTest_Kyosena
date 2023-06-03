from rest_framework import serializers
from .models import *
class BukuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buku
        fields = '__all__'

class PeminjamanSerializer(serializers.ModelSerializer):
    buku = serializers.IntegerField(source='buku.isbn')
    def create(self, validated_data):
        buku_data = validated_data.pop('buku')
        buku_instance = Buku.objects.get(**buku_data)
        peminjaman_instance = Peminjaman.objects.create(buku=buku_instance, **validated_data)
        return peminjaman_instance
    class Meta:
        model = Peminjaman
        fields = '__all__'
