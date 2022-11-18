import json

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Variable



@csrf_exempt
def variables(request):
    if request.method == 'GET':
        bot_id = None
        _variables = Variable.objects.all()

        # handle bot_id in sesstion
        if 'bot_id' in request.session:
            bot_id = request.session['bot_id']
            _variables = _variables.filter(bot_id__exact=bot_id)

        # handle bot_id in request
        bot_id = request.GET.get('bot_id', None)
        if bot_id is not None and bot_id != '0':
            _variables = _variables.filter(bot_id__exact=bot_id)

        return JsonResponse(list(_variables.values()), safe=False)
    elif request.method == 'POST':
        params = json.loads(request.body)
        if 'bot_id' in request.session:
            params['bot_id'] = request.session['bot_id']
        Variable.objects.create (
            bot_id=params['bot_id'] if 'bot_id' in params else None,
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