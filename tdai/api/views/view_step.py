import json

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from chat_bot.models import Step, Scenario, Card, Variable

from module import  module_qa, module_variables


@csrf_exempt
def steps(request):
    if request.method == "GET":
        _steps = Step.objects.all()

        # handle bot_id
        bot_id = None
        if 'bot_id' in request.session:
            bot_id = request.session['bot_id']
            _steps = _steps.filter(bot_id__exact=bot_id)

        # handle scenario_id
        scenario_id = request.GET.get('scenario_id')
        if (scenario_id != None and scenario_id != '0'):
            _steps = _steps.filter(scenario_id__exact=scenario_id)

        result = list(_steps.values())
        for step in result:
            # add scenario
            scenarios = list(Scenario.objects.filter(id=step['scenario_id']).values())
            step['scenario'] = scenarios[0]

        return JsonResponse(result, safe=False)
    elif request.method == "POST":
        params = json.loads(request.body)
        Step.objects.create(
            scenario_id=params.get('scenario_id'),
            name=params.get('name'),
            position=params.get('position'),
            created_time=timezone.now()
        )
        return JsonResponse({"status": 200}, safe=False)


@csrf_exempt
def step_detail(request, id):
    if request.method == 'GET':
        try:
            step = Step.objects.get(id=id)
        except Exception as e:
            print(e)
            return JsonResponse(None, safe=False)

        cards = list(Card.objects.filter(step_id=step.id).values())
        for card in cards:
            config = json.loads(card['config'])
            if card['card_type'] == 'form':
                questions = config['questions']
                for question in questions:
                    variable = Variable.objects.get(id=question['variable_id'])
                    question['variable_name'] = variable.name

            card['config'] = config

        result = {
            'id': step.id,
            'scenario_id': step.scenario_id,
            'name': step.name,
            'position': step.position,
            'cards': cards,
            'created_time': step.created_time,
            'updated_time': step.updated_time
        }

        return JsonResponse(result, safe=False)

        return JsonResponse(step, safe=False)
    elif request.method == 'PUT':
        params = json.loads(request.body)
        step = Step.objects.get(id=id)
        step.scenario_id = params.get('scenario_id')
        step.name = params.get('name')
        step.position = params.get('position')
        step.updated_time = timezone.now()
        step.save()
        return JsonResponse({'status': 200}, safe=False)
    elif request.method == 'DELETE':
        step = Step.objects.get(id=id)
        step.delete()
        return JsonResponse({'status': 200}, safe=False)


@csrf_exempt
def jumpto_step(request):
    if request.method == "POST":
        params = json.loads(request.body)
        step_id = params.get('step_id')
        user_name = params.get('user_name')
        status = module_variables.init_history_variables(step_id, user_name)
        if status:
            answer_cards = module_qa.get_answer_cards(step_id,user_name)
            answer = module_qa.get_answer(answer_cards,step_id, user_name)
            return JsonResponse(answer, safe=False)
        
        return JsonResponse({
            'answers': [],
            'step_id': step_id
        }, safe=False)
