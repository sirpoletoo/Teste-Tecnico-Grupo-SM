from rest_framework import serializers
from .models import Pokemon
from .services import PokeAPIService

class PokemonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pokemon
        fields = ['id', 'nome', 'foto', 'altura', 'peso', 'criado_em', 'atualizado_em']
        read_only_fields = ['id', 'foto', 'altura', 'peso', 'criado_em', 'atualizado_em']
        extra_kwargs = {
            'nome': {'required': True, 'allow_blank': False}
        }
    def create(self, validated_data):
        """
        Criar um novo Pokémon
        Busca os dados na PokeAPI e salva o objeto
        """
        nome_pokemon = validated_data['nome']

        # Cria uma instância para o serviço
        api_service = PokeAPIService()

        try:
            # Busca os dados externos
            dados_pokeapi = api_service.buscar_dados_pokemon(nome_pokemon)
        
        except ValueError as e:
            # Trata o erro de "Pokémon não encontrado"
            raise serializers.ValidationError({'nome': str(e)})
        except ConnectionError as e:
            # Trata erro de conexão
            raise serializers.ValidationError({'detalhe': f"Falha na comunicação externa: {e}"})
        
        # Combina os dados (nome original + dados da API)
        # validated_data.update(dados_pokeapi)

        return super().create(dados_pokeapi)
    
    def update(self, instance, validated_data):
        """
        Função para o método PUT/PATCH
        Se o nome for alterado, busca novos dados na PokeAPI.
        """
        # checa se o campo 'nome' foi enviado na req
        novo_nome = validated_data.get('nome', None)

        # se um novo nome for inserido, atualiza os dados externos

        if novo_nome and novo_nome != instance.nome:
            api_service = PokeAPIService()

            try:
                dados_pokeapi = api_service.buscar_dados_pokemon(novo_nome)
            
            except ValueError as e:
                raise serializers.ValidationError({'nome': str(e)})
            except ConnectionError as e:
                raise serializers.ValidationError({'detalhe': f"Falha na comunicação externa: {e}"})
            
            # validated_data.update(dados_pokeapi)
        return super().update(instance, validated_data)

