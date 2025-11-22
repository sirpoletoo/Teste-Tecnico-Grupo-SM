from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Treinador
from .serializers import TreinadorSerializer
from pokemons.models import Pokemon

"""
Viewset é como se fosse o Controller, vai gerenciar as operações CRUD

"""
class TreinadorViewSet(viewsets.ModelViewSet):
    # Fornece as operações CRUD
    # Consulta no Repository
    queryset = Treinador.objects.all()

    # Serializer traduz as infos para json
    serializer_class = TreinadorSerializer

    @action(detail=True, methods=['post'])
    def adicionar_pokemon(self, request, pk=None):
        treinador = self.get_object()
        pokemon_id = request.data.get('pokemon_id')

        if not pokemon_id:
            return Response({"erro": "ID do Pokémon é obrigatório"}, status=400)
        
        pokemon = get_object_or_404(Pokemon, pk=pokemon_id)

        treinador.pokemons.add(pokemon)

        return Response({"mensagem": f"{pokemon.nome} adicionado à equipe do(a) {treinador.nome}!"})
    
    @action(detail=True, methods=['post'])
    def remover_pokemon(self, request, pk=None):
        treinador = self.get_object()
        pokemon_id = request.data.get('pokemon_id')

        pokemon = get_object_or_404(Pokemon, pk=pokemon_id)

        # Remove o pokemon
        treinador.pokemons.remove(pokemon)

        return Response({"mensagem": f"{pokemon.nome} foi removido da equipe do(a) {treinador.nome}"})
