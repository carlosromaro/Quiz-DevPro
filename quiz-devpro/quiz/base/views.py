from django.db.models import Sum
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.timezone import now

from quiz.base.forms import PlayerForm
from quiz.base.models import Pergunta, Player, Resposta


def home(request):
    if request.method == 'POST':
        # Usuário existe
        email = request.POST['email']
        try:
            player = Player.objects.get(email=email)
        except Player.DoesNotExist:
            # Usuário não existe
            formulario = PlayerForm(request.POST)
            if formulario.is_valid():
                player = formulario.save()
                return redirect('/perguntas/1')
            else:
                contexto = {'formulario': formulario}
                return  render(request, 'base/home.html', contexto)
        else:
            request.session['player_id'] = player.id
            return redirect('/perguntas/1')
    return  render(request, 'base/home.html')


Max = 1000


def perguntas(requisicao, indice):
    try:
        player_id = requisicao.session['player_id']
    except KeyError:
        return redirect('/')
    else:
        try:
            pergunta = Pergunta.objects.filter(disponivel=True).order_by('id')[indice - 1]
        except IndexError:
            return redirect('/classificacao')
        else:
            contexto = {'indice_da_questao': indice, 'pergunta': pergunta}
            if requisicao.method == 'POST':
                resposta_indice = int(requisicao.POST['resposta_indice'])
                if resposta_indice == pergunta.alternativa_correta:
                    #armazenar ponto
                    try:
                        data_primeira_resposta = Resposta.objects.filter(pergunta=pergunta).order_by('respondida_em')[0].respondida_em
                    except IndexError:
                        Resposta(player_id=player_id, pergunta=pergunta, pontos=Max).save()
                    else:
                        dif = now() - data_primeira_resposta
                        dif_sec = int(dif.total_seconds())
                        pontos = max(Max - dif_sec, 10)
                        Resposta(player_id=player_id, pergunta=pergunta, pontos=pontos).save()
                    return redirect(f'/perguntas/{indice + 1}')
                contexto['resposta_indice'] = resposta_indice
                return render(requisicao, 'base/perguntas.html', context=contexto)




def classificacao(requisicao):
    try:
        player_id = requisicao.session['player_id']
    except KeyError:
        return redirect('/')
    else:
        pontos_dct = Resposta.objects.filter(player_id=player_id).aggregate(Sum('pontos'))
        pontos_player = pontos_dct['pontos__sum']

        qnt_maior_pontuacao = Resposta.objects.values('player').annotade(Sum('pontos')).filter(pontos__sum__gt = pontos_player).count()
        colocacao = qnt_maior_pontuacao + 1

        primeiros_colocados = list(Resposta.objects.values('player', 'player__nome').annotate(Sum('pontos')).ordey_by('-pontos__sum')[:5])

        contexto = {
            'pontos_player' : pontos_player,
            'colocacao' : colocacao,
            'primeiros_colocados' : primeiros_colocados,
        }
        return render(requisicao, 'base/classificacao.html', contexto)