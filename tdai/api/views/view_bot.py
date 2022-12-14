from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.forms import model_to_dict

from chat_bot.models import Bot, Intent, Entity, Sentence

import json

@csrf_exempt
def bots(request):
    if request.method == 'GET':
        _bots = Bot.objects.all()

        # handle user_id
        user_id = None
        if 'user_id' in request.session:
            user_id = request.session.get('user_id')
            _bots = _bots.filter(user_id__exact=user_id)

        result = []
        for bot in _bots:
            result_item = model_to_dict(bot)

            result_item['user_id'] = result_item['user']
            del result_item['user']

            result_item['total_intent'] = len(Intent.objects.filter(bot_id=bot.id))
            result_item['total_entity'] = len(Entity.objects.filter(bot_id=bot.id))
            result_item['total_sentence'] = len(Sentence.objects.filter(bot_id=bot.id))
            result.append(result_item)

        return JsonResponse(result, safe=False)
    elif request.method == 'POST':
        params = json.loads(request.body)
        Bot.objects.create(
            user_id=request.session['user_id'] if 'user_id' in request.session else None,
            name=params.get('name'),
            description=params.get('description'),
            created_time=timezone.now()
        )
        return JsonResponse({'status': 200}, safe=False)

@csrf_exempt
def bot_detail(request, id):
    if request.method == 'GET':
        _bots = list(Bot.objects.filter(id=id).values())

        if not _bots:
            return JsonResponse(None, safe=False)

        return JsonResponse(_bots[0], safe=False)
    elif request.method == 'PUT':
        params = json.loads(request.body)
        bot = Bot.objects.get(id=id)
        bot.name = params.get('name')
        bot.description = params.get('description')
        bot.updated_time = timezone.now()
        bot.save()
        return JsonResponse({'status': 200}, safe=False)
    elif request.method == 'DELETE':
        bot = Bot.objects.get(id=id)
        bot.delete()
        return JsonResponse({'status': 200}, safe=False)

@csrf_exempt
def bot_choose(request, id):
    if request.method == 'GET':
        _bots = Bot.objects.filter(id=id).values()

        if not _bots:
            return JsonResponse(None, safe=False)
        else:
            request.session['bot_id'] = _bots[0]['id']
            return JsonResponse(_bots[0], safe=False)
