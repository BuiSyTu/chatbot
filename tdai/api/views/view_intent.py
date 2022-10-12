import json

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from operator import itemgetter

from chat_bot.models import Intent, Sentence
from api.repositories import repository_intent

@csrf_exempt
def intents(request):
    if request.method == "GET":
        result = repository_intent.get_all(request=request)
        return JsonResponse(result, safe=False)
    elif request.method == 'POST':
        params = json.loads(request.body)
        if 'bot_id' in request.session:
            params['bot_id'] = request.session['bot_id']
        status, message = itemgetter('status', 'message')(repository_intent.create(params=params))
        return JsonResponse({'message': message}, safe=False, status=status)


@csrf_exempt
def intent_detail(request, id):
    if request.method == 'GET':
        status, result, message = itemgetter('status', 'result', 'message')(repository_intent.get_by_id(id=id))
        return JsonResponse(result, safe=False) if status == 200 else JsonResponse({'message': message}, safe=False, status=status)
    elif request.method == 'PUT':
        params = json.loads(request.body)
        status, message = itemgetter('status', 'message')(repository_intent.update(id=id, params=params))
        return JsonResponse({'message': message}, safe=False, status=status)
    elif request.method == 'DELETE':
        status, message = itemgetter('status', 'message')(repository_intent.delete(id=id))
        return JsonResponse({'message': message}, safe=False, status=status)
