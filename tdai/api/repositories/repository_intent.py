from django.utils import timezone
from django.forms import model_to_dict

from chat_bot.models import Intent, Sentence

def get_all(request):
    _intents = Intent.objects.all()

    # handle bot_id
    if 'bot_id' in request.session:
        bot_id = request.session['bot_id']
        _intents = _intents.filter(bot_id__exact=bot_id).values()

    result = list(_intents.values())

    # handle include
    include = request.GET.get('include', None)
    if include == 'count':
        for intent in result:
            count = len(list(Sentence.objects.filter(intent_id__exact=intent['id'])))
            intent['count'] = count
    return result

def create(params):
    try:
        Intent.objects.create(
            bot_id=params['bot_id'] if 'bot_id' in params else None,
            intent=params.get("intent"),
            description=params.get("description"),
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

def get_by_id(id: int):
    try:
        _intent = Intent.objects.get(id=id)
        result = model_to_dict(_intent)
        sentences = list(Sentence.objects.filter(intent_id=id).values())
        result['sentences'] = sentences

        return {
            'status': 200,
            'message': None,
            'result': result
        }
    except Exception as e:
        print(e)
        return {
            'status': 404,
            'message': str(e),
            'result': None
        }

def update(id: int, params):
    try:
        intent = Intent.objects.get(id=id)
        intent.intent = params.get('intent')
        intent.description = params.get('description')
        intent.updated_time = timezone.now()
        intent.save()
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
        intent = Intent.objects.get(id=id)
        intent.delete()
        return {
            'status': 204,
            'message': None
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
        }
