import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from operator import itemgetter

from api.repositories import repository_sentence


@csrf_exempt
def sentences(request):
    if request.method == "GET":
        result = repository_sentence.get_all(request=request)
        return JsonResponse(result, safe=False)
    elif request.method == 'POST':
        params = json.loads(request.body)
        if 'bot_id' in request.session:
            params['bot_id'] = request.session['bot_id']
        status, message = itemgetter('status', 'message')(repository_sentence.create(params=params))
        return JsonResponse({'message': message}, safe=False, status=status)


@csrf_exempt
def sentence_detail(request, id):
    if request.method == 'GET':
        status, result, message = itemgetter('status', 'result', 'message')(repository_sentence.get_by_id(id=id))
        return JsonResponse(result, safe=False) if status == 200 else JsonResponse({'message': message}, safe=False, status=status)
    elif request.method == 'PUT':
        params = json.loads(request.body)
        status, message = itemgetter('status', 'message')(repository_sentence.update(id=id, params=params))
        return JsonResponse({'message': message}, safe=False, status=status)
    elif request.method == 'DELETE':
        status, message = itemgetter('status', 'message')(repository_sentence.delete(id=id))
        return JsonResponse({'message': message}, safe=False, status=status)

