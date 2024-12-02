from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
user=[]
def index(request):
    if request.method=='POST':
        username=request.POSt['username']
        password=request.POSt['password']
        users.append({'username':username,'password':password})
        return redirect(index2)
    return render(request,'index.html')

def index2(request):
    return render(request,'index2.html')

adminuser
