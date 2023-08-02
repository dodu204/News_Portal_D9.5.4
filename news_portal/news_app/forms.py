from django import forms
from .models import Category


class SubscribeForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)


class UnsubscribeForm(forms.Form):
    categories = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
