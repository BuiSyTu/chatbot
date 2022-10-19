import json

from django.utils import timezone
from django.forms import model_to_dict

from chat_bot.models import Step, Scenario, Card, Variable

def get_all(request):
    _steps = Step.objects.all()

    # handle bot_id
    bot_id = None
    if 'bot_id' in request.session:
        bot_id = request.session['bot_id']
        _steps = _steps.filter(bot_id__exact=bot_id)

    # handle scenario_id
    scenario_id = request.GET.get('scenario_id', None)
    if scenario_id is not None:
        _steps = _steps.filter(scenario_id__exact=scenario_id)

    result = list(_steps.values())
    for step in result:
        scenario = Scenario.objects.get(id=step['scenario_id'])
        step['scenario'] = model_to_dict(scenario)
    return result

def create(params):
    try:
        Step.objects.create(
            scenario_id=params.get('scenario_id'),
            name=params.get('name'),
            position=params.get('position'),
            created_time=timezone.now()
        )
        return {
            'status': 201,
            'message': 'Thêm thành công'
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
        }

def get_by_id(id):
    try:
        step = Step.objects.get(id=id)
    except Exception as e:
        return {
            'message': str(e),
            'result': None,
            'status': 404
        }

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

    return {
        'result': result,
        'status': 200,
        'message': None
    }

def update(id, params):
    try:
        step = Step.objects.get(id=id)
        step.scenario_id = params.get('scenario_id')
        step.name = params.get('name')
        step.position = params.get('position')
        step.updated_time = timezone.now()
        step.save()
        return {
            'status': 204,
            'message': None
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
        }

def delete(id):
    try:
        step = Step.objects.get(id=id)
        step.delete()
        return {
            'status': 204,
            'message': None
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
        }
