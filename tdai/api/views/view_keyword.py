import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from operator import itemgetter

from chat_bot.models import Entity, KeyWord
from api.repositories import repository_keyword

@csrf_exempt
def key_words(request):
    if request.method == "GET":
        data = repository_keyword.get_all(request=request)  
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        params = json.loads(request.body)
        if 'bot_id' in request.session:
            params['bot_id'] = request.session['bot_id']
        status, message = itemgetter('status', 'message')(repository_keyword.create(params=params))
        return JsonResponse({'message': message}, safe=False, status=status)


@csrf_exempt
def key_word_detail(request, id):
    if request.method == 'GET':
        status, result, message = itemgetter('status', 'result', 'message')(repository_keyword.get_by_id(id=id))
        return JsonResponse(result, safe=False) if status == 200 else JsonResponse({'message': message}, safe=False, status=status)
    elif request.method == 'PUT':
        params = json.loads(request.body)
        status, message = itemgetter('status', 'message')(repository_keyword.update(id=id, params=params))
        return JsonResponse({'message': message}, safe=False, status=status)
    elif request.method == 'DELETE':
        status, message = itemgetter('status', 'message')(repository_keyword.delete(id=id))
        return JsonResponse({'message': message}, safe=False, status=status)
