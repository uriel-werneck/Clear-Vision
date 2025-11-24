from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'classifier/index.html')

def get_results(request):
    pass