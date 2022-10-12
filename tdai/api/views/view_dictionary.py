import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from operator import itemgetter

from api.repositories import repository_dictionary


@csrf_exempt
def dictionaries(request):
    if request.method == "GET":
        result = repository_dictionary.get_all(request=request)
        return JsonResponse(result, safe=False)
    elif request.method == "POST":
        params = json.loads(request.body)
        status, message =  itemgetter('status', 'message')(repository_dictionary.create(params=params))
        return JsonResponse({'message': message}, safe=False, status=status)


@csrf_exempt
def dictionary_detail(request, id):
    if request.method == 'GET':
        status, result, message = itemgetter('status', 'result', 'message')(repository_dictionary.get_by_id(id=id))
        return JsonResponse(result, safe=False) if status == 200 else JsonResponse({'message': message}, safe=False, status=status)
    elif request.method == 'PUT':
        params = json.loads(request.body)
        status, message = itemgetter('status', 'message')(repository_dictionary.update(id=id, params=params))
        return JsonResponse({'message': message}, safe=False, status=status)
    elif request.method == 'DELETE':
        status, message = itemgetter('status', 'message')(repository_dictionary.delete(id=id))
        return JsonResponse({'message': message}, safe=False, status=status)

