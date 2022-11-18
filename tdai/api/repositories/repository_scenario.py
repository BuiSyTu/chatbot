from django.utils import timezone
from django.forms import model_to_dict

from chat_bot.models import Scenario, Step

def get_all(request):
    _scenarioes = Scenario.objects.all()

    # handle bot_id
    bot_id = None
    if 'bot_id' in request.session:
        bot_id = request.session['bot_id']
        _scenarioes = _scenarioes.filter(bot_id__exact=bot_id)

    result = list(_scenarioes.values())

    for scenario in result:
        steps = list(Step.objects.filter(scenario_id=scenario['id']).values())
        scenario['steps'] = steps
    return result

def create(params):
    try:
        Scenario.objects.create(
            bot_id=params['bot_id'] if 'bot_id' in params else None,
            name=params.get("name"),
            position=params.get("position"),
            created_time=timezone.now
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

def get_by_id(id: int):
    try:
        scenario = Scenario.objects.get(id=id)
        result = model_to_dict(scenario)
        return {
            'result': result,
            'status': 200,
            'message': None
        }
    except Exception as e:
        return {
            'message': str(e),
            'result': None,
            'status': 404
        }

def update(id: int, params):
    try:
        scenario = Scenario.objects.get(id=id)
        scenario.name = params.get('name')
        scenario.position = params.get('position')
        scenario.updated_time = timezone.now
        scenario.save()
        return {
            'status': 204,
            'message': None
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
        }

def delete(id: int):
    try:
        scenario = Scenario.objects.get(id=id)
        scenario.delete()
        return {
            'status': 204,
            'message': None
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
        }
