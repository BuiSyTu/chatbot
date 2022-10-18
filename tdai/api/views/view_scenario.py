import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from operator import itemgetter
from api.repositories import repository_scenario


@csrf_exempt
def scenarios(request):
    if request.method == 'GET':
        result = repository_scenario.get_all(request=request)
        return JsonResponse(result, safe=False)
    elif request.method == 'POST':
        params = json.loads(request.body)
        status, message = itemgetter('status', 'message')(repository_scenario.create(params=params))
        return JsonResponse({'message': message}, safe=False, status=status)


@csrf_exempt
def scenario_detail(request, id):
    if request.method == 'GET':
        status, result, message = itemgetter('status', 'result', 'message')(repository_scenario.get_by_id(id=id))
        return JsonResponse(result, safe=False) if status == 200 else JsonResponse({'message': message}, safe=False, status=status)
    elif request.method == 'PUT':
        params = json.loads(request.body)
        status, message = itemgetter('status', 'message')(repository_scenario.update(id=id, params=params))
        return JsonResponse({'message': message}, safe=False, status=status)
    elif request.method == 'DELETE':
        status, message = itemgetter('status', 'message')(repository_scenario.delete(id=id))
        return JsonResponse({'message': message}, safe=False, status=status)

