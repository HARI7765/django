from django.shortcuts import render,redirect
from django.http import HttpResponse
# Create your views here.
users=[]
def index(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        users.append({'username':username,'password':password})
        print(users)
    return render(request,'index.html')

def admlogin(request):
    return render(request,'adminhome.html')

adminusername="adm123"
adminpassword="123"
def adminlogin(request):
    if request.method=='POST':
        username=request.POST['username']
        print(username)
        password=request.POST['password']
        if  username==adminusername and password==adminpassword:
            print("logged in")
            return redirect(adminhome)
    return render(request,'adminlogin.html')

def adminhome(request):
    return render(request,'adminhome.html',{'users':users})
