from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Card, Step


@csrf_exempt
def cards(request):
    return render(request, 'cards/index.html')

@csrf_exempt
def add_cards(request):
    if request.method == 'GET':
        steps = Step.objects.values()
        data = {
            "steps": steps
        }
        return render(request, 'cards/add.html', data)


@csrf_exempt
def card_detail(request, id):
    if request.method == 'GET':
        card = Card.objects.get(id=id)
        steps = Step.objects.values()
        data = {
            'card': card,
            'steps': steps
        }
        return render(request, 'cards/update.html', data)


