from django.forms import ModelForm

from quiz.base.models import Player


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['nome', 'email']