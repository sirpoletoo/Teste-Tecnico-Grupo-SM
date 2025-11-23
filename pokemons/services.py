import requests
import unicodedata

class PokeAPIService:
    """
    Responsável por buscar dados na PokeAPI
    """
    BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

    def buscar_dados_pokemon(self, nome_pokemon):
        """
        Faz uma requisição GET para a PokeAPI.
        Retorna foto, altura e peso.
        Devolve uma mensagem de erro caso o Pokemon não seja encontrado
        """
        # tratamento de dados no nome do pokémon, para tirar os acentos e deixar em minúsculo
        nome_formatado = unicodedata.normalize('NFKD', nome_pokemon).encode('ASCII', 'ignore').decode('utf-8').lower().strip()
        url = f"{self.BASE_URL}{nome_formatado}/"

        try:
            # Fazer a requisição HTTP
            response = requests.get(url, timeout=10)
            response.raise_for_status()

        except requests.exceptions.HTTPError as e:
            # Tratar o erro 404
            if response.status_code == 404:
                # Gera uma exceção personalizada no Serializer
                raise ValueError(f"Pokémon '{nome_pokemon}' não encontrado na PokeAPI")
            
            # Trata os demais erros
            response.raise_for_status()
        
        except requests.exceptions.RequestException as e:
            # Trata erros de conexão
            raise ConnectionError(f"Erro de comunicação com a PokeAPI (Status {response.status_code}). Verifique se o nome '{nome_pokemon}' é válido.")
        
        data = response.json()

        # Extrair e retornar os dados
        return {
            'foto': data['sprites']['front_default'],
            'altura': data['height'], # CM
            'peso': data['weight'] # HECTOGRAMAS
        }