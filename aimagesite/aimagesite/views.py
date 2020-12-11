from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    return render(request, 'homepage.html')
    
def about(request):
    return render(request, 'about.html')
    
def howitworks(request):
    return render(request, 'how_it_works.html')    