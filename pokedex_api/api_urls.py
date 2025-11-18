from django.urls import path, include

urlpatterns = [
    path('', include('treinadores.urls')),
    path('', include('pokemons.urls')),
]
