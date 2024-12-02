from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request,data):
    return render(request,'index.html',{'data':data})

def index2(request):
    return render(request,'index2.html')
