from django.utils import timezone
from django.forms import model_to_dict

from chat_bot.models import Scenario

def get_all(request):
    _scenarioes = Scenario.objects.all()

    # handle bot_id
    bot_id = None
    if 'bot_id' in request.session:
        bot_id = request.session['bot_id']
        _scenarioes = _scenarioes.filter(bot_id__exact=bot_id)

    result = list(_scenarioes.values())
    return result

def create(params):
    try:
        Scenario.objects.create(
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

def get_by_id(id):
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

def update(id, params):
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

def delete(id):
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