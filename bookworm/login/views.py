from django.shortcuts import render
from django.http import HttpResponse
from django.views import View


# Create your views here.
#test for connection of front and back end

def hello_world(request):
    return HttpResponse("Hello, World!")

class HelloWorldView(View):
     def get(self, request):
          return HttpResponse("Hello, World View!")
