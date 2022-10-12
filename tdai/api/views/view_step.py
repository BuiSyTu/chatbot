import json

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from operator import itemgetter

from api.repositories import repository_step

from api.services import service_variable, service_qa

@csrf_exempt
def steps(request):
    if request.method == "GET":
        result = repository_step.get_all(request=request)
        return JsonResponse(result, safe=False)
    elif request.method == "POST":
        params = json.loads(request.body)
        status, message = itemgetter('status', 'message')(repository_step.create(params=params))
        return JsonResponse({'message': message}, safe=False, status=status)


@csrf_exempt
def step_detail(request, id):
    if request.method == 'GET':
        status, result, message = itemgetter('status', 'result', 'message')(repository_step.get_by_id(id=id))
        return JsonResponse(result, safe=False) if status == 200 else JsonResponse({'message': message}, safe=False, status=status)
    elif request.method == 'PUT':
        params = json.loads(request.body)
        status, message = itemgetter('status', 'message')(repository_step.update(id=id, params=params))
        return JsonResponse({'message': message}, safe=False, status=status)
    elif request.method == 'DELETE':
        status, message = itemgetter('status', 'message')(repository_step.delete(id=id))
        return JsonResponse({'message': message}, safe=False, status=status)



@csrf_exempt
def jumpto_step(request):
    if request.method == "POST":
        params = json.loads(request.body)
        step_id = params.get('step_id')
        user_name = params.get('user_name')
        status = service_variable.init_history_variables(step_id, user_name)
        if status:
            answer_cards = service_qa.get_answer_cards(step_id,user_name)
            answer = service_qa.get_answer(answer_cards,step_id, user_name)
            return JsonResponse(answer, safe=False)
        
        return JsonResponse({
            'answers': [],
            'step_id': step_id
        }, safe=False)
