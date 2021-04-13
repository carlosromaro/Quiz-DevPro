from django.db import models


# Create your models here.
class Player(models.Model):
    nome = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Pergunta(models.Model):
    sub_title = models.TextField()
    alternativa = models.JSONField()
    disponivel = models.BooleanField(default=False)
    alternativa_correta = models.IntegerField(choices=[
        (0, 'A'),
        (1, 'B'),
        (2, 'C'),
        (3, 'D')
    ])

    def __str__(self):
        return self.sub_title

class Resposta(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    pontos = models.IntegerField()
    respondida_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['player', 'pergunta'], name='resposta_unica')
        ]