from django.urls import path
from .views import cdn_serve

urlpatterns = [
    path('cdn/<path:file_path>/', cdn_serve),
]
