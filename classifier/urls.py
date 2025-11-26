from django.urls import path
from .views import home, get_results, get_filtered_result, delete_image
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('results/', get_results, name='results'),
    path('results/<int:pk>/', get_filtered_result, name='filtered_result'),
    path('results/<int:pk>/delete/', delete_image, name='delete_image')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)