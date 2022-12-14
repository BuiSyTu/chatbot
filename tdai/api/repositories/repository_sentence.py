from django.utils import timezone
from django.forms import model_to_dict

from chat_bot.models import Intent, Sentence

def get_all(request):
    bot_id = None
    intent_id = None

    _sentences = Sentence.objects.all()

    # handle bot_id in sesstion
    if 'bot_id' in request.session:
        bot_id = request.session['bot_id']
        _sentences = _sentences.filter(bot_id__exact=bot_id)

    # handle bot_id in request
    bot_id = request.GET.get('bot_id', None)
    if bot_id is not None and bot_id != '0':
        _sentences = _sentences.filter(bot_id__exact=bot_id)

    # handle intent_id
    intent_id = request.GET.get('intent_id', None)
    if intent_id is not None and intent_id != '0':
        _sentences = _sentences.filter(intent_id__exact=intent_id)

    result = list(_sentences.values())
    for sen in result:
        intent = Intent.objects.get(id=sen['intent_id'])
        sen['intent'] = model_to_dict(intent)
    return result

def create(params):
    try:
        Sentence.objects.create(
            bot_id=params['bot_id'] if 'bot_id' in params else None,
            sentence=params.get("sentence"),
            intent_id=params.get("intent_id"),
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
        _sentence = Sentence.objects.get(id=id)
        result = model_to_dict(_sentence)
        result['intent_id'] = result['intent']
        result['intent'] = model_to_dict(Intent.objects.get(id=result['intent_id'])) if result['intent_id'] != None else None

        return {
            'status': 200,
            'message': None,
            'result': result
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e),
            'result': None
        }

def update(id: int, params):
    try:
        sentence = Sentence.objects.get(id=id)
        sentence.sentence = params.get('sentence')
        sentence.intent_id = params.get('intent_id')
        sentence.updated_time = timezone.now()
        sentence.save()
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
        sentence = Sentence.objects.get(id=id)
        sentence.delete()
        return {
            'status': 204,
            'message': None
        }
    except Exception as e:
        return {
            'status': 500,
            'message': str(e)
        }
