from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


# Create your views here.
#test for connection of front and back end

def login_view(request):
    if request.method == 'POST':
        # Handle login logic here
        return HttpResponse("Login successful!")
    else:
        return render(request, 'login/login.html')
    
def register_view(request):
    if request.method == 'POST':
        # Handle registration logic here
        return HttpResponse("Registration successful!")
    else:
        return render(request, 'login/register.html')
    
def logout_view(request):
    # Handle logout logic here
    return HttpResponse("Logout successful!")

