from django.shortcuts import render, redirect, get_object_or_404
from .models import Classification
from .utils import crack_classification

# Create your views here.
def home(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if image is not None:
            original_image = image
            result_image, cracked_confidence, uncracked_confidence = crack_classification(original_image)
            classification = Classification.objects.create(
                original_image=original_image,
                result_image=result_image,
                cracked_confidence=cracked_confidence,
                uncracked_confidence=uncracked_confidence
            )
            classification.save()
            return redirect('filtered_result', pk=classification.id)
    return render(request, 'classifier/index.html')

def get_results(request):
    images = Classification.objects.all().order_by('-id')
    context = {'results': images}
    return render(request, 'classifier/results.html', context)

def get_filtered_result(request, pk):
    image = get_object_or_404(Classification, id=pk)
    context = {'result': image}
    return render(request, 'classifier/filtered.html', context)

def delete_image(request, pk):
    if request.method == 'POST':
        image = Classification.objects.filter(id=pk)
        if image.exists():
            image.first().delete()
            return redirect('results')
    return redirect('results')