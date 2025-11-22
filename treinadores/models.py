from django.db import models

from django.db import models

class Treinador(models.Model):
    """
    Modelo para representar um Treinador de Pokémon.
    """
    nome = models.CharField(
        max_length=100,
        help_text="Nome completo do treinador."
    )
    idade = models.IntegerField(
        help_text="Idade do treinador."
    )
    criado_em = models.DateTimeField(
        auto_now_add=True,
        help_text="Data de criação do registro."
    )
    atualizado_em = models.DateTimeField(
        auto_now=True,
        help_text="Data da última atualização do registro."
    )
    pokemons = models.ManyToManyField(
        'pokemons.Pokemon',
        blank=True, # permite criar um treinador sem pokémon
        related_name='treinadores'
    )

    class Meta:
        verbose_name = "Treinador"
        verbose_name_plural = "Treinadores"
        ordering = ['nome']

    def __str__(self):
        return f"Treinador: {self.nome} ({self.id})"
