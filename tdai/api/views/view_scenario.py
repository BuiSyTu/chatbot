import json

from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from chat_bot.models import Scenario, Step


@csrf_exempt
def scenarios(request):
    if request.method == "GET":
        _scenarios = Scenario.objects.all()

        # handle bot_id
        bot_id = request.GET.get('bot_id', None)
        if bot_id != None:
            _scenarios = _scenarios.filter(bot_id__exact=bot_id)


        # handle return
        data = []
        for scenario in _scenarios:
            steps = list(Step.objects.filter(scenario_id=scenario.id).values())
            data.append({
                'id': scenario.id,
                'bot_id': scenario.bot_id,
                'name': scenario.name,
                'position': scenario.position,
                'steps': steps,
                'created_time': scenario.created_time,
                'updated_time': scenario.updated_time
            })

        return JsonResponse(data, safe=False)
    elif request.method == "POST":
        params = json.loads(request.body)
        Scenario.objects.create(
            bot_id=3,
            name=params["name"],
            position=params["position"],
            created_time=timezone.now
        )
        return JsonResponse({"status": 200}, safe=False)

@csrf_exempt
def scenario_detail(request, id):
    if request.method == "GET":
        _scenarios = list(Scenario.objects.filter(id=id).values())

        if not _scenarios:
            return JsonResponse(None, safe=False)

        return JsonResponse(_scenarios[0], safe=False)
    elif request.method == "PUT":
        params = json.loads(request.body)

        scenario = Scenario.objects.get(id=id)
        scenario.bot_id = 3
        scenario.name = params.get('name')
        scenario.position = params.get('position')
        scenario.updated_time = timezone.now
        scenario.save()

        return JsonResponse({"status": 200}, safe=False)
    elif request.method == 'DELETE':
        scenario = Scenario.objects.get(id=id)
        scenario.delete()
        return JsonResponse({"status": 200}, safe=False)

