from django import forms
from . import models


class CommentForm(forms.Form):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',
                'rows': 1,
                'style': 'overflow:hidden; resize:none;',
            },
        ),
        label="Ajouter un commentaire",
    )
    answer_to_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False,
    )


class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content', 'answer_to']


class ReportForm(forms.Form):
    reason = forms.ChoiceField(
        choices=[
            ('discrimination', 'Discours haineux / discrimination'),
            ('terror', 'Apologie du terrorisme'),
            ('menace', 'Menace ou incitation à la violence'),
            ('obscenity', 'Contenu obscène'),
            ('diffamation', 'Diffamation'),
            ('irrelevant', 'Hors sujet'),
            ('other', 'Autre'),
        ],
        widget=forms.RadioSelect(),
    )
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="Commentaires supplémentaires (optionnel)",
    )
    type_ = forms.CharField(
        widget=forms.HiddenInput(),
        required=False,
    )
    id_ = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False,
    )
