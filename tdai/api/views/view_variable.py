import json

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Variable



@csrf_exempt
def variables(request):
    if request.method == 'GET':
        _variables = Variable.objects.values()
        return JsonResponse(list(_variables), safe=False)
    elif request.method == 'POST':
        params = json.loads(request.body)
        Variable.objects.create (
            name=params.get('name'),
            variable_type=params.get('variable_type'),
            created_time=timezone.now
        )
        return JsonResponse({'status': 200}, safe=False)


@csrf_exempt
def variable_detail(request, id):
    if request.method == 'GET':
        _variables = list(Variable.objects.filter(id=id).values())

        if not _variables:
            return JsonResponse(None, safe=False)

        return JsonResponse(_variables[0], safe=False)
    elif request.method == 'PUT':
        params = json.loads(request.body)
        
        variable = Variable.objects.get(id=id)
        variable.name = params.get('name')
        variable.variable_type = params.get('variable_type')        
        variable.updated_time = timezone.now()
        variable.save()
        
        return JsonResponse({'status': 200}, safe=False)
    elif request.method == 'DELETE':
        variable = Variable.objects.get(id=id)
        variable.delete()
        return JsonResponse({'status': 200}, safe=False)