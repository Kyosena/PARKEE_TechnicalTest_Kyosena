from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models.functions import ExtractDay
from .models import *
from .serializers import *
import pandas as pd

def index(request):
    buku = Buku.objects.all()
    data = {
        'buku' : buku
    }
    return render(request,"index.html",data)
class BukuListApiView(APIView):

    def get(self, request, *args, **kwargs):
        if not request.data:
            buku = Buku.objects.all()
            serializer = BukuSerializer(buku, many = True)
        else:
            data = request.data
            buku = Buku.objects.get(isbn = data.get('isbn'))
            serializer = BukuSerializer(buku)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'judul': request.data.get('judul'), 
            'isbn': request.data.get('isbn'), 
            'stok': request.data.get('stok')
        }
        serializer = BukuSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PeminjamanListApiView(APIView):
    def get(self, request, *args, **kwargs):
        if not request.data:
            peminjaman = Peminjaman.objects.all()
            serializer = PeminjamanSerializer(peminjaman, many = True)
        else:
            data = request.data
            peminjaman = Peminjaman.objects.get(primary_id = data.get('primary_id'))
            serializer = Peminjaman.Serializer(peminjaman)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self,request, *args, **kwargs):
        #update buku yang dipinjam
        ktp = request.data.get('ktp')
        nama = request.data.get('nama')
        isbn = request.data.get('buku')
        buku = Buku.objects.get(isbn=isbn)
        pengembalian = request.data.get('pengembalian')
        if pengembalian == False:
            if buku.stok == 0:
                return Response("Stock habis!", status=status.HTTP_200_OK)
            ktp = request.data.get('ktp')
            ktp_list = Peminjaman.objects.filter(ktp=ktp,dikembalikan=False)
            if ktp_list:
                return Response("Peminjam belum mengembalikan buku.")
            # elif ExtractDay(pd.to_datetime(tanggal_deadline) - pd.to_datetime(tanggal_pinjam)) > 30:
            #     return Response("Tanggal deadline harus tidak melebihi 30 hari dari tanggal peminjaman.")
            data = {
                'buku': buku,
                'ktp' : request.data.get('ktp'),
                'nama' : request.data.get('nama'),
                'email' : request.data.get('email'),
                'tanggal_pinjam' : request.data.get('tanggal_pinjam'),
                'tanggal_deadline' : request.data.get('tanggal_deadline')
            }
            serializer = PeminjamanSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                buku.stok = buku.stok - 1
                buku.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            buku.stok = buku.stok + 1
            buku.save()
            tanggal_pengembalian = request.data.get('tanggal_pengembalian')
            peminjaman = Peminjaman.objects.filter(ktp=ktp,nama=nama,buku=buku).latest("tanggal_pinjam")
            peminjaman.dikembalikan = True
            peminjaman.tanggal_pengembalian = tanggal_pengembalian
            peminjaman.telat = False
            if pd.to_datetime(tanggal_pengembalian).date() >pd.to_datetime(peminjaman.tanggal_deadline).date():
                peminjaman.telat = True
            peminjaman.save()
            if peminjaman.telat:
                return Response("Buku berhasil dikembalikan. Buku dikembalikan telat.")
            return Response("Buku berhasil dikebalikan tepat waktu.")
