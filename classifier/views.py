from django.shortcuts import render
from .models import Classification

# Create your views here.
def home(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image is not None:
            result = 'Sample Result'
            classification = Classification.objects.create(image=image, result=result)
            classification.save()
            context = {'classification': classification}
            return render(request, 'classifier/index.html', context)
    return render(request, 'classifier/index.html')