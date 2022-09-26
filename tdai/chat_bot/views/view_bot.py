from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Bot, Intent, Entity, Sentence


@csrf_exempt
def bots(request):
    if request.method == 'GET':
        _bots = Bot.objects.values()

        for bot in _bots:
            total_intent = len(Intent.objects.filter(bot_id = bot['id']))
            total_entity = len(Entity.objects.filter(bot_id = bot['id']))
            total_sentence = len(Sentence.objects.filter(bot_id = bot['id']))
            bot['total_intent'] = total_intent
            bot['total_entity'] = total_entity
            bot['total_sentence'] = total_sentence

        data = {'bots': _bots}
        return render(request, 'bots/index.html', data)


@csrf_exempt
def add_bot(request):
    if request.method == 'GET':
        bots = list(Bot.objects.values('name'))
        data = {
            'bots': bots
        }
        return render(request, 'bots/add.html', data)


@csrf_exempt
def bot_detail(request, id):
    if request.method == 'GET':
        bot = Bot.objects.get(id=id)
        data = {
            'bot': bot
        }
        return render(request, 'bots/update.html', data)



