from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView


class TestHomePage(TemplateView):
    template_name = 'index.html'

class BudgetPage(TemplateView):
    template_name = 'contato.html'

class PrivacyPage(TemplateView):
    template_name = 'privacidade.html'
