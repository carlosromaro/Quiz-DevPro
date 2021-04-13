from django.contrib import admin

# Register your models here.
from quiz.base.models import Pergunta, Player, Resposta


@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    list_display = ('id', 'sub_title', 'disponivel')


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'data')


@admin.register(Resposta)
class RespostaAdmin(admin.ModelAdmin):
    list_display = ('respondida_em', 'player', 'pergunta', 'pontos')
