import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Intent, Sentence

@csrf_exempt
def intents(request):
    if request.method == "GET":
        _intents = Intent.objects.all()

        # handle bot_id
        if 'bot_id' in request.session:
            bot_id = request.session['bot_id']
            _intents = _intents.filter(bot_id__exact=bot_id).values()

        result = list(_intents.values())

        # handle include
        include = request.GET.get('include')
        if include == 'count':
            for intent in result:
                count = len(list(Sentence.objects.filter(intent_id__exact=intent['id'])))
                intent['count'] = count

        return JsonResponse(result, safe=False)
    elif request.method == 'POST':
        params = json.loads(request.body)
        Intent.objects.create(
            bot_id=request.session['bot_id'] if 'bot_id' in request.session else None,
            intent=params.get("intent"),
            description=params.get("description"),
            created_time=timezone.now()
        )
        return JsonResponse({"status": 200}, safe=False)


@csrf_exempt
def intent_detail(request, id):
    if request.method == 'GET':
        try:
            _intent = Intent.objects.get(id=id)
        except Exception as e:
            print(e)
            return JsonResponse(None, safe=False)

        sentences = list(Sentence.objects.filter(intent_id=id).values())
        result = {
            'id': _intent.id,
            'bot_id': _intent.bot_id,
            'intent': _intent.intent,
            'description': _intent.description,
            'sentences': sentences,
            'created_time': _intent.created_time,
            'updated_time': _intent.updated_time
        }

        return JsonResponse(result, safe=False)
    elif request.method == "PUT":
        params = json.loads(request.body)
        intent = Intent.objects.get(id=id)
        intent.intent = params.get('intent')
        intent.description = params.get('description')
        intent.updated_time = timezone.now()
        intent.save()
        return JsonResponse({"status": 200}, safe=False)
    elif request.method == 'DELETE':
        intent = Intent.objects.get(id=id)
        intent.delete()
        return JsonResponse({"status": 200}, safe=False)
