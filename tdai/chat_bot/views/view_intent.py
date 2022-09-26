from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Intent, Sentence


@csrf_exempt
def intents(request):
    return render(request, 'intents/index.html')


@csrf_exempt
def add_intents(request):
    if request.method == 'GET':
        _intents = list(Intent.objects.values("intent"))
        data = {
            "intents": _intents
        }
        return render(request, 'intents/add.html', data)


@csrf_exempt
def intent_detail(request, id):
    if request.method == 'GET':
        intent = Intent.objects.get(id=id)
        data = {
            'intent': intent
        }
        return render(request, 'intents/update.html', data)