from django.urls import path
from .views import BatalhaView

urlpatterns = [
    path('batalhar/', BatalhaView.as_view(), name='simular-batalha')
]