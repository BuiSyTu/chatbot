from django.http import JsonResponse, QueryDict
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Dictionary

import json

@csrf_exempt
def dictionaries(request):
    if request.method == "GET":
        _dictionaries = Dictionary.objects.all()

        # hanle bot_id
        if 'bot_id' in request.session:
            bot_id = request.session['bot_id']
            _dictionaries = _dictionaries.filter(bot_id__exact=bot_id)

        return JsonResponse(list(_dictionaries.values()), safe=False)
    elif request.method == "POST":
        params = json.loads(request.body)
        Dictionary.objects.create(
            bot_id=bot_id,
            word=params.get("word"),
            synonym=params.get("synonym"),
            created_time=timezone.now()
        )
        return JsonResponse({"status": 200}, safe=False)


@csrf_exempt
def dictionary_detail(request, id):
    if request.method == 'GET':
        _dictionaries = list(Dictionary.objects.filter(id=id).values())

        if not _dictionaries:
            return JsonResponse(None, safe=False)

        return JsonResponse(_dictionaries[0], safe=False)
    elif request.method == "PUT":
        params = json.loads(request.body)
        dictionary = Dictionary.objects.get(id=id)
        dictionary.word = params.get('word')
        dictionary.synonym = params.get('synonym')
        dictionary.updated_time = timezone.now()
        dictionary.save()
        return JsonResponse({"status": 200}, safe=False)
    elif request.method == "DELETE":
        dictionary = Dictionary.objects.get(id=id)
        dictionary.delete()
        return JsonResponse({"status": 200}, safe=False)

